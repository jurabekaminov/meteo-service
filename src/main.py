import json
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from src.api import router as meteo_router
from src.config import settings
from src.etl_handler import etl_handler

logger = logging.getLogger(__name__)


def setup_logging() -> None:
    with Path("logs_config.json").open("r") as f:
        config = json.load(f)
    logging.config.dictConfig(config)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    setup_logging()
    scheduler = etl_handler.get_scheduler()
    scheduler.start()
    logger.info("Application startup complete.")
    yield
    scheduler.shutdown()
    logger.info("Application shutdown complete.")


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.TITLE,
        version=settings.VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )
    app.include_router(meteo_router)
    return app
