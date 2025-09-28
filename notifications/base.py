from abc import ABC, abstractmethod
from typing import Any

class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str) -> None:
        pass