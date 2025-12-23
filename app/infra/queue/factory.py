from app.infra.queue.rabbitmq import RabbitMQQueueClient
from app.domain.queue.base import QueueClient

class QueueFactory:

    def __init__(self):
        self.queue_client = None
    
    def get_queue(self, backend:str, config:dict) -> QueueClient:
        if not self.queue_client:
            if backend == "rabbitmq":
                self.queue_client = RabbitMQQueueClient(**config)
            else:
                raise ValueError("Unsupported queue backend")
        return self.queue_client