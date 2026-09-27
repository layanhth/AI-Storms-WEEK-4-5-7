# Integration note: AI storms (v1, go-live)

Copy this file, fill every angle bracket, and hand it to your paired Agentic AI
team. It is Part A of the cross-cohort runbook
(`../../../week-06-capstone/cross-cohort-runbook.md`); the full operating rules
for the window live there.

- **base_url** (client form, ends in `/v1` - paste into an OpenAI client):
  `https://t15.aidc.nadir.sh/v1`

- **service root** (no `/v1` - the runbook's triage curls and `verify.sh`
  build paths from this):
  `https://t15.aidc.nadir.sh`

- **model id:** `Qwen/Qwen2.5-1.5B-Instruct-AWQ`

- **auth:** bearer key, handed over by DM to their on-call, never in this file

- **modalities:** text in, text out, tool calls per the OpenAI schema. Text only.

- **example call:**
  ```bash
  curl -s https://t15.aidc.nadir.sh/v1/chat/completions \
    -H "Authorization: Bearer REDACTED" \
    -H 'Content-Type: application/json' \
    -d '{"model":"Qwen/Qwen2.5-1.5B-Instruct-AWQ","messages":[{"role":"user","content":"hello from outside"}]}'

- **SLOs we publish:**  availability 95% over the window · TTFT p95 under 500 ms (tier 1) · error rate under 2%
- **limits, declared honestly:** max model context length 4096 tokens · concurrency knee ~16
- **on-call:**  Layan · Discord · response within 30 minutes during the window
