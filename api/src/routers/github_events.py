"""
All API endpoints.
"""

from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, HTTPException, Request

# from src import logger
from src.commons import names as ns
from src.db.mongo.models import (
    Event,
    EventAverageTime,
    EventPerRepoCount,
    EventPerRepoCountList,
    EventType,
    EventTypeCount,
    EventTypeCountList,
)
from src.db.mongo.mongo_db import init_pymongo_client
from src.routers import templates
from src.routers.data_lib import (
    dataframe_from_mongo_data,
    delta_timeline_data,
    generate_diagram,
    validate_data,
)

router = APIRouter(
    prefix=f"/{ns.events}",
    tags=[f"{ns.events}"],
    responses={404: {"description": "Issue with endpoint"}},
)


@router.get("/counts")
async def counts(limit: str | int = 50):
    """
    List of repositories with the most PR occurences. Default size is 50.
    :param limit: size of the response, can be changed with '?limit=<int>' query parameter.
    :return: a json response
    """
    mongodb = init_pymongo_client()  # pylint: disable=C0103

    type_query = {"type": EventType.PullRequestEvent}
    count = mongodb.events.count_documents(type_query)
    if count == 0:
        raise HTTPException(status_code=404, detail="No events data available.")

    db_data = mongodb.events.aggregate(
        [
            {"$match": {"type": EventType.PullRequestEvent}},
            {"$sortByCount": "$repo_name"},
            {"$limit": int(limit)},
        ]
    )

    results_df = dataframe_from_mongo_data(db_data)
    return EventPerRepoCountList(
        repository_list=[
            EventPerRepoCount(name=repo["_id"], count=repo["count"])
            for repo in results_df.to_dict(orient="records")
        ]
    )


@router.get("/count")
async def count(repo_name: str):
    """
    PR events count for a given repo.
    :param repo_name: name of the repository
    :return: a json response
    """
    mongodb = init_pymongo_client()  # pylint: disable=C0103
    query = {"repo_name": repo_name, "type": EventType.PullRequestEvent}
    count = mongodb.events.count_documents(query)

    if count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No events data available for the repository '{repo_name}'.",
        )
    return EventPerRepoCount(name=repo_name, count=count)


@router.get("/count_per_type/all")
async def count_per_type_all(offset: str = "0"):
    """
    Return the total number of events grouped by the event type for a given offset.
    The offset determines how much time we want to look back
    i.e. an offset of 10 means we count only the events which have been created in the last 10 minutes
    :param offset: offset in minutes
    :return: a json response
    """

    mongodb = init_pymongo_client()

    iso_date_with_delta = datetime.now(timezone.utc) - timedelta(minutes=int(offset))
    offset_query = {"created_at": {"$lte": iso_date_with_delta}}

    # if repo_name is None:
    count = mongodb.events.count_documents(offset_query)
    if count == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No events retrieved with an offset of {offset} minutes.",
        )

    aggregation_pipeline = [
        {"$match": offset_query},
        {"$sortByCount": "$type"},
        {
            "$project": {
                "type": "$_id",  # Rename _id to type
                "count": 1,  # Keep the count field
            }
        },
    ]
    db_data = mongodb.events.aggregate(aggregation_pipeline)
    results_df = dataframe_from_mongo_data(db_data)

    return EventTypeCountList(
        count_per_type=[
            EventTypeCount(type=record["type"], count=record["count"])
            for record in results_df.to_dict(orient="records")
        ]
    )


@router.get("/count_per_type")
async def count_per_type(repo_name: str, offset: str = "0"):
    """
    Return the total number of events grouped by the event type for a given offset.
    The offset determines how much time we want to look back
    i.e. an offset of 10 means we count only the events which have been created in the last 10 minutes
    :param offset: offset in minutes
    :return: a json response
    """

    mongodb = init_pymongo_client()

    iso_date_with_delta = datetime.now(timezone.utc) - timedelta(minutes=int(offset))
    offset_query = {"created_at": {"$lte": iso_date_with_delta}}
    query = {"repo_name": repo_name, **offset_query}
    db_data = mongodb.events.find(query)
    results_df = dataframe_from_mongo_data(db_data)

    if results_df.shape[0] == 0:
        raise HTTPException(
            status_code=404,
            detail=f"No events retrieved with an offset of {offset} minutes and/or the repository '{repo_name}'.",
        )

    grouped_df = (
        results_df[["repo_name", "type"]]
        .rename(columns={"repo_name": "count"})
        .groupby(["type"])
        .count()
        .reset_index()
    )
    return EventTypeCountList(
        count_per_type=[
            EventTypeCount(type=record["type"], count=record["count"])
            for record in grouped_df.to_dict(orient="records")
        ]
    )


@router.get("/pr_average_delta")
async def pr_average_delta(repo_name: str):
    """
    Calculate the average time between pull requests for a given repository
    :param repo_name: name of the repository to check
    :return: a json response
    """

    mongodb = init_pymongo_client()  # pylint: disable=C0103
    query = {"repo_name": repo_name, "type": EventType.PullRequestEvent}
    count = mongodb.events.count_documents(query)
    average_time = None

    if not count > 1:
        raise HTTPException(
            status_code=404,
            detail=f"Not enough PullRequestEvent data retrieved for '{repo_name}' (2 PRs minimum).",
        )

    db_data = mongodb.events.find(query)
    valid_data = validate_data(db_data, model=Event)
    results_df = dataframe_from_mongo_data(valid_data, "created_at")

    deltas = results_df["created_at"].diff().dt.total_seconds()
    average_time = round(
        deltas.drop(index=0).mean(), 3
    )  # rounded to millisecond floats

    return EventAverageTime(pr_average_time_in_seconds=average_time)


@router.get("/pr_deltas_timeline")
async def pr_deltas_timeline(request: Request, repo_name: str, size: int = 0):
    """
    Plots a diagram showing the time deltas between the last n PRs for that repo.
    Generates a unique html template for each call, based on repo name and timestamp
    :param repo_name: name of the repository to check
    :param size: how much PR intervals will be displayed (needs to be higher than 2 to generate to enough delta points)
    :return: a json response
    """

    mongodb = init_pymongo_client()  # pylint: disable=C0103

    query = {"repo_name": repo_name, "type": EventType.PullRequestEvent}
    count = mongodb.events.count_documents(query)
    if count == 0:
        raise HTTPException(
            status_code=404,
            detail="Not enough data to make a PR timeline:"
            " 3 PullRequestEvents minimum are required to generate 2 intervals.",
        )

    results_df = delta_timeline_data(mongodb, repo_name, size)
    diagram_filepath = generate_diagram(results_df, repo_name, size)

    return templates.TemplateResponse(
        diagram_filepath,
        context={
            "request": request,
        },
    )


@router.get("/dashboard")
async def dashboard(request: Request):
    """
    Dashboard page
    """

    event_counts = await counts()
    data = [event.dict() for event in event_counts.repository_list]

    return templates.TemplateResponse(
        f"{ns.github_events}/dashboard.html",
        context={
            "request": request,
            "data": data,
            "title": "Dashboard",
            "table_headers": list(EventPerRepoCount.model_fields),
        },
    )


# 'details/{repo_name}' generated errors due to the '/' in repo_name
@router.get("/details")
async def details(request: Request, repo_name: str):
    """
    Detailed page for each event, with embedded average PR time and diagram
    """

    mongodb = init_pymongo_client()  # pylint: disable=C0103
    average_delta = await pr_average_delta(repo_name)
    pr_count = await count(repo_name)
    results_df = delta_timeline_data(mongodb, repo_name, pr_count.count)
    diagram_filepath = generate_diagram(results_df, repo_name, pr_count.count)

    return templates.TemplateResponse(
        f"{ns.github_events}/details.html",
        context={
            "request": request,
            "repo_name": repo_name,
            "pr_count": pr_count.count,
            "pr_average_delta": average_delta.pr_average_time_in_seconds,
            "diagram_filepath": diagram_filepath,
            "title": "Details",
        },
    )
