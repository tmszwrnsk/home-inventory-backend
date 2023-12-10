"""Application configuration - FastAPI."""
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.version import __version__


class Application(BaseSettings):
    """Define application configuration model.

    Constructor will attempt to determine the values of any fields not passed
    as keyword arguments by reading from the environment. Default values will
    still be used if the matching environment variable is not set.

    Environment variables:
        * FASTAPI_DEBUG
        * FASTAPI_PROJECT_NAME
        * FASTAPI_VERSION
        * FASTAPI_DOCS_URL

    Attributes:
        DEBUG: FastAPI logging level. Disable this for production.
        PROJECT_NAME: FastAPI project name.
        VERSION: Application version.
        DOCS_URL: Path where swagger ui will be served at.

    """

    model_config = SettingsConfigDict(case_sensitive=True, env_prefix="FASTAPI_")

    DEBUG: bool = True
    PROJECT_NAME: str = "home-inventory"
    VERSION: str = __version__
    DOCS_URL: str = "/"


settings = Application()
