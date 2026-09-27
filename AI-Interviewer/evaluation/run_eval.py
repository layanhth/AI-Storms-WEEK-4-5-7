import json
import time
import requests
import re


BASE_URL="http://localhost:8001/v1"
MODEL="Qwen/Qwen3-8B-AWQ"

DATASET="eval_dataset.json"



def clean_response(text):

    text = re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    return text.strip()





def call_model(prompt):

    start=time.time()

    response=requests.post(

        f"{BASE_URL}/chat/completions",

        json={

            "model":MODEL,

            "messages":[

                {
                    "role":"system",
                    "content":
                    "You are a professional AI interviewer."
                },

                {
                    "role":"user",
                    "content":prompt
                }

            ],

            "temperature":0.2,

            "max_tokens":150,

            "chat_template_kwargs":{
                "enable_thinking":False
            }

        }

    )


    latency=time.time()-start

    data=response.json()


    answer=data["choices"][0]["message"]["content"]


    # تنظيف <think>
    answer=clean_response(answer)


    return answer,latency






with open(DATASET,"r",encoding="utf-8") as f:

    dataset=json.load(f)



results=[]

total_latency=0



for item in dataset:


    prompt=f"""

Role:
{item['role']}

Language:
{item['language']}


Interview Question:
{item['question']}


Candidate Answer:
{item['candidate_answer']}


Expected Behavior:
{item['expected_output']}


Generate exactly ONE interviewer follow-up question.

Rules:
- Do not explain.
- Do not provide analysis.
- Return only the question.

"""



    output,latency=call_model(prompt)


    total_latency+=latency



    results.append({

        "id":item["id"],

        "generated_question":output,

        "latency":round(latency,3)

    })


    print(
        f"Case {item['id']} completed"
    )





with open(
    "evaluation_results.json",
    "w",
    encoding="utf-8"
) as f:


    json.dump(
        results,
        f,
        ensure_ascii=False,
        indent=4
    )





print("\n========= Evaluation Report =========")


print(
    "Total Cases:",
    len(dataset)
)



print(
    "Average Latency:",
    round(
        total_latency/len(dataset),
        3
    ),
    "seconds"
)



print(
    "Results saved: evaluation_results.json"
)


print("====================================")