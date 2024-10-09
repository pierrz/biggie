"""
Loads required data from JSON files into MongoDB
"""

import os
from pathlib import Path
from typing import List

import pandas as pd
from config import data_directories
from src import logger
from src.commons import enums
from src.commons import names as ns
from src.spark_jobs.commons.jobs import ToMongoFromJson
from src.spark_jobs.github_events.events_mongo_connectors import EventReader
from src.spark_jobs.github_events.schemas import event_schema
from worker import celery


def github_event_data_preparation(flat_df):
    """
    Prepare incoming data from the Github Event API and keep only the relevant bits.
    """

    logger.info("=> Preparing dataframe ...")
    columns_to_drop = []
    columns_to_rename = {"id": enums.CheckedColumns.event_id}
    for col in flat_df.columns.to_list():
        if col.startswith("payload") or col.startswith("org"):
            columns_to_drop.append(col)

    if len(columns_to_drop) > 0:
        flat_df.drop(
            columns=columns_to_drop, inplace=True
        )  # reducing the loaded data (prod)

    flat_df.rename(columns=columns_to_rename, inplace=True)
    datetime_values = pd.to_datetime(flat_df[ns.created_at])
    flat_df[ns.created_at] = datetime_values
    # flat_df[enums.CheckedColumns.event_id].astype("int64")     # not sure whether it is wise on the long-run
    logger.success(" ... dataframe finalised")
    columns = flat_df.columns.to_list()
    logger.info(f"=> {flat_df.shape[0]} rows and {len(columns)} columns")


@celery.task(name="load-github-events")
def run_load_events(page_range: int) -> List[int]:
    """
    Starts the whole module
    *args is bein used to handle the 'None' returned by harvester_task (necessary for the scheduled chain)
    """

    input_dir = data_directories.github_in
    output_dir = data_directories.github_out

    if not output_dir.exists():
        Path.mkdir(output_dir, parents=True)

    logger.info("Initiating data loading task to Mongo ...")
    ToMongoFromJson(
        input_dir_paths=[input_dir],
        collection=ns.events,
        check_columns=list(enums.CheckedColumns),
        output_dir_path=output_dir,
        reader_class=EventReader,
        custom_preps=github_event_data_preparation,
        schema=event_schema,
    )
    logger.success("=> Data loaded successfully.")

    file_count = len(os.listdir(output_dir))
    if file_count is None:
        return [0, page_range]
    return [file_count, page_range]
