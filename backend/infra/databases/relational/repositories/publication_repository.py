from typing import List
from sqlalchemy.orm import Session

from backend.core.publication.domain.repositories.publication_repository import PublicationRepositoryInterface
from backend.core.publication.domain.entities.publication import Publication
from backend.core.category.domain.entities.category import Category
from backend.infra.databases.relational.models import PublicationModel, CategoryModel, PublicationFormatEnum, PublicationStageEnum
from backend.infra.databases.relational.session import get_db


class PublicationRepository(PublicationRepositoryInterface):

    def __init__(self, db: Session = None):
        self.db = db

    def save(self, publication: Publication) -> Publication:
        """Save a publication to the database"""
        if not self.db:
            self.db = next(get_db())

        category_models = []
        if publication.categories:
            category_models = self.db.query(CategoryModel).filter(
                CategoryModel.id.in_(
                    [cat.id for cat in publication.categories])
            ).all()

        publication_model = PublicationModel(
            id=publication.id,
            title=publication.title,
            content=publication.content,
            categories=category_models,
            outlining=publication.outlining,
            format=PublicationFormatEnum(publication.format),
            stage=PublicationStageEnum(publication.stage),
            thought_ids=publication.thought_ids,
            user_guideline=publication.user_guideline
        )

        self.db.add(publication_model)
        self.db.commit()

        # Return the saved publication
        return self.get_by_id(publication.id)

    def get_by_id(self, id: str) -> Publication:
        """Get a publication by its ID"""
        if not self.db:
            self.db = next(get_db())

        publication_model = self.db.query(PublicationModel).filter(
            PublicationModel.id == id
        ).first()

        if not publication_model:
            raise ValueError(f"Publication with id {id} not found")

        categories = [
            Category(
                id=cat.id,
                name=cat.name,
                color=cat.color
            )
            for cat in publication_model.categories
        ]

        return Publication(
            id=publication_model.id,
            title=publication_model.title,
            content=publication_model.content,
            categories=categories,
            outlining=publication_model.outlining,
            format=publication_model.format.value,
            stage=publication_model.stage.value,
            thought_ids=publication_model.thought_ids,
            user_guideline=publication_model.user_guideline
        )

    def list(self) -> List[Publication]:
        """List all publications"""
        if not self.db:
            self.db = next(get_db())

        publication_models = self.db.query(PublicationModel).all()

        publications = []
        for model in publication_models:
            categories = [
                Category(
                    id=cat.id,
                    name=cat.name,
                    color=cat.color
                )
                for cat in model.categories
            ]

            publications.append(Publication(
                id=model.id,
                title=model.title,
                content=model.content,
                categories=categories,
                outlining=model.outlining,
                format=model.format.value,
                stage=model.stage.value,
                thought_ids=model.thought_ids,
                user_guideline=model.user_guideline
            ))

        return publications

    def delete(self, id: str) -> None:
        """Delete a publication by its ID"""
        if not self.db:
            self.db = next(get_db())

        publication_model = self.db.query(PublicationModel).filter(
            PublicationModel.id == id
        ).first()

        if not publication_model:
            raise ValueError(f"Publication with id {id} not found")

        self.db.delete(publication_model)
        self.db.commit()

    def update(self, publication: Publication) -> None:
        """Update a publication"""
        if not self.db:
            self.db = next(get_db())

        publication_model = self.db.query(PublicationModel).filter(
            PublicationModel.id == publication.id
        ).first()

        if not publication_model:
            raise ValueError(f"Publication with id {publication.id} not found")

        category_models = []
        if publication.categories:
            category_models = self.db.query(CategoryModel).filter(
                CategoryModel.id.in_(
                    [cat.id for cat in publication.categories])
            ).all()

        publication_model.title = publication.title
        publication_model.content = publication.content
        publication_model.categories = category_models
        publication_model.outlining = publication.outlining
        publication_model.format = PublicationFormatEnum(publication.format)
        publication_model.stage = PublicationStageEnum(publication.stage)
        publication_model.thought_ids = publication.thought_ids
        publication_model.user_guideline = publication.user_guideline

        self.db.commit()
