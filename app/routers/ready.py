"""Application implementation - Ready router."""

from fastapi import APIRouter, status

from app import schemas

router = APIRouter()


@router.get(
    "/ready",
    tags=["ready"],
    response_model=schemas.ReadyResponse,
    summary="Simple health check.",
    status_code=status.HTTP_200_OK,
)
def readiness_check() -> schemas.ReadyResponse:
    """Run basic application health check.

    If the application is up and running then this endpoint will return simple
    response with status ok.
    \f

    Returns:
        response (ReadyResponse): ReadyResponse model object instance.

    """

    return schemas.ReadyResponse(status="ok")
