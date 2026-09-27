#!/usr/bin/env bash
set -u

DOOMED=""
cleanup() { [ -n "$DOOMED" ] && kubectl delete pod "$DOOMED" --ignore-not-found >/dev/null 2>&1; }
trap cleanup EXIT
fail() { echo "GREEN CHECK: FAIL ($1)"; exit 1; }

command -v kubectl >/dev/null || fail "kubectl not on PATH"

DEPLOY="${DEPLOY:-serving}"
kubectl get deployment "$DEPLOY" >/dev/null 2>&1 || fail "no deployment '$DEPLOY' in this namespace"

spec=$(kubectl get deployment "$DEPLOY" -o json)
for want in requests limits; do
  printf '%s' "$spec" | grep -q "\"$want\"" || fail "serving spec has no $want; Step 1 not applied"
done
for res in cpu memory; do
  v=$(kubectl get deployment "$DEPLOY" -o jsonpath="{.spec.template.spec.containers[0].resources.requests.$res}")
  [ -n "$v" ] || fail "serving requests carry no $res"
done
image=$(kubectl get deployment "$DEPLOY" -o jsonpath='{.spec.template.spec.containers[0].image}')

TEAM_NS="${TEAM_NS:-team}"
gpu=$(kubectl get nodes -o jsonpath='{.items[*].status.allocatable.nvidia\.com/gpu}' 2>/dev/null)
if printf '%s' "$gpu" | grep -q '[1-9]'; then
  ENGINE="${ENGINE:-vllm}"
  kubectl -n "$TEAM_NS" get deployment "$ENGINE" >/dev/null 2>&1 \
    || fail "this node has a card, but no engine '$ENGINE' in namespace '$TEAM_NS'; Step 6 has not run"

  for res in cpu memory 'nvidia\.com/gpu'; do
    v=$(kubectl -n "$TEAM_NS" get deployment "$ENGINE" -o jsonpath="{.spec.template.spec.containers[0].resources.requests.$res}")
    [ -n "$v" ] || fail "the engine requests no ${res//\\/}"
  done

  pod=$(kubectl -n "$TEAM_NS" get pods -l app=vllm --sort-by=.metadata.creationTimestamp \
        -o jsonpath='{.items[-1:].metadata.name}' 2>/dev/null)
  [ -n "$pod" ] || fail "no pod with label app=vllm in '$TEAM_NS'"

  qos=$(kubectl -n "$TEAM_NS" get pod "$pod" -o jsonpath='{.status.qosClass}')
  [ "$qos" = "Guaranteed" ] \
    || fail "engine QoS is $qos, not Guaranteed; requests must equal limits on cpu and memory"

  kubectl -n "$TEAM_NS" get svc vllm >/dev/null 2>&1 \
    && fail "a Service named 'vllm' exists in '$TEAM_NS'; it sets VLLM_PORT and kills the engine on next restart"

  kubectl -n "$TEAM_NS" get pod "$pod" -o jsonpath='{.status.conditions[?(@.type=="Ready")].status}' | grep -q True \
    || fail "engine pod is not Ready"

  kubectl -n "$TEAM_NS" exec "$pod" -- nvidia-smi -L >/dev/null 2>&1 \
    || fail "the container cannot see the GPU it was charged for"

  echo "team engine: Guaranteed, GPU visible inside the container, Service name safe"
fi

DOOMED="verify-wants-gpu-$$"
cat <<EOF | kubectl apply -f - >/dev/null || fail "could not create the doomed GPU pod"
apiVersion: v1
kind: Pod
metadata:
  name: $DOOMED
spec:
  containers:
    - name: wisher
      image: $image
      command: ["sleep", "60"]
      resources:
        requests: {nvidia.com/gpu: 1}
        limits: {nvidia.com/gpu: 1}
EOF

verdict=""
for _ in $(seq 1 20); do
  phase=$(kubectl get pod "$DOOMED" -o jsonpath='{.status.phase}' 2>/dev/null)
  events=$(kubectl get events --field-selector "involvedObject.name=$DOOMED" -o jsonpath='{.items[*].message}' 2>/dev/null)
  if printf '%s' "$events" | grep -qi 'nvidia.com/gpu'; then verdict=ok; break; fi
  [ "$phase" = "Running" ] && fail "the GPU pod scheduled: a card was free"
  sleep 1
done
[ "$verdict" = "ok" ] || fail "no scheduler event naming nvidia.com/gpu appeared"

phase=$(kubectl get pod "$DOOMED" -o jsonpath='{.status.phase}')
[ "$phase" = "Pending" ] || fail "doomed pod is $phase, expected Pending"

echo "overdraft verified: Pending with 'Insufficient nvidia.com/gpu'"
echo "GREEN CHECK: PASS"
