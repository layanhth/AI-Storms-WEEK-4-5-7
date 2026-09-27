# AI Interviewer

## Overview

AI Interviewer is an AI-powered mock interview system that conducts role-based interviews using the Qwen3-8B-AWQ model.

The system supports:

- Arabic interviews
- English interviews
- Mixed Arabic-English interviews

Supported roles:

- Junior Data Scientist
- Junior Financial Analyst

---

# System Architecture

Frontend (HTML / CSS / JavaScript)  
↓  
Flask Backend API  
↓  
Qwen3-8B-AWQ Model  


The system includes:

- Frontend interface for user interaction
- Flask backend for managing interview sessions
- AI model service for generating questions and feedback
- Evaluation pipeline for measuring model performance

---

# Project Structure

```
AI-Interviewer-Final/

backend/
├── app.py
├── interview/
├── prompts/
└── Dockerfile

frontend/
├── index.html
├── app.js
├── style.css
└── Dockerfile

evaluation/
├── eval_dataset.json
├── golden_dataset.json
├── evaluation_results.json
└── run_eval.py

docker-compose.yml
prom-config-ai-interviewer.yaml
README.md
```

---

# Requirements

Required software:

- Docker
- Docker Compose
- Python 3.10+


AI Model:

Qwen/Qwen3-8B-AWQ

---

# Deployment Setup

The system is deployed using Docker containers.

## Frontend Container

Responsible for:

- User interface
- Language selection
- Interview interaction

Technology:

- Nginx
- HTML
- CSS
- JavaScript

## Backend Container

Responsible for:

- Managing interview sessions
- Handling API requests
- Generating interview questions
- Generating final feedback

Technology:

- Python
- Flask

## AI Model Service

Responsible for:

- Generating interview questions
- Evaluating candidate responses
- Producing final feedback

Model:

Qwen3-8B-AWQ

---

# Running the System

## 1. Start AI Model Server

Ensure the Qwen model server is running:

localhost:8001

## 2. Start Application Using Docker

From the project root directory:

```bash
docker compose up --build
```

After successful deployment:

Frontend:

Port 3000

Backend:

Port 5000

## 3. Stop Application

To stop all containers:

```bash
docker compose down
```

---

# Local Running Without Docker

## Start Backend

```bash
cd backend
python3 app.py
```
Backend runs on:

localhost:5000

## Start Frontend

```bash
cd frontend
python3 -m http.server 3000
```
Frontend runs on:

localhost:3000

---

# System Workflow

1. User selects interview language.
2. User selects job role.
3. Backend creates an interview session.
4. AI generates follow-up questions based on candidate answers.
5. AI generates final interview feedback.

---

# API Endpoints

## Start Interview

Endpoint:

POST /start

Example request:

{
  "language": "arabic",
  "job_role": "Junior Data Scientist",
  "session_id": "example"
}

## Submit Answer

Endpoint:

POST /answer

Example request:

{
  "session_id": "example",
  "answer": "candidate answer"
}

---

# Evaluation

The model was evaluated using:

- Evaluation dataset
- Golden dataset
- Benchmark testing

Evaluation files:

evaluation/

- eval_dataset.json
- golden_dataset.json
- evaluation_results.json
- run_eval.py

Evaluation covers:

- Follow-up question relevance
- Language consistency
- Role alignment
- Response latency

---

# Benchmark Results

The model was benchmarked using the evaluation dataset.

Measured metrics:

- Number of test cases
- Response latency
- Generated question quality

Example:

Total Cases: 10

Average Latency: 0.217 seconds

Results:

evaluation/evaluation_results.json

---

# Monitoring

The backend provides Prometheus metrics through:

/metrics

Collected metrics:

- HTTP request count
- Request latency
- Interview sessions started
- Answers received

Monitoring configuration:

prom-config-ai-interviewer.yaml

---

# Deployment Verification

The deployment was verified by:

- Successfully building Docker images
- Running frontend container
- Running backend container
- Accessing the web interface
- Completing a full AI interview session

Running services:

- ai-interviewer-frontend
- ai-interviewer-backend
- Qwen model server

---

# Future Improvements

Possible improvements:

- Voice interview support
- Resume analysis
- More job roles
- Advanced monitoring dashboard
- Cloud deployment

---

# Final Deliverable

AI Interviewer provides a complete AI interview pipeline:

Frontend  
↓  
Backend API  
↓  
AI Model  
↓  
Interview Questions  
↓  
Candidate Feedback