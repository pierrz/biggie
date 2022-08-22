"""
Harvests paginated data from the GitHub Events API
"""

import asyncio
import time
from pathlib import Path
from typing import Union

from config import data_directories
from src.harvester.asyncio_operations import download_github_events, write_aio
from src.harvester.auth_parameters import github_params
from src.harvester.github_events_urls import get_events_urls
from worker import celery, logger


@celery.task(name="github-events-data-acquisition")
def run_github_events_da() -> Union[int, None]:
    """
    Starts the whole module
    """

    input_dir = data_directories.github_in
    if not input_dir.exists():
        Path.mkdir(input_dir, parents=True)

    try:

        urls = asyncio.run(get_events_urls())
        logger.info(f"Retrieved {len(urls)} event pages")

        start_time = time.time()
        data_array = asyncio.run(
            download_github_events(urls, auth=github_params, mode="json")
        )
        asyncio.run(write_aio(data_array=data_array, output_dir=input_dir))
        logger.info(f"Downloads took {time.time() - start_time} seconds")

        # send page range as handle to init the cleaning (or not)
        return len(urls)

    except Exception as exception:  # pylint: disable=W0703
        logger.info(exception)
        return None
