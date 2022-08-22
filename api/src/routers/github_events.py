"""
All API endpoints.
"""

from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
from config import diagrams_dir
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from src.db.mongo import init_mongo_connection
from src.routers.templates import templates

router = APIRouter(
    prefix="/events",
    tags=["events"],
    responses={404: {"description": "Issue with endpoint"}},
)


@router.get("/")
def main():
    return RedirectResponse(url="/docs/")


def dataframe_from_mongo_data(db_data, sort_by: str = None):
    """
    Prepares the data retrieved from Mongo to be compliant with pd.DataFrame and JSONResponse
    :param db_data: data retrieved from Mongo
    :param sort_by: the column to sort the dataframe with
    :return: the prepared/cleaned dataframe
    """

    raw_df = pd.DataFrame(db_data)
    if raw_df.shape[0] > 1:  # at least 2 rows to get an interval
        raw_df.drop(columns=["_id"])
        # drop_duplicates to cover potential overlaps from the GitHub events API
        clean_df = raw_df.drop_duplicates().replace(to_replace=[np.nan], value=[""])

        if sort_by is None:
            return clean_df
        return clean_df.sort_values(by=sort_by)

    return None


@router.get("/pr_deltas_timeline")
async def pr_deltas_timeline(request: Request, repo_name: str, size: int = 0):
    """
    Plots a diagram showing the time deltas between the last n PRs for that repo.
    Generates a unique html template for each call, based on repo name and timestamp
    :param repo_name: name of the repository to check
    :param size: how much PR intervals will be displayed (needs to be higher than 2 to generate to enough delta points)
    :return: a json response
    """

    # data
    mongodb = init_mongo_connection()  # pylint: disable=C0103
    db_data = mongodb.event.find({"repo_name": repo_name, "type": "PullRequestEvent"})
    raw_df = dataframe_from_mongo_data(db_data, "created_at")

    if raw_df is None:
        return JSONResponse({"result": "not enough data to make a PR timeline (at least 3 events for 2 intervals)"})

    if size > 2:
        results_df = raw_df.tail(size).reset_index()
    else:
        results_df = raw_df.reset_index()

    dates = pd.to_datetime(results_df["created_at"]).rename("#PR")
    deltas = dates.diff().dt.total_seconds().drop(index=0)
    plot_df = pd.DataFrame(
        list(zip(deltas.index, deltas)), columns=["#PR", "delta (seconds)"]
    ).astype({"#PR": "int32"})

    # diagram
    fig = px.line(plot_df, x="#PR", y="delta (seconds)")
    fig.update_xaxes(nticks=plot_df.shape[0])  # shows only integers for that axe

    title_text = (
        f"<span style='font-weight:800;'>PR deltas timeline</span> [{repo_name}]"
    )
    if 0 < size < 3:
        title_text += "<br><span style='font-size: .8rem;'>/!\\ the required size is too small (< 2)</span>"
    fig.update_layout(title_text=title_text)

    # html
    timestamp = datetime.now(timezone.utc).isoformat()
    normalized_repo_name = repo_name.replace("/", "_-_")
    filename = f"pr_deltas_timeline_{normalized_repo_name}_{timestamp}.html"

    if not diagrams_dir.exists():
        Path.mkdir(diagrams_dir, parents=True)

    fig.write_html(Path(diagrams_dir, filename))

    return templates.TemplateResponse(
        str(Path("diagrams", filename)),
        context={
            "request": request,
        },
    )


@router.get("/pr_average_delta")
async def pr_average_delta(repo_name: str):
    """
    Calculate the average time between pull requests for a given repository
    :param repo_name: name of the repository to check
    :return: a json response
    """

    mongodb = init_mongo_connection()  # pylint: disable=C0103
    db_data = mongodb.event.find({"repo_name": repo_name, "type": "PullRequestEvent"})
    results_df = dataframe_from_mongo_data(db_data, "created_at")

    if results_df is not None:
        dates = pd.to_datetime(results_df["created_at"])
        deltas = dates.diff().dt.total_seconds()
        average_pr = round(
            deltas.drop(index=0).mean(), 3
        )  # rounded to millisecond floats
        response_data = {"pr_average_time[seconds]": average_pr}

    else:
        response_data = {
            "pr_average_time[error]": f"only 1 PullRequestEvent retrieved for '{repo_name}' (2 events minimum)"
        }

    return JSONResponse(response_data)


@router.get("/count_per_type")
async def count_per_type(offset: str):
    """
    Return the total number of events grouped by the event type for a given offset.
    The offset determines how much time we want to look back
    i.e. an offset of 10 means we count only the events which have been created in the last 10 minutes
    :param offset: offset in minutes
    :return: a json response
    """

    time_with_offset = (
        datetime.now(timezone.utc) - timedelta(minutes=int(offset))
    ).isoformat()
    offset_filter = {"created_at": {"$lte": f"{time_with_offset}"}}

    mongodb = init_mongo_connection()  # pylint: disable=C0103
    db_data = mongodb.event.find(offset_filter)
    results_df = dataframe_from_mongo_data(db_data)

    if results_df is not None:
        data = (
            results_df[["repo_name", "type"]]
            .rename(columns={"repo_name": "type_count"})
            .groupby(["type"])
            .count()
        )
        return JSONResponse(data.to_dict())

    return JSONResponse({"result": "no events retrieved with this offset"})
