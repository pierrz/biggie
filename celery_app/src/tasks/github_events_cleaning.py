"""
Cleaning task aka deleting all files in the local 'data/processed' directory and related Mongo collection
"""

import os
import shutil
from pathlib import Path
from typing import List

from config import data_directories
from src import logger
from src.commons import names as ns
from worker import celery


@celery.task(name="github-events-cleaning")
def clean_local_files(args: List[int], wait_minutes: int):
    """
    Task deleting all the files whose data was already loaded in Mongo
    :return: does its thing
    """

    file_count, page_range = args
    rest_minutes = wait_minutes - int(file_count / page_range)

    if rest_minutes <= 0:

        logger.info("Cleaning task initialised ...")
        shutil.rmtree(data_directories.github_out)
        logger.success(f"- {file_count} data files were deleted.")

        templates_dir = data_directories.github_diagrams
        diag_count = 0
        if templates_dir.exists():
            with os.scandir(templates_dir) as it:
                for entry in it:
                    if entry.is_file():
                        os.remove(Path(entry))
                        diag_count += 1
            logger.success(f"- {diag_count} HTML {ns.diagrams} were deleted.")

    else:
        logger.warning(
            f"=> {rest_minutes} minutes remaining before next cleaning operation."
        )
