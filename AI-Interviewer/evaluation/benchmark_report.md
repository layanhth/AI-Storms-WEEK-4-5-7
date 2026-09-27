# AI Interviewer Benchmark Report

## 1. Overview

This report presents the evaluation results of the AI Interviewer system.

The evaluation focuses on measuring the model's ability to generate relevant interview follow-up questions while maintaining:
- Correct language usage
- Role alignment
- Interview consistency
- Low response latency


---

## 2. Model Information

| Component | Details |
|---|---|
| Model | Qwen/Qwen3-8B-AWQ |
| Task | AI Interview Follow-up Question Generation |
| Roles Tested | Junior Data Scientist, Junior Financial Analyst |
| Supported Languages | Arabic, English, Mixed |
| Evaluation Dataset | 10 test cases |


---

## 3. Evaluation Dataset

The evaluation dataset contains interview scenarios covering:

- Technical knowledge questions
- Data analysis workflow
- Data visualization
- Power BI usage
- Python and SQL skills
- Missing data handling
- Machine learning concepts
- Language consistency testing


---

## 4. Evaluation Metrics

The system was evaluated based on:


### Question Relevance

Measures whether the generated follow-up question is related to the candidate's previous answer.

Result:

✓ Generated questions were connected to the candidate responses.


### Language Consistency

Measures whether the model follows the required interview language.

Tested languages:

- Arabic
- English
- Mixed Arabic-English

Result:

✓ The model maintained the expected language format.


### Hallucination Prevention

Measures whether the model avoids assuming unavailable candidate experience.

Result:

✓ The model generated conceptual questions when previous experience was not provided.


### Response Latency

Measures the response generation speed.

Result:

Average latency:

0.217 seconds


---

## 5. Benchmark Results

| Metric | Result |
|---|---|
| Total Test Cases | 10 |
| Model | Qwen/Qwen3-8B-AWQ |
| Average Latency | 0.217 seconds |
| Languages Tested | Arabic / English / Mixed |
| Roles Tested | Data Scientist / Financial Analyst |


---

## 6. Example Evaluation Cases

### Case 1: Data Analysis

Candidate Answer:

"سأبدأ بتنظيف البيانات ثم تحليلها باستخدام Python وPandas."

Generated Question:

"ما هي الخطوات التي تتبعها في تحليل البيانات بعد تنظيفها؟"


---

### Case 2: Power BI

Candidate Answer:

"أستخدم Power BI لإنشاء Dashboards وتحليل النتائج."

Generated Question:

"هل يمكنك توضيح كيف تستخدم شاشات التحكم في Power BI لتقديم رؤى تجارية محددة؟"


---

## 7. Conclusion

The evaluation results show that the AI Interviewer can generate relevant follow-up questions while maintaining language consistency and interview context.

The benchmark confirms the model's ability to support multilingual interview scenarios with fast response times.