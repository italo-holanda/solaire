from typing import List
from sqlalchemy.orm import Session

from backend.core.thought.domain.repositories.thought_repository import ThoughtRepositoryInterface
from backend.core.thought.domain.entities.thought import Thought
from backend.core.category.domain.entities.category import Category
from backend.infra.databases.relational.models import ThoughtModel, CategoryModel
from backend.infra.databases.relational.session import get_db


class ThoughtRepository(ThoughtRepositoryInterface):

    def __init__(self, db: Session = None):
        self.db = db

    def save(self, thought: Thought) -> None:
        """Save a thought to the database"""
        if not self.db:
            self.db = next(get_db())

        category_models = []
        if thought.categories:
            category_models = self.db.query(CategoryModel).filter(
                CategoryModel.id.in_([cat.id for cat in thought.categories])
            ).all()

        thought_model = ThoughtModel(
            id=thought.id,
            title=thought.title,
            summary=thought.summary,
            text=thought.text,
            categories=category_models
        )

        self.db.add(thought_model)
        self.db.commit()

    def get_by_id(self, id: str) -> Thought:
        """Get a thought by its ID"""
        if not self.db:
            self.db = next(get_db())

        thought_model = self.db.query(ThoughtModel).filter(
            ThoughtModel.id == id
        ).first()

        if not thought_model:
            return None

        categories = [
            Category(
                id=cat.id,
                name=cat.name,
                color=cat.color
            )
            for cat in thought_model.categories
        ]

        return Thought(
            id=thought_model.id,
            title=thought_model.title,
            summary=thought_model.summary,
            text=thought_model.text,
            categories=categories,
            embeddings=[]
        )

    def list(self) -> List[Thought]:
        """List all thoughts"""
        if not self.db:
            self.db = next(get_db())

        thought_models = self.db.query(ThoughtModel).all()

        thoughts = []
        for model in thought_models:

            categories = [
                Category(
                    id=cat.id,
                    name=cat.name,
                    color=cat.color
                )
                for cat in model.categories
            ]

            thoughts.append(Thought(
                id=model.id,
                title=model.title,
                summary=model.summary,
                text=model.text,
                categories=categories,
                embeddings=[]
            ))

        return thoughts

    def delete(self, id: str) -> None:
        """Delete a thought by its ID"""
        if not self.db:
            self.db = next(get_db())

        thought_model = self.db.query(ThoughtModel).filter(
            ThoughtModel.id == id
        ).first()

        if thought_model:
            self.db.delete(thought_model)
            self.db.commit()

    def update(self, thought: Thought) -> None:
        if not self.db:
            self.db = next(get_db())

        thought_model = self.db.query(ThoughtModel).filter(
            ThoughtModel.id == thought.id
        ).first()

        if not thought_model:
            return

        thought_model.text = thought.text
        thought_model.summary = thought.summary
        thought_model.title = thought.title

        category_models = []
        if thought.categories:
            category_models = self.db.query(CategoryModel).filter(
                CategoryModel.id.in_([cat.id for cat in thought.categories])
            ).all()
        thought_model.categories = category_models

        self.db.commit()
