import requests
import time

BASE_URL = "http://127.0.0.1:5001"

languages = {
    "arabic": [
        "أنا خريج حديث ومهتم بالتحليل المالي والعمل مع البيانات.",
        "أستخدم Excel لتنظيم البيانات وتحليل النتائج المالية."
    ],

    "english": [
        "I am a recent graduate interested in financial analysis and working with data.",
        "I use Excel to organize financial data and analyze results."
    ],

    "mixed": [
        "أنا recent graduate ومهتم بمجال financial analysis والعمل مع البيانات.",
        "أستخدم Excel في تنظيم البيانات وتحليل financial results."
    ]
}

INTERVIEWS_PER_LANGUAGE = 5


successful_starts = 0
successful_answers = 0
failed_requests = 0


for language, answers in languages.items():

    print(f"\n=== {language.upper()} ===")

    for i in range(1, INTERVIEWS_PER_LANGUAGE + 1):

        session_id = f"grafana-{language}-{i}"

        start_payload = {
            "language": language,
            "job_role": "Junior Financial Analyst",
            "session_id": session_id
        }

        try:
            response = requests.post(
                f"{BASE_URL}/start",
                json=start_payload,
                timeout=120
            )

            if response.status_code == 200:
                successful_starts += 1
                print(f"Interview {i}: started")
            else:
                failed_requests += 1
                print(
                    f"Interview {i}: start failed "
                    f"({response.status_code})"
                )
                continue

        except Exception as e:
            failed_requests += 1
            print(f"Interview {i}: start error: {e}")
            continue


        for answer_number, answer in enumerate(answers, start=1):

            answer_payload = {
                "session_id": session_id,
                "answer": answer
            }

            try:
                response = requests.post(
                    f"{BASE_URL}/answer",
                    json=answer_payload,
                    timeout=120
                )

                if response.status_code == 200:
                    successful_answers += 1
                    print(
                        f"  Answer {answer_number}: success"
                    )
                else:
                    failed_requests += 1
                    print(
                        f"  Answer {answer_number}: failed "
                        f"({response.status_code})"
                    )

            except Exception as e:
                failed_requests += 1
                print(
                    f"  Answer {answer_number}: error: {e}"
                )

            time.sleep(0.2)


print("\n==============================")
print("Dashboard Data Generation Done")
print("==============================")
print(f"Successful Interviews: {successful_starts}")
print(f"Successful Answers: {successful_answers}")
print(f"Failed Requests: {failed_requests}")

