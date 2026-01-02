from app.infra.queue.rabbitmq import RabbitMQQueueClient
from app.infra.queue.sqs import SQSQueueClient
from app.domain.queue.base import QueueClient


class QueueFactory:

    def __init__(self):
        self.queue_client = None
    
    def get_queue(self, backend: str, config: dict) -> QueueClient:
        if not self.queue_client:
            if backend == "rabbitmq":
                self.queue_client = RabbitMQQueueClient(**config)
            elif backend == "sqs":
                self.queue_client = SQSQueueClient(**config)
            else:
                raise ValueError(f"Unsupported queue backend: {backend}")
        return self.queue_client