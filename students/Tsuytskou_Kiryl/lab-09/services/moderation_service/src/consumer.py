import pika
import json

def on_listing_created(ch, method, properties, body):
    data = json.loads(body)
    print(f"[МОДЕРАЦИЯ] Новое объявление на проверку: {data['listing_id']} - {data['title']}")

def on_listing_approved(ch, method, properties, body):
    data = json.loads(body)
    print(f"[МОДЕРАЦИЯ] Объявление {data['listing_id']} ОДОБРЕНО")

def on_listing_rejected(ch, method, properties, body):
    data = json.loads(body)
    print(f"[МОДЕРАЦИЯ] Объявление {data['listing_id']} ОТКЛОНЕНО")

def on_category_created(ch, method, properties, body):
    data = json.loads(body)
    print(f"[МОДЕРАЦИЯ] Создана новая категория: {data['name']}")

connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.exchange_declare(exchange='listing_events', exchange_type='topic')

result = channel.queue_declare(queue='moderation_queue', durable=True)
queue_name = result.method.queue

channel.queue_bind(exchange='listing_events', queue=queue_name, routing_key='listing.created')
channel.queue_bind(exchange='listing_events', queue=queue_name, routing_key='listing.approved')
channel.queue_bind(exchange='listing_events', queue=queue_name, routing_key='listing.rejected')
channel.queue_bind(exchange='listing_events', queue=queue_name, routing_key='category.created')

channel.basic_consume(queue=queue_name, on_message_callback=on_listing_created, auto_ack=True)

print(" [*] Moderation Service ждет событий...")
channel.start_consuming()
