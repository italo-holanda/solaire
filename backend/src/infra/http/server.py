from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.infra.http.routes import common, thoughts, categorires, publications

root_dir = Path(__file__).parent.parent.parent.parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(common.router)
app.include_router(thoughts.router, prefix="/thoughts", tags=["thoughts"])
app.include_router(categorires.router, prefix="/categories", tags=["categories"])
app.include_router(publications.router, prefix="/publications", tags=["publications"])