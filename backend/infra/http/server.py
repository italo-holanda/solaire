from dotenv import load_dotenv
from fastapi import FastAPI

from backend.infra.http.routes import common, thoughts, categorires

load_dotenv(dotenv_path='.env')

app = FastAPI()

app.include_router(common.router)
app.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
app.include_router(categorires.router, prefix="/categories", tags=["categories"])