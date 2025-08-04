from src.infra.databases.relational.engine import engine
from src.infra.databases.relational.models import Base

Base.metadata.create_all(engine)
