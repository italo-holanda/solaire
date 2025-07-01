from backend.core.domain.entities.entity import Entity


class Category(Entity):
    id: str
    name: str
    color: str
