import logging
from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.staticfiles import StaticFiles
from src.db import db_helper
from src.logging_conf import setup_logger
from src.settings import settings
from fastapi import FastAPI

APP_ROOT = Path(__file__).parent
setup_logger()

logger = logging.getLogger("fastapi_app")



@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    yield
    # shutdown
    await db_helper.dispose()


def mount_folders(app: FastAPI):
    media_dir = Path(__file__).parent / "media"
    media_dir.mkdir(parents=True, exist_ok=True)
    app.mount("/media", StaticFiles(directory=APP_ROOT / "media"), name="media")


def create_app() -> FastAPI:
    logger.debug("Creating app...")
    app = FastAPI(
        title="Кофеен API",
        version=settings.api.version,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )

    logger.debug("Mount folders...")
    mount_folders(app)

    logger.debug("Configure middleware...")
    app.add_middleware(SessionMiddleware, secret_key=settings.token.secret_key)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app
