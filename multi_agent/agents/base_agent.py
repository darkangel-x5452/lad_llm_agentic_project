from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def handle_task(self, task):
        """Receive a task and return result"""
        pass
