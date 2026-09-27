# Service report

Team: khawlah
Use case: Team-served chat completions (Qwen2.5-1.5B-Instruct-AWQ) behind a Kubernetes Service
Service and model: team-serving / Qwen/Qwen2.5-1.5B-Instruct-AWQ
Measured requests or tasks: ~150 chat completion requests across 4 traffic phases
Indicator and unit: TTFT p95, seconds
SLO target and window: < 0.1s, 5-minute rolling window
Measurement start and end: 2026-09-14T08:30:00Z to 2026-09-14T08:33:00Z
Workload: traffic.py (single caller 60s, quiet 30s, four callers 60s, wait 30s)
Observed result and sample count: 0.03898s p95 over ~150 requests
Evidence: Grafana Explore query result confirmed against the same expression used in the alert rule
Conclusion: met
Limitations: Single short test workload, not sustained production traffic; SLO is met under this specific observed test, not guaranteed generally
Follow-up action: Re-measure under a longer, more representative workload before treating this SLO as a standing guarantee

## Measurement query

```
histogram_quantile(0.95, sum by (le) (rate(vllm:time_to_first_token_seconds_bucket{job="serving"}[5m]))) or histogram_quantile(0.95, sum by (le) (rate(vllm_time_to_first_token_seconds_bucket{job="serving"}[5m])))
```

Evaluated as an instant query at the end of the traffic run. Measures the 95th percentile time-to-first-token across requests scraped by Prometheus in the trailing 5-minute window, for the serving job. Excludes requests that failed before a first token streamed back, and excludes traffic to any other job.

## Service alert

Condition and unit: TTFT p95 > 0.1 seconds
Evaluation interval: 1m
Pending period: None
Relationship to the SLO: Directly tests the same indicator and threshold published as the SLO
First response to a notification: Check Grafana Explore for the current TTFT p95 trend and kubectl top pod for saturation on team-serving

## Notification test

Firing received at: 2026-09-14T08:39:00+00:00
Resolved received at: 2026-09-14T08:44:00+00:00
What the test establishes: The full alert pipeline delivers both firing and resolved notifications correctly, independent of the real service SLI
