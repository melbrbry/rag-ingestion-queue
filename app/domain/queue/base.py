from abc import ABC, abstractmethod
from typing import Dict, Any, Iterable

class QueueMessage(Dict[str, Any]):
    pass


class QueueClient(ABC):


    @abstractmethod
    def send(self, message: QueueMessage) -> None:
        pass

    @abstractmethod
    def receive(self, max_messages: int = 1) -> Iterable[QueueMessage]:
        pass

    @abstractmethod
    def delete(self, message: QueueMessage) -> None:
        pass
