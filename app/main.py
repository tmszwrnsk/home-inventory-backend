"""Initialize FastAPI application."""
import logging

from fastapi import FastAPI

from app.config import settings
from app.routers import root_api_router

log: logging.Logger = logging.getLogger(__name__)

log.debug("Initialize FastAPI application.")
app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION,
    docs_url=settings.DOCS_URL,
)
log.debug("Add application routes.")
app.include_router(root_api_router)
