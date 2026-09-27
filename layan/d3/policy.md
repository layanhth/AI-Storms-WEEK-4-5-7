Policy: serving is guaranteed enough resources for reliable response time, dashboard may burst when needed, and batch is throttled first.

serving:
  resources:
    requests:
      cpu: "1"
      memory: 1Gi
    limits:
      cpu: "1"
      memory: 1Gi

batch:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi

dashboard:
  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 256Mi

Evidence: unlimited p95 was 3ms and limited p95 was also 3ms, so the serving endpoint stayed stable in our test while the batch workload can be the first to throttle.