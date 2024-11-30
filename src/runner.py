import logging
import uvicorn

from src.apps.api.routers import api_router
from src.apps.websocket.consumers import ws

from src.fastapi_core import create_app
from src.settings import settings

logger = logging.getLogger(__name__)

main_app = create_app()

main_app.include_router(api_router)
main_app.include_router(ws)

if __name__ == "__main__":
    logger.debug("Application started")
    uvicorn.run(
        "runner:main_app",
        host=settings.run.host,
        port=settings.run.port,
        # reload=True,
    )
    logger.debug("Application stopped")
