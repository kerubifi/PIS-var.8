FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pika
COPY ./src ./src
CMD ["uvicorn", "src.infrastructure.adapter.in.listing_controller:app", "--host", "0.0.0.0", "--port", "8000"]
