from abc import ABC, abstractmethod
from typing import List
from models.data_models import TaskEntry, CategoryBatch

class BaseLoader(ABC):
    @abstractmethod
    def load(self) -> List[TaskEntry]:
        """
        Load data and return a list of TaskEntry objects.
        """
        pass

    @abstractmethod
    def load_by_category(self) -> List[CategoryBatch]:
        """Load and group data into category-aligned batches."""
        pass
