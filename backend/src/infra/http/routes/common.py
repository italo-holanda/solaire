import tomli
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponseDto(BaseModel):
    status: str
    version: str


@router.get("/healthz")
def healthz() -> HealthResponseDto:
    """
    Health check endpoint
    """

    with open("pyproject.toml", "rb") as f:
        pyproject_data = tomli.load(f)
        version = pyproject_data.get("project", {}).get("version", "unknown")

    return HealthResponseDto(status="ok", version=version)
