"""
Mongo oriented APIs
"""

from fastapi import APIRouter
from pydantic import BaseModel
from src.db.mongo import init_mongo_connection
from src.routers.data_lib import dataframe_from_mongo_data

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
    responses={404: {"description": "Issue with endpoint"}},
)


class Repo(BaseModel):
    name: str
    count: int


class RepoList(BaseModel):
    repository_list: list[Repo]


@router.get("/aggregated_repo_list")
async def aggregated_repo_list():
    mongodb = init_mongo_connection()  # pylint: disable=C0103
    db_data = mongodb.event.aggregate(
        [
            {"$group": {"_id": "$repo_name", "count": {"$count": {}}}},
            {"$sort": {"count": -1}},
        ]
    )
    results_df = dataframe_from_mongo_data(db_data, sort_by="count")
    return RepoList(
        repository_list=[
            Repo(name=repo["_id"], count=repo["count"])
            for repo in results_df.to_dict(orient="records")
        ]
    )
