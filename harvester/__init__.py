"""
Harvests the whole data from the Marvel Characters API
"""

import asyncio
import os
import time

import requests

from .config import harvester_config
from .src.asyncio_operations import download_aio, write_aio
from .src.utils import get_auth, get_meta

parameters = {
    "characters_api_url": "http://gateway.marvel.com/v1/public/characters?",
    "page_info": "&offset=0&limit=1",
}


def run():
    """
    Starts the whole module
    """

    try:
        response = requests.get(
            f"{parameters['characters_api_url']}{get_auth()}{parameters['page_info']}"
        ).json()["data"]
        response.pop("results")

        # get data from all API result pages
        total, urls = get_meta(response)
        print(f"Retrieved {total} items")
        start_time = time.time()
        json_data = asyncio.run(download_aio(urls))
        asyncio.run(write_aio(json_data, harvester_config.OUTPUT_DIR))
        print(f"Downloads took {time.time() - start_time} seconds")

    except Exception as exception:  # pylint: disable=W0703
        print(exception)


if __name__ == "__main__":

    if not harvester_config.OUTPUT_DIR.exists():
        os.mkdir(harvester_config.OUTPUT_DIR)

    run()
