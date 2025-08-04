from typing import List
from sqlalchemy.orm import Session

from src.core.category.domain.repositories.category_repository import CategoryRepositoryInterface
from src.core.category.domain.entities.category import Category
from src.infra.databases.relational.models import CategoryModel
from src.infra.databases.relational.session import get_db


class CategoryRepository(CategoryRepositoryInterface):

    def __init__(self, db: Session = None):
        self.db = db

    def save(self, category: Category) -> None:
        """Save a category to the database"""
        if not self.db:
            self.db = next(get_db())

        category_model = CategoryModel(
            id=category.id,
            name=category.name,
            color=category.color
        )

        self.db.add(category_model)
        self.db.commit()

    def get_by_id(self, id: str) -> Category:
        """Get a category by its ID"""
        if not self.db:
            self.db = next(get_db())

        category_model = self.db.query(CategoryModel).filter(
            CategoryModel.id == id
        ).first()

        if not category_model:
            raise ValueError(f"Category with id {id} not found")

        return Category(
            id=category_model.id,
            name=category_model.name,
            color=category_model.color
        )

    def get_by_name(self, name: str) -> Category:
        """Get a category by its name"""
        if not self.db:
            self.db = next(get_db())

        category_model = self.db.query(CategoryModel).filter(
            CategoryModel.name == name
        ).first()

        if not category_model:
            return None

        return Category(
            id=category_model.id,
            name=category_model.name,
            color=category_model.color
        )

    def list(self) -> List[Category]:
        """List all categories"""
        if not self.db:
            self.db = next(get_db())

        category_models = self.db.query(CategoryModel).all()

        return [
            Category(
                id=model.id,
                name=model.name,
                color=model.color
            )
            for model in category_models
        ]

    def delete(self, id: str) -> None:
        """Delete a category by its ID"""
        if not self.db:
            self.db = next(get_db())

        category_model = self.db.query(CategoryModel).filter(
            CategoryModel.id == id
        ).first()

        if not category_model:
            raise ValueError(f"Category with id {id} not found")

        self.db.delete(category_model)
        self.db.commit()
