from abc import ABC, abstractmethod
from typing import List, Optional

class Repository(ABC):
    @abstractmethod
    def get(self, id: int) -> Optional[object]:
        pass

    @abstractmethod
    def add(self, entity: object) -> None:
        pass

    @abstractmethod
    def update(self, entity: object) -> None:
        pass

    @abstractmethod
    def delete(self, id: int) -> None:
        pass

    @abstractmethod
    def list_all(self) -> List[object]:
        pass
