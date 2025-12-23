import pika
from app.domain.queue.base import QueueClient, QueueMessage
import json

class RabbitMQQueueClient(QueueClient):

    def __init__(self, connection_string, queue_name: str):
        self.connection_string = connection_string
        self.queue_name = queue_name

        self._connect()

    def _connect(self):
        self._connection = pika.BlockingConnection(pika.URLParameters(self.connection_string))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.queue_name, durable=True)
        self._channel.basic_qos(prefetch_count=1)

    def send(self, message: QueueMessage) -> None:
        self._channel.basic_publish(
            exchange="",
            routing_key=self.queue_name,
            body=json.dumps(message)
        )

    def receive(self, max_messages: int = 1):
        for method, _, body in self._channel.consume(
            queue=self.queue_name,
            inactivity_timeout=1
        ):
            if method:
                yield {
                    "body": json.loads(body),
                    "delivery_tag": method.delivery_tag
                }

    def delete(self, message: QueueMessage) -> None:
        self._channel.basic_ack(
            delivery_tag=message["delivery_tag"]
        )