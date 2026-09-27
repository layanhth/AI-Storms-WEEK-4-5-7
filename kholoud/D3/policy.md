# Resource Policy

Our policy is to protect latency-sensitive serving workloads with guaranteed resources, throttle batch workloads with explicit CPU limits, and allow low-priority dashboard workloads to use spare capacity.

## Serving

```yaml
resources:
  requests:
    cpu: "1"
    memory: 512Mi
  limits:
    cpu: "1"
    memory: 512Mi
```

QoS class: Guaranteed

## Batch

```yaml
resources:
  requests:
    cpu: 100m
    memory: 128Mi
  limits:
    cpu: 500m
    memory: 512Mi
```

QoS class: Burstable

## Dashboard

No CPU or memory requests or limits.

QoS class: BestEffort

## Noisy-neighbour measurement

Unlimited burners: p95 = 5000 ms, fails = 576.

CPU-limited burners at 500m: p95 = 5000 ms, fails = 579.

In this experiment, the 500m CPU limit did not improve measured p95 latency, but it still prevents each batch worker from consuming unlimited CPU, so batch remains the first workload we choose to throttle.
