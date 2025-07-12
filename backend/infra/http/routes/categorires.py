import traceback
from typing import List

from fastapi import APIRouter, HTTPException

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.category.application.usecases.list_categories_usecase import ListCategoriesUsecase
from backend.core.category.domain.entities.category import Category
from backend.infra.container.container import Container

router = APIRouter()


@router.get("")
async def list_categories() -> List[Category]:
    """
    Get categories list
    """

    usecase = Container.resolve(ListCategoriesUsecase)

    try:
        result = usecase.execute()
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
