from abc import ABC, abstractmethod
from typing import List
from models.data_models import TaskEntry

class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> List[TaskEntry]:
        """
        Load data and return a list of TaskEntry objects.
        """
        pass
