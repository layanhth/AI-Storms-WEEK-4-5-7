# HPA Failure Analysis

## 1. Where CPU-based HPA fails for a real GPU inference engine

CPU utilization is not always the best scaling signal for a GPU-based vLLM inference server.

During the load test, the vLLM pod used about 1431m CPU, while the GPU reached about 77% utilization and used about 41877 MiB of 49140 MiB GPU memory.

The main inference work is happening on the GPU, so CPU utilization does not directly represent GPU pressure, request queueing, or KV-cache pressure. A CPU-based HPA can therefore scale too late, too early, or not at all even when the GPU is becoming saturated.

## 2. Better scaling signal

A better signal would be the number of waiting or in-flight requests, for example:

- vllm_num_requests_waiting
- in-flight request count
- KV-cache utilization

These metrics are more closely related to real inference pressure.

If requests are waiting, it means the current replica cannot process incoming traffic fast enough. KV-cache utilization can also show when the inference engine is approaching memory pressure and has less capacity for additional requests.

## 3. Starting target and tuning

I would start with vllm_num_requests_waiting as the autoscaling metric.

A starting target could be approximately 2 waiting requests per pod.

If the queue regularly stays above this value, the system should add replicas. If replicas scale too aggressively, the target can be increased. If users experience high latency before scaling starts, the target can be lowered.

The target should be tuned using real request latency, request rate, GPU utilization, and queue length under representative production traffic.
