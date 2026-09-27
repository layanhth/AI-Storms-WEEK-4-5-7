import requests
import os
import re


BASE_URL="http://localhost:8001/v1"
MODEL="Qwen/Qwen3-8B-AWQ"


PROMPT_PATH=os.path.join(
    os.path.dirname(__file__),
    "..",
    "prompts",
    "arabic.txt"
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





def detect_language(text):

    arabic_count=len(
        re.findall(
            r"[\u0600-\u06FF]",
            text
        )
    )

    english_count=len(
        re.findall(
            r"[A-Za-z]",
            text
        )
    )


    if arabic_count>0 and english_count>0:
        return "mixed"

    elif arabic_count>0:
        return "arabic"

    else:
        return "english"






def language_instruction(language):

    if language=="arabic":

        return """
لغة الإجابة:

- المتقدم يجيب بالعربية.
- اسأل السؤال بالعربية فقط.
- يمكن استخدام أسماء الأدوات الإنجليزية عند الحاجة مثل Python وExcel.
- لا تنتقل للإنجليزية.
"""


    if language=="mixed":

        return """
لغة الإجابة:

- المتقدم يستخدم العربية والإنجليزية.
- اسأل سؤالًا طبيعيًا يجمع بينهما.
- لا تكتب ترجمة مزدوجة.
- استخدم المصطلحات التقنية الإنجليزية عند الحاجة.
"""


    return """
لغة الإجابة:

- المتقدم يستخدم الإنجليزية.
- اسأل باللغة الإنجليزية فقط.
"""






class ArabicInterview:


    def __init__(self,job_role,language="arabic"):

        self.job_role=job_role
        self.language=language

        self.question_count=0
        self.records=[]
        self.last_question=""




    def call_model(self,instruction,max_tokens=120):

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

                "temperature":0.1,

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






    def get_role_name(self):

        roles={

            "Junior Data Scientist":
            "عالم بيانات مبتدئ",

            "Junior Financial Analyst":
            "محلل مالي مبتدئ"

        }


        return roles.get(
            self.job_role,
            self.job_role
        )






    def start(self):

        role_name=self.get_role_name()


        return (

            "مرحبًا بك في المقابلة التجريبية لوظيفة "
            f"{role_name}. "
            "في البداية، قدم نبذة مهنية قصيرة عن نفسك واهتمامك بهذا المجال."

        )







    def ask_question(self,answer):


        if self.last_question:

            self.records.append({

                "question":self.last_question,

                "answer":answer

            })




        if self.question_count>=7:

            return self.generate_feedback()





        detected_language=detect_language(answer)



        instruction=f"""

أنت الآن تعمل كمحاور توظيف محترف.


الوظيفة:

{self.get_role_name()}


إجابة المتقدم الأخيرة:

{answer}



قواعد المقابلة:

- اسأل سؤال متابعة واحد فقط.
- اجعل السؤال مرتبطًا مباشرة بإجابة المتقدم.
- لا تفترض خبرة غير مذكورة.
- لا تخترع مشاريع أو شركات أو مسؤوليات.
- لا تغير الموضوع بدون سبب.
- إذا كانت الإجابة غير واضحة اطلب توضيحًا.
- اجعل السؤال قصيرًا واحترافيًا.
- ابقَ في دور المحاور فقط.


{language_instruction(detected_language)}


أعد السؤال فقط بدون شرح.

"""


        question=self.call_model(

            instruction,

            200

        )


        self.last_question=question

        self.question_count+=1


        return question






    def generate_feedback(self):


        transcript="\n\n".join(

            [

                f"السؤال:{x['question']}\nالإجابة:{x['answer']}"

                for x in self.records

            ]

        )



        instruction=f"""

انتهت المقابلة.


الوظيفة:

{self.get_role_name()}


إجابات المتقدم:

{transcript}



اكتب تقييم نهائي للمقابلة.


اللغة المطلوبة:

العربية.


يشمل:

- نقاط القوة
- جوانب تحتاج تحسين
- المعرفة التقنية والمهنية
- التواصل
- حل المشكلات
- ملخص نهائي


اعتمد فقط على إجابات المتقدم.

لا تضف معلومات غير موجودة.

"""


        return self.call_model(

            instruction,

            700

        )