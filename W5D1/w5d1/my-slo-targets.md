# Service indicators and proposed targets

Team: Team 15
Use case: Baseline bilingual chat model service for enterprise AI workloads
Service measured: Qwen/Qwen2.5-1.5B-Instruct-AWQ, /v1/chat/completions, namespace team; baseline engine
Workload: 120 requests; one caller for 60 seconds, 30-second quiet period, up to four callers for 60 seconds; max_tokens=64
Measurement period: 2026-09-13 08:36:11 UTC to 2026-09-13 08:39:11 UTC
Instrumentation gaps: HTTP request-success percentage and output quality are not measured by these vLLM metrics

## SLI 1

Indicator: p95 time to first token
Panel: TTFT p95 (5m)
Unit: seconds
Target: < 0.1 seconds (provisional SLO)
Window: 5 minutes
Observed: 0.039 seconds under the recorded 120-request lab workload
Evidence: Grafana Team service dashboard, measured during 2026-09-13 08:36:11 UTC to 08:39:11 UTC
Why it fits: Time to first token directly affects how quickly a user feels the chat service responds
Limitations: Short lab workload only; the target needs retesting with longer runs, higher concurrency and representative production traffic

## SLI 2

Indicator: completed requests per minute
Panel: Completed requests / min (5m)
Unit: requests/min
Target: >= 20 requests/min (provisional operating target)
Window: 5 minutes
Observed: 24.8 requests/min during the active traffic period
Evidence: Grafana Team service dashboard, measured during 2026-09-13 08:36:11 UTC to 08:39:11 UTC
Why it fits: Completed requests per minute shows whether the service can sustain useful request throughput under load
Limitations: Completion does not prove response quality or HTTP success rate; this target needs retesting with longer and more representative workloads
