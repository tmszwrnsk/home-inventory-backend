"""Application implementation - Ready router."""
import logging

from fastapi import APIRouter, status

from app import schemas

router = APIRouter()
log: logging.Logger = logging.getLogger(__name__)


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
    log.info("Started GET /ready")

    return schemas.ReadyResponse(status="ok")
