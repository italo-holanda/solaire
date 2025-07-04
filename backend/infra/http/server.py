from dotenv import load_dotenv
from fastapi import FastAPI

from backend.infra.http.routes import common

load_dotenv(dotenv_path='.env')

app = FastAPI()

app.include_router(common.router)
