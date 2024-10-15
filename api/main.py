"""
Module spinning up FastApi
NB: Postgres is disabled at the moment, only Mongo is handling data
"""

from config import main_config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.routers import dummy_endpoint, github_events

# DISABLED (current endpoints only rely on MongoDB)
# from src.db import models
# from src.db.postgres.postgres_db import pg_engine
# models.Base.metadata.create_all(bind=pg_engine)

app = FastAPI(debug=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# TODO: fix the CSP issue with static files
allowed_ip_trails = [
    "121",  # API test
    "122",  # API prod
    "111",  # Jupyter
    "101",  # MongoDB
    # "102"   # PostgreSQL
]
allowed_origins = [
    f"https://{main_config.DOCKER_SUBNET_BASE}.{trail}" for trail in allowed_ip_trails
]
allowed_origins += [
    f"http://{main_config.DOCKER_SUBNET_BASE}.122:{main_config.API_PORT}/static"
]
# allowed_origins += [f"http://{main_config.DOCKER_SUBNET_BASE}.122"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# routers
app.include_router(dummy_endpoint.router)
app.include_router(github_events.router)
