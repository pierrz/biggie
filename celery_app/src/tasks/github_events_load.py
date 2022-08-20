"""
Loads required data from JSON files into MongoDB
"""

import os
from pathlib import Path
from typing import List

from config import data_directories
from src.pyspark.jobs import ToMongoFromJson
from src.pyspark.mongo_connectors import EventReader
from worker import celery, logger


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
    ToMongoFromJson(input_dir_paths=[input_dir],
                    collection="event",
                    check_columns=["type", "actor_id", "repo_name"],
                    output_dir_path=output_dir,
                    reader_class=EventReader)
    logger.info("=> Data loaded successfully.")

    file_count = len(os.listdir(output_dir))
    if file_count is None:
        return [0, page_range]
    return [file_count, page_range]
