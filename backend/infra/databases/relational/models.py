import uuid
import enum
import json

from typing import List

from sqlalchemy import (
    Column,
    String,
    Table,
    ForeignKey,
    Text,
    Enum,
    DateTime,
    TypeDecorator,
    func
)

from sqlalchemy.orm import (
    relationship,
    Mapped,
    mapped_column,
    DeclarativeBase
)


class Base(DeclarativeBase):
    pass


thought_category_association = Table(
    "thought_category",
    Base.metadata,

    Column(
        "thought_id",
        String(length=36),
        ForeignKey("thoughts.id"),
        primary_key=True
    ),

    Column(
        "category_id",
        String(length=36),
        ForeignKey("categories.id"),
        primary_key=True
    ),
)

publication_category_association = Table(
    "publication_category",
    Base.metadata,

    Column(
        "publication_id",
        String(length=36),
        ForeignKey("publications.id"),
        primary_key=True
    ),

    Column(
        "category_id",
        String(length=36),
        ForeignKey("categories.id"),
        primary_key=True
    ),
)


class PublicationFormatEnum(str, enum.Enum):
    linkedin_post = "linkedin_post"
    blog_post = "blog_post"
    short_video = "short_video"
    long_video = "long_video"


class PublicationStageEnum(str, enum.Enum):
    preview = "preview"
    ready = "ready"


class JSONList(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return "[]"
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        if not value:
            return []
        return json.loads(value)


class CategoryModel(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    name: Mapped[str] = mapped_column(String, nullable=False)
    color: Mapped[str] = mapped_column(String, nullable=True)

    thoughts: Mapped[List["ThoughtModel"]] = relationship(
        "ThoughtModel",
        secondary=thought_category_association,
        back_populates="categories",
        lazy="joined",
    )
    publications: Mapped[List["PublicationModel"]] = relationship(
        "PublicationModel",
        secondary=publication_category_association,
        back_populates="categories",
        lazy="joined",
    )


class ThoughtModel(Base):
    __tablename__ = "thoughts"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    title: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)

    categories: Mapped[List[CategoryModel]] = relationship(
        "CategoryModel",
        secondary=thought_category_association,
        back_populates="thoughts",
        lazy="joined",
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )


class PublicationModel(Base):
    __tablename__ = "publications"

    id: Mapped[str] = mapped_column(
        String(length=36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    title: Mapped[str] = mapped_column(String, nullable=False)

    content: Mapped[str] = mapped_column(Text, nullable=False)

    categories: Mapped[List[CategoryModel]] = relationship(
        "CategoryModel",
        secondary=publication_category_association,
        back_populates="publications",
        lazy="joined",
    )

    outlining: Mapped[List[str]] = mapped_column(
        JSONList,
        nullable=False,
        default=list
    )

    format: Mapped[PublicationFormatEnum] = mapped_column(
        Enum(PublicationFormatEnum),
        nullable=False
    )

    stage: Mapped[PublicationStageEnum] = mapped_column(
        Enum(PublicationStageEnum),
        nullable=False
    )

    thought_ids: Mapped[List[str]] = mapped_column(
        JSONList,
        nullable=False,
        default=list
    )

    user_guideline: Mapped[str] = mapped_column(Text, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    deleted_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
