FROM python:3.11-slim

WORKDIR /app

COPY . .

RUN pip install flask flask-cors prometheus-client requests openai

EXPOSE 5000

CMD ["python3", "app.py"]