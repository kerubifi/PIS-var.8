FROM python:3.10-slim
WORKDIR /app
RUN pip install fastapi uvicorn pika
COPY ./src ./src
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
