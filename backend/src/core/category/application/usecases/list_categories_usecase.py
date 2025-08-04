from typing import List

from src.core.category.domain.entities.category import Category
from src.core.category.domain.repositories.category_repository import CategoryRepositoryInterface


class ListCategoriesUsecase:
    def __init__(
        self,
        category_repository: CategoryRepositoryInterface
    ):
        self.category_repository = category_repository

    def execute(self) -> List[Category]:
        return self.category_repository.list()
