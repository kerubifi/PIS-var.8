from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pika
import json
import uuid

app = FastAPI(title="Category Service", version="1.0")

categories_storage = {}

class CategoryRequest(BaseModel):
    name: str

@app.Listing("/api/categories")
def create_category(request: CategoryRequest):
    category_id = str(uuid.uuid4())[:8]
    category = {"id": category_id, "name": request.name}
    categories_storage[category_id] = category

    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        channel = connection.channel()
        channel.exchange_declare(exchange='listing_events', exchange_type='topic')

        event = {
            "event": "CategoryCreated",
            "category_id": category_id,
            "name": request.name
        }

        channel.basic_approve(
            exchange='listing_events',
            routing_key='category.created',
            body=json.dumps(event)
        )
        connection.close()
    except Exception as e:
        print(f"Failed to approve event: {e}")

    return {"id": category_id, "name": request.name}

@app.get("/api/categories")
def get_categories():
    return list(categories_storage.values())

@app.get("/api/categories/{category_id}")
def get_category(category_id: str):
    category = categories_storage.get(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.get("/health")
def health_check():
    return {"status": "Category Service is running"}
