import traceback
from typing import List

from fastapi import APIRouter, HTTPException

from backend.core.common.domain.exceptions.application_exception import (
    ApplicationException,
)
from backend.core.thought.application.usecases.create_thought_usecase import (
    CreateThoughtDTO,
    CreateThoughtUsecase,
)
from backend.core.thought.application.usecases.delete_thought_usecase import (
    DeleteThoughtDTO,
    DeleteThoughtUsecase,
)
from backend.core.thought.application.usecases.list_related_thoughts_usecase import (
    ListRelatedThoughtsDTO,
    ListRelatedThoughtsUsecase,
)
from backend.core.thought.application.usecases.list_thoughts_usecase import (
    ListThoughtsDTO,
    ListThoughtsUsecase,
)
from backend.core.thought.application.usecases.suggest_relevant_topics_usecase import (
    SuggestRelevantTopicsDTO,
    SuggestRelevantTopicsUsecase,
)
from backend.core.thought.application.usecases.update_thought_usecase import (
    UpdateThoughtDTO,
    UpdateThoughtUsecase,
)
from backend.core.thought.domain.entities.thought import Thought

from backend.infra.container.container import Container

router = APIRouter()


@router.get("")
async def get_thoughts(search_term: str = None) -> List[Thought]:
    """
    Get thought list
    """

    usecase = Container.resolve(ListThoughtsUsecase)

    try:
        search_request = ListThoughtsDTO(search_term=search_term)
        result = usecase.execute(search_request)
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("", status_code=204)
async def create_thought(dto: CreateThoughtDTO) -> None:
    """
    Create new thought
    """

    usecase = Container.resolve(CreateThoughtUsecase)

    try:
        result = usecase.execute(dto)
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.delete("/{thought_id}", status_code=204)
async def delete_thought(thought_id: str) -> None:
    """
    Delete thought by ID
    """

    usecase = Container.resolve(DeleteThoughtUsecase)

    try:
        result = usecase.execute(DeleteThoughtDTO(thought_id=thought_id))
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{thought_id}/relevant-topics")
async def sugget_similar_topics(thought_id: str) -> List[str]:
    """
    Get topic suggestions for a thought
    """

    usecase = Container.resolve(SuggestRelevantTopicsUsecase)

    try:
        result = usecase.execute(SuggestRelevantTopicsDTO(thought_id=thought_id))
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.get("/{thought_id}/related")
async def list_related_thoughts(thought_id):
    """
    Given a thought, list related others
    """

    usecase = Container.resolve(ListRelatedThoughtsUsecase)

    try:
        result = usecase.execute(ListRelatedThoughtsDTO(thought_id=thought_id))
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.patch("")
async def update_thought(dto: UpdateThoughtDTO):
    """
    Given a thought, list related others
    """

    usecase = Container.resolve(UpdateThoughtUsecase)

    try:
        result = usecase.execute(dto)
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
