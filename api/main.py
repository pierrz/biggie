"""
Module spinning up FastApi
"""

from config import app_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.db import models
from src.db.postgres import pg_engine
from src.routers import api_endpoints, dummy_endpoint, github_events

models.Base.metadata.create_all(bind=pg_engine)

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
app.include_router(dummy_endpoint.router)
app.include_router(github_events.router)
app.include_router(api_endpoints.router)
