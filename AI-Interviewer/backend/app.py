import time

from flask import Flask, request, jsonify, Response, g
from flask_cors import CORS

from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST
)

from interview.arabic import ArabicInterview
from interview.english import EnglishInterview
from interview.mixed import MixedInterview


app = Flask(__name__)
CORS(app)


sessions = {}

# Prometheus Metrics

HTTP_REQUESTS = Counter(
    "ai_interviewer_http_requests_total",
    "Total number of HTTP requests",
    ["method", "endpoint", "status"]
)

HTTP_LATENCY = Histogram(
    "ai_interviewer_http_request_duration_seconds",
    "HTTP request latency in seconds",
    ["method", "endpoint"]
)

INTERVIEWS_STARTED = Counter(
    "ai_interviewer_interviews_started_total",
    "Total number of interviews started",
    ["language"]
)

ANSWERS_RECEIVED = Counter(
    "ai_interviewer_answers_received_total",
    "Total number of interview answers received"
)


# Request timing

@app.before_request
def before_request():
    g.start_time = time.perf_counter()


@app.after_request
def after_request(response):

    if request.path != "/metrics":

        duration = time.perf_counter() - g.start_time

        HTTP_REQUESTS.labels(
            method=request.method,
            endpoint=request.path,
            status=response.status_code
        ).inc()

        HTTP_LATENCY.labels(
            method=request.method,
            endpoint=request.path
        ).observe(duration)

    return response


# Prometheus endpoint


@app.route("/metrics", methods=["GET"])
def metrics():

    return Response(
        generate_latest(),
        content_type=CONTENT_TYPE_LATEST
    )


# Start interview

@app.route("/start", methods=["POST"])
def start_interview():

    data = request.json

    language = data.get("language")
    job_role = data.get("job_role")
    session_id = data.get("session_id")


    if not job_role:

        return jsonify({
            "error": "Job role is required"
        }), 400


    if language == "arabic":

        interviewer = ArabicInterview(
            job_role,
            "arabic"
        )


    elif language == "english":

        interviewer = EnglishInterview(
            job_role,
            "english"
        )


    elif language == "mixed":

        interviewer = MixedInterview(
            job_role,
            "mixed"
        )


    else:

        return jsonify({
            "error": "Invalid language"
        }), 400


    sessions[session_id] = interviewer


    INTERVIEWS_STARTED.labels(
        language=language
    ).inc()


    return jsonify({
        "message": interviewer.start()
    })


# Answer

@app.route("/answer", methods=["POST"])
def answer():

    data = request.json

    session_id = data.get("session_id")
    answer = data.get("answer")


    interviewer = sessions.get(session_id)


    if not interviewer:

        return jsonify({
            "error": "Session not found"
        }), 404


    ANSWERS_RECEIVED.inc()


    return jsonify({
        "message": interviewer.ask_question(answer)
    })


# Run app

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )