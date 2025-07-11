from backend.infra.databases.relational.engine import engine
from backend.infra.databases.relational.models import Base

Base.metadata.create_all(engine)
