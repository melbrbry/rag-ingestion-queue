import json
import boto3
from typing import Iterable

from app.domain.queue.base import QueueClient, QueueMessage


class SQSQueueClient(QueueClient):
    """
    AWS SQS implementation of the QueueClient interface.
    """

    def __init__(self, queue_url: str):
        """
        Initialize SQS client.
        
        Args:
            queue_url: The URL of the SQS queue
        """
        self.queue_url = queue_url
        self._client = boto3.client("sqs")

    def send(self, message: QueueMessage) -> None:
        """
        Send a message to the SQS queue.
        """
        self._client.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message)
        )

    def receive(self, max_messages: int = 1) -> Iterable[QueueMessage]:
        """
        Receive messages from the SQS queue.
        
        Args:
            max_messages: Maximum number of messages to receive (1-10 for SQS)
        
        Yields:
            QueueMessage containing body and receipt_handle for deletion
        """
        # SQS allows max 10 messages per receive call
        max_messages = min(max_messages, 10)
        
        response = self._client.receive_message(
            QueueUrl=self.queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=5  # Long polling for efficiency
        )
        
        messages = response.get("Messages", [])
        
        for msg in messages:
            yield {
                "body": json.loads(msg["Body"]),
                "receipt_handle": msg["ReceiptHandle"]
            }

    def delete(self, message: QueueMessage) -> None:
        """
        Delete a message from the SQS queue after processing.
        
        Args:
            message: The message containing receipt_handle to delete
        """
        self._client.delete_message(
            QueueUrl=self.queue_url,
            ReceiptHandle=message["receipt_handle"]
        )

