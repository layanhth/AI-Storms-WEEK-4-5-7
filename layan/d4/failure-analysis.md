# Failure Analysis

CPU-based HPA is not always a good signal for vLLM because LLM inference mainly depends on the GPU. The GPU can be overloaded while CPU usage is still low, so the HPA may scale too late.

A better signal would be GPU utilization, the number of waiting requests, or vLLM queue depth.

In our Conservative policy, the HPA target was 70% CPU with a maximum of 3 replicas. During the load test, CPU increased above the target and the HPA scaled from 1 to 3 replicas. After the load ended, it scaled back down to 1 after the stabilization period.
