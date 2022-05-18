"""
Module spinning up FastApi
"""
import os

from config import app_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.routers import api_endpoints
from src.tasks.harvester_task import harvester_task
from src.tasks.spark_task import spark_task

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

if app_config.LOCAL_DEV:
    localhost_origins = [
        "http://localhost",
        "https://localhost",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=localhost_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# routers
app.include_router(api_endpoints.router)


def init_pipeline():
    """
    Start the celery pipeline for harvesting data from the Marvel characters API
    and store it into Mongo
    :return: does its thing
    """

    for data_dir in [app_config.OUTPUT_DIR, app_config.PROCESSED_DIR]:
        if not data_dir.exists():
            os.mkdir(data_dir)

    chain = harvester_task.s() | spark_task.s()
    chain()


# TODO: move all that into a separate container
if app_config.APP_MODE == "PROD":
    init_pipeline()
