import os
import re
from openai import OpenAI


BASE_URL="http://127.0.0.1:8001/v1"

MODEL="Qwen/Qwen3-8B-AWQ"


PROMPT_PATH=os.path.join(
    os.path.dirname(__file__),
    "..",
    "prompts",
    "english.txt"
)


with open(PROMPT_PATH,encoding="utf-8") as f:
    SYSTEM_PROMPT=f.read()



client=OpenAI(
    base_url=BASE_URL,
    api_key="not-needed"
)





def clean_response(text):

    text=re.sub(
        r"<think>.*?</think>",
        "",
        text,
        flags=re.DOTALL
    )

    return text.strip()






class EnglishInterview:


    def __init__(self,job_role,language="english"):

        self.job_role=job_role

        self.language=language

        self.question_count=0

        self.records=[]

        self.last_question=""

        self.previous_experience_status="UNKNOWN"








    def detect_experience(self,answer):


        keywords=[

            "project",
            "internship",
            "worked",
            "developed",
            "created",
            "built",
            "experience",
            "job",
            "task",
            "training"

        ]


        answer_lower=answer.lower()


        for word in keywords:

            if word in answer_lower:

                return "KNOWN"


        return "UNKNOWN"








    def call_model(self,instruction,max_tokens=120):


        response=client.chat.completions.create(

            model=MODEL,

            messages=[

                {
                    "role":"system",
                    "content":SYSTEM_PROMPT
                },

                {
                    "role":"user",
                    "content":instruction
                }

            ],

            temperature=0.2,

            max_tokens=max_tokens,

            extra_body={

                "chat_template_kwargs":{

                    "enable_thinking":False

                }

            }

        )


        reply=response.choices[0].message.content


        return clean_response(reply)










    def start(self):


        return (

            "Welcome to the AI interview for "

            f"{self.job_role}. "

            "Please introduce yourself and explain your interest in this field."

        )











    def ask_question(self,answer):


        if self.last_question:


            self.records.append({

                "question":self.last_question,

                "answer":answer

            })




        self.previous_experience_status = (
            self.detect_experience(answer)
        )




        if self.question_count>=7:

            return self.generate_feedback()





        runtime_instruction=""



        if self.previous_experience_status=="UNKNOWN":


            runtime_instruction="""

The candidate has not explicitly described previous experience.

Ask ONE conceptual or hypothetical follow-up question.

Do NOT ask about:
- previous projects
- previous jobs
- internships
- tasks completed
- tools they used

unless the candidate already mentioned them.

"""


        else:


            runtime_instruction="""

The candidate explicitly mentioned previous experience.

Ask ONE follow-up question related to the specific experience mentioned.

Do not invent additional details.

"""







        instruction=f"""

You are a professional AI interviewer.


Role:

{self.job_role}



Previous interviewer question:

{self.last_question}



Candidate answer:

{answer}



Interview rules:

- Ask exactly ONE follow-up question.
- Base the question on the candidate's latest answer.
- Keep it relevant to the role.
- Do not evaluate the candidate.
- Do not praise the answer.
- Do not explain.
- Output only the next interview question.


{runtime_instruction}

"""



        question=self.call_model(

            instruction,

            120

        )



        self.last_question=question

        self.question_count+=1



        return question







    def generate_feedback(self):


        transcript="\n\n".join(

            [

                f"Question: {x['question']}\nAnswer: {x['answer']}"

                for x in self.records

            ]

        )



        instruction=f"""


The interview has ended.


Role:

{self.job_role}



Candidate answers:

{transcript}



Provide final interview feedback in English.



Include:

- Strengths
- Areas for Improvement
- Technical & Professional Knowledge
- Communication
- Problem Solving
- Summary



Rules:

- Evaluate only based on the answers.
- Do not invent experience.
- Do not add information that was not mentioned.

"""


        return self.call_model(

            instruction,

            700

        )