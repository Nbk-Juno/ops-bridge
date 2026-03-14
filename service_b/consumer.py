from dotenv import load_dotenv
from database import engine
from models import AuditLog
from sqlalchemy.orm import Session
import pika
import json
import os

load_dotenv()


def on_message(channel, method_frame, header_frame, body):
    data = json.loads(body)
    event_type = data["event_type"]
    asset_payload = data["payload"]
    asset_id = asset_payload["id"]
    with Session(engine) as session:
        new_log = AuditLog(
            asset_id=asset_id,
            event_type=event_type,
            payload=asset_payload,
        )

        session.add(new_log)
        session.commit()

    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def main():
    RABBITMQ_URL = os.environ.get("RABBITMQ_URL")
    assert RABBITMQ_URL is not None, "RABBITMQ_URL is not set in .env"
    parameters = pika.URLParameters(RABBITMQ_URL)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    channel.queue_declare("asset_events")
    channel.basic_consume("asset_events", on_message)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()


if __name__ == "__main__":
    main()

