"""
Mongo oriented APIs
"""

from fastapi import APIRouter
from src.db.mongo.models import EventPerRepoCount, EventPerRepoCountList
from src.db.mongo_db import init_mongo_connection
from src.routers.data_lib import dataframe_from_mongo_data

router = APIRouter(
    prefix="/mongo",
    tags=["mongo"],
    responses={404: {"description": "Issue with endpoint"}},
)


@router.get("/aggregated_repo_list")
async def aggregated_repo_list():
    mongodb = init_mongo_connection()  # pylint: disable=C0103
    db_data = mongodb.events.aggregate([{"$sortByCount": "$repo_name"}])

    results_df = dataframe_from_mongo_data(db_data)
    return EventPerRepoCountList(
        repository_list=[
            EventPerRepoCount(name=repo["_id"], count=repo["count"])
            for repo in results_df.to_dict(orient="records")
        ]
    )
