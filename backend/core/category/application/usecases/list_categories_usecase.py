from typing import List

from backend.core.category.domain.entities.category import Category
from backend.core.category.domain.repositories.category_repository import CategoryRepository


class ListCategoriesUsecase:
    def __init__(
        self,
        category_repository: CategoryRepository
    ):
        self.category_repository = category_repository

    def execute(self) -> List[Category]:
        return self.category_repository.list()
