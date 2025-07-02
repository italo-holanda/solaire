from typing import List, Literal

from backend.core.category.domain.entities.category import Category
from backend.core.common.domain.entities.entity import Entity

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
    id: str
    title: str
    content: str
    categories: List[Category]
    outlining: List[str]
    format: PublicationFormat
    stage: PublicationStage
    thought_ids: List[str]
