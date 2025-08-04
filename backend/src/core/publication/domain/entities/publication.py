from typing import List, Literal

from src.core.category.domain.entities.category import Category
from src.core.common.domain.entities.entity import Entity

PublicationFormat = Literal[
    "linkedin_post",
    "blog_post",
    "short_video",
    "long_video"
]

PublicationStage = Literal[
    "preview",
    "ready"
]


class Publication(Entity):
    title: str
    content: str
    categories: List[Category]
    outlining: List[str]
    format: PublicationFormat
    stage: PublicationStage
    thought_ids: List[str]
    user_guideline: str
