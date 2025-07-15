import traceback

from fastapi import APIRouter, HTTPException

from backend.core.common.domain.exceptions.application_exception import ApplicationException
from backend.core.publication.application.usecases.create_publication_preview_usecase import CreatePublicationPreviewDTO, CreatePublicationPreviewUsecase
from backend.core.publication.application.usecases.create_publication_content_usecase import CreatePublicationContentDTO, CreatePublicationContentUsecase
from backend.core.publication.domain.entities.publication import Publication
from backend.infra.container.container import Container

router = APIRouter()


@router.post("/preview")
async def create_publication_preview(dto: CreatePublicationPreviewDTO) -> Publication:
    """
    Create publication preview from selected thoughts
    """

    usecase = Container.resolve(CreatePublicationPreviewUsecase)

    try:
        result = usecase.execute(dto)
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/content")
async def create_publication_content(dto: CreatePublicationContentDTO) -> Publication:
    """
    Create publication content from publication id and outlining
    """

    usecase = Container.resolve(CreatePublicationContentUsecase)

    try:
        result = usecase.execute(dto)
        return result
    except ApplicationException as ae:
        raise HTTPException(status_code=ae.code, detail=ae.message)
    except Exception:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal server error")
