from abc import ABC, abstractmethod
from typing import List

from backend.core.category.domain.entities.category import Category


class CategoryRepository(ABC):

    @abstractmethod
    def save(category: Category) -> None:
        pass

    @abstractmethod
    def get_by_id(id: str) -> Category:
        pass

    @abstractmethod
    def list() -> List[Category]:
        pass

    @abstractmethod
    def delete(id: str) -> None:
        pass
