import pika
from app.config import settings
from dotenv import load_dotenv
import os
import json
import logging


logger = logging.getLogger(__name__)
load_dotenv()
TEST_RABBITMQ_URL = os.environ.get("TEST_RABBITMQ_URL")


def publish_event(event_type: str, payload: dict, url: str = settings.rabbitmq_url):
    try:
        parameters = pika.URLParameters(url)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()

        channel.queue_declare(queue="asset_events")

        channel.basic_publish(
            "",
            "asset_events",
            json.dumps({"event_type": event_type, "payload": payload}),
            pika.BasicProperties(
                content_type="text/plain", delivery_mode=pika.DeliveryMode.Transient
            ),
        )
        connection.close()
    except Exception as e:
        logger.warning(f"Failed to publish event '{event_type}': {e}")
