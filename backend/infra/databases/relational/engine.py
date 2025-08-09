from sqlalchemy import create_engine
import os

# Use a persistent database file
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///solaire.db")

engine = create_engine(DATABASE_URL, echo=True)