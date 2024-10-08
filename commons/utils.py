"""
Common utilities
"""

import io
import json
from typing import Iterable, Tuple

import pandas as pd
import requests
from src import logger


def get_url(url, mode: str = None):
    """Fetch JSON data from given url"""
    response = requests.get(url)
    if mode == "json":
        return response.json()
    elif mode == "content":
        return response.content
    return response


def load_json(file_path):
    """Load JSON into dict object"""
    with open(file_path, "rt", encoding="utf8") as json_file:
        json_str = json_file.read()
        return json.loads(json_str)


def write_file(filepath, data, mode: str):
    with io.open(filepath, "w", encoding="utf-8") as output_file:
        try:
            if mode == "json":
                json.dump(data, output_file, indent=4)
                logger.info(f"=> data saved at '{filepath}'")
            elif mode == "txt":
                output_file.write(data.decode("utf-8"))
                output_file.close()
        except Exception as e:
            logger.error(e)


def dataframe_info_log(pairs: Iterable[Tuple[str, pd.DataFrame]]):
    """Celery logs with basic dataframe overview
    :param pairs: list of pairs name/dataframe
    """
    for pair in pairs:
        name, df = pair
        logger.info(
            "'{}' dataframe with {} columns and {} rows".format(name, *df.shape)
        )
        logger.info(df.head(5))
