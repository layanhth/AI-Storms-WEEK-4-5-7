# Size a Saudi Data Centre

## Site
HUMAIN's first building: 50 MW, announced with about 18,000 NVIDIA GB300 GPUs.

## Given Values
- PUE: 1.25
- 10% of IT power for switches and storage
- 20% headroom
- GB300 NVL72 rack: 72 GPUs, ~20 TB, ~120 kW
- Serving rate: 125 output tokens/s/GPU
- Average site draw: 65%
- Electricity: $0.08/kWh
- Non-electricity cost: $450,000 per MW per month
- Training: 6 ops/parameter/token, 20 tokens/parameter, 40% peak
- H100 peak: 989 TFLOPS

## 1. Racks and GPUs

50 MW / 1.25 = 40 MW IT

40 MW x 0.90 x 0.80 = 28.8 MW compute

28,800 kW / 120 kW = 240 racks

240 x 72 = 17,280 GPUs

**Answer: 240 racks and 17,280 GPUs.**

## 2. Largest Open Model Served

The largest open model in the provided material is Kimi K2 (~1T parameters).

Using ~1 TB for FP8 weights and ~0.3 TB as the context allowance:

~1.3 TB per serving copy.

20 TB / 1.3 TB ≈ 15 copies per rack.

15 x 240 ≈ 3,600 copies.

**Answer: Kimi K2, approximately 3,600 copies.**

## 3. Largest Model Trained in Six Months

Total compute:

17,280 x 989e12 x 0.40 x 15.8e6 ≈ 1.08e26 operations

Training compute = 6 x N x 20N = 120N^2

N = sqrt(1.08e26 / 120) ≈ 9.49e11 parameters

**Answer: approximately 949B parameters.**

## 4. Monthly Electricity Bill

Average draw:

50 MW x 0.65 = 32.5 MW

Assuming a 30-day month:

32.5 MW x 720 hours = 23.4 million kWh

23.4M x $0.08 = $1.872M

**Answer: approximately $1.87 million per month.**

At the $0.048/kWh industrial rate, the bill would be approximately $1.12 million/month.

## 5. Cost per Million Tokens

Non-electricity cost:

50 x $450,000 = $22.5M/month

Total monthly cost:

$22.5M + $1.872M = $24.372M

Full token capacity:

17,280 x 125 x 2,592,000 = 5.599 trillion tokens/month

At 30% capacity sold:

Cost ≈ **$14.51 per 1M tokens**

At 80% capacity sold:

Cost ≈ **$5.44 per 1M tokens**


