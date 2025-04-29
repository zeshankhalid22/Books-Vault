from fastapi import FastAPI
import logging

from starlette.staticfiles import StaticFiles

from app.core.logger import setup_logging
from app.api.routers.main_router import router

from fastapi.middleware.cors import CORSMiddleware

setup_logging()


logger = logging.getLogger(__name__)

# Create application
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

# Log application startup
logger.info("Application started")

# You can use logger throughout your application
logger.debug("Debug message")
logger.warning("Warning message")
logger.error("Error message")