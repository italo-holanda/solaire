import traceback
from typing import List

from fastapi import APIRouter, HTTPException

from backend.core.thought.application.usecases.list_thoughts_usecase import ListThoughtsDTO, ListThoughtsUsecase
from backend.core.thought.domain.entities.thought import Thought

from backend.infra.container.container import Container

router = APIRouter()


@router.get("/")
async def get_thoughts(search_request: ListThoughtsDTO) -> List[Thought]:
    """
    Get thought list
    """

    usecase = Container.resolve(ListThoughtsUsecase)

    try:
        result = usecase.execute(search_request)
        return result
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
