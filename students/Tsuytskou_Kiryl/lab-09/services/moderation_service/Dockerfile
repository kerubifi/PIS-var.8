FROM python:3.10-slim
WORKDIR /app
RUN pip install pika
COPY ./src ./src
CMD ["python", "src/consumer.py"]
