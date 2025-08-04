from abc import ABC, abstractmethod
from typing import List

from src.core.category.domain.entities.category import Category


class CategoryRepositoryInterface(ABC):

    @abstractmethod
    def save(category: Category) -> None:
        pass

    @abstractmethod
    def get_by_id(id: str) -> Category:
        pass

    @abstractmethod
    def get_by_name(name: str) -> Category:
        pass

    @abstractmethod
    def list() -> List[Category]:
        pass

    @abstractmethod
    def delete(id: str) -> None:
        pass
