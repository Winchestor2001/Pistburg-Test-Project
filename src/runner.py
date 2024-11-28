import logging

import uvicorn

from src.apps.api.routers import api_router

from src.fastapi_core import create_app
from src.settings import settings

logger = logging.getLogger('fastapi_app')

main_app = create_app()

main_app.include_router(api_router)


if __name__ == "__main__":
    logger.debug("Application started")
    uvicorn.run(
        "runner:main_app",
        host=settings.run.host,
        port=settings.run.port,
        # reload=True,
    )
    logger.debug("Application stopped")
