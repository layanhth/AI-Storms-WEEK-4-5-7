import requests
import os
import re


BASE_URL="http://localhost:8001/v1"
MODEL="Qwen/Qwen3-8B-AWQ"


PROMPT_PATH=os.path.join(
    os.path.dirname(__file__),
    "..",
    "prompts",
    "mixed.txt"
)


with open(PROMPT_PATH,"r",encoding="utf-8") as f:
    SYSTEM_PROMPT=f.read()



def clean_response(text):

    text=re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    return text.strip()






class MixedInterview:



    def __init__(self,job_role,language="mixed"):


        self.job_role=job_role

        self.language=language

        self.question_count=0

        self.records=[]

        self.last_question=""

        self.previous_questions=[]

        self.previous_topics=[]


        self.topics=[

            "Background and motivation",

            "Role-specific knowledge",

            "Technical or professional skills",

            "Practical work scenario",

            "Problem-solving",

            "Behavioral and teamwork",

            "Role-specific decision-making scenario"

        ]






    def call_model(self,instruction,max_tokens=200):


        response=requests.post(

            f"{BASE_URL}/chat/completions",

            json={

                "model":MODEL,


                "messages":[

                    {

                        "role":"system",

                        "content":SYSTEM_PROMPT

                    },

                    {

                        "role":"user",

                        "content":instruction

                    }

                ],


                "temperature":0.2,


                "max_tokens":max_tokens,


                "chat_template_kwargs":{

                    "enable_thinking":False

                }

            },


            timeout=120

        )


        response.raise_for_status()


        reply=response.json()["choices"][0]["message"]["content"]


        return clean_response(reply)







    def start(self):


        return (

            "مرحبًا بك في المقابلة التجريبية لوظيفة "

            f"{self.job_role}. "

            "قبل أن نبدأ، قدم نبذة مهنية قصيرة عن نفسك واهتمامك بهذا المجال."

        )









    def ask_question(self,answer):


        if self.last_question:


            self.records.append({

                "question":self.last_question,

                "answer":answer

            })





        if self.question_count>=7:


            return self.generate_feedback()





        current_topic=self.topics[
            self.question_count
        ]



        previous_questions=" | ".join(
            self.previous_questions
        ) if self.previous_questions else "None"




        previous_topics=" | ".join(
            self.previous_topics
        ) if self.previous_topics else "None"






        instruction=f"""


أنت الآن تعمل كمحاور توظيف محترف.


الوظيفة:

{self.job_role}



إجابة المتقدم الأخيرة:

{answer}



المجال الحالي للمقابلة:

{current_topic}



المجالات السابقة:

{previous_topics}



الأسئلة السابقة:

{previous_questions}




قواعد اللغة:

- العربية هي اللغة الأساسية.
- استخدم English technical terms فقط عند الحاجة.
- لا تكتب ترجمة للسؤال.
- اجعل السؤال طبيعيًا وليس خليطًا مصطنعًا.



قواعد المقابلة:

- اسأل سؤالًا واحدًا فقط.
- اجعل السؤال مرتبطًا بإجابة المتقدم.
- لا تكرر سؤالًا سابقًا.
- لا تفترض خبرة غير مذكورة.
- لا تخترع مشاريع أو وظائف أو مسؤوليات.
- إذا لم توجد معلومات كافية، اسأل سؤال توضيحي بسيط.
- لا تقدم تقييمًا أو Feedback.
- لا تشرح.
- أخرج السؤال فقط.

"""



        question=self.call_model(

            instruction,

            200

        )



        self.last_question=question


        self.previous_questions.append(
            question
        )


        self.previous_topics.append(
            current_topic
        )


        self.question_count+=1



        return question








    def generate_feedback(self):


        transcript="\n\n".join(

            [

                f"السؤال: {x['question']}\nالإجابة: {x['answer']}"

                for x in self.records

            ]

        )





        instruction=f"""


انتهت المقابلة.


الوظيفة:

{self.job_role}



إجابات المتقدم:

{transcript}




اكتب Feedback نهائي.



القواعد:

- اللغة الأساسية: العربية.
- استخدم English technical terms فقط عند الحاجة.
- لا تخاطب المتقدم مباشرة.
- لا تخترع مهارات أو خبرات غير مذكورة.
- اعتمد فقط على إجابات المقابلة.



استخدم هذا الشكل:


نقاط القوة:

...


جوانب تحتاج إلى التحسين:

...


المعرفة التقنية أو المهنية:

...


التواصل:

...


حل المشكلات:

...


ملخص:

...

"""



        return self.call_model(

            instruction,

            700

        )