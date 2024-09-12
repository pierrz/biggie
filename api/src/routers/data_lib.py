from datetime import datetime, timezone
from pathlib import Path
from typing import List, Type

import numpy as np
import pandas as pd
import plotly.express as px
from config import diagrams_dir
from pydantic import BaseModel
from pymongo import MongoClient
from pymongo.command_cursor import CommandCursor
from src.db.mongo.models import Event, EventType


def dataframe_from_mongo_data(
    db_data: CommandCursor, sort_by: str = None
) -> pd.DataFrame:
    """
    Prepares the data retrieved from Mongo to be compliant with pd.DataFrame and JSONResponse
    :param db_data: data retrieved from Mongo
    :param sort_by: the column to sort the dataframe with
    :return: the prepared/cleaned pandas dataframe
    """

    raw_df = pd.DataFrame(db_data)
    clean_df = raw_df.drop_duplicates().replace(to_replace=[np.nan], value=[""])
    if sort_by is None:
        return clean_df
    return clean_df.sort_values(by=sort_by)


def validate_data(data: CommandCursor, model: Type[BaseModel]) -> List[BaseModel]:
    """
    Validate data (from Postgres or Mongo) based on a specific Pydantic model.
    Convert the validated data into a list to pass it into Pandas later on.
    :return: a list of instances of Pydantic models
    """

    valid_data = [model(**doc).dict() for doc in data]
    return valid_data


def delta_timeline_data(
    mongodb: MongoClient, repo_name: str, size: int
) -> pd.DataFrame:
    """
    Prepare the data to compute the deltas between PRs
    :param mongodb: mongo client
    :param repo_name: name of the related repository
    :param size: data size
    :return: the prepared dataframe
    """
    db_data = mongodb.events.find(
        {"repo_name": repo_name, "type": EventType.PullRequestEvent}
    )
    valid_data_dict = validate_data(db_data, model=Event)
    raw_df = dataframe_from_mongo_data(valid_data_dict, "created_at")

    if size > 2:
        results_df = raw_df.tail(size).reset_index()
    else:
        results_df = raw_df.reset_index()

    return results_df


def generate_diagram(results_df: pd.DataFrame, repo_name: str, size: int) -> str:
    """
    Generate the diagram for the PR deltas timeline
    :param results_df: input dataframe
    :param repo_name: name of the related repository
    :param size: data size
    :return: path of the generated file
    """

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

    file_path = Path(diagrams_dir, filename)
    fig.write_html(file_path)

    return f"{diagrams_dir.name}/{filename}"
