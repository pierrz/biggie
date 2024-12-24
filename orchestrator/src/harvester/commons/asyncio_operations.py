"""
Module dedicated to all Asyncio functions

TODO: fix the orders of line in the logs i.e. writes befores gets
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path, PurePath
from typing import Dict, Iterable, List, Tuple, Union

import aiohttp
import pandas as pd
from config import data_directories, harvester_config
from src import logger
from src.commons import names as ns

from .errors import APILimitError, EmptyResults, GenericError


async def get_url(auth: Dict = None, **kwargs):

    try:
        async with aiohttp.ClientSession() as client:

            url = kwargs["url"]
            parameters = {"url": url}
            get_message = f"Start downloading {url}"

            if isinstance(auth, Dict):
                get_message += " (with authentication parameters i.e. key/token)"
                parameters["headers"] = auth

            logger.info(get_message)
            response = await client.get(**parameters)
            logger.success("Successful download.")

            if "mode" in kwargs:
                if kwargs["mode"] == "json":
                    return await response.json()
                elif kwargs["mode"] in ["csv", "txt"]:
                    return await response.content.read()
                elif kwargs["mode"] == "response":
                    return response

            # TODO: check why that still throws something ...
            # status = response.status
            # headers = response.headers
            # logger.info(status)
            # logger.info(headers)
            # # return (status, headers)
            # return response

    except KeyError as e:
        APILimitError(e)
    except Exception as e:
        GenericError(e)


def download(func):
    """
    Async loop to download a list of urls
    :param func: the function actually cleaning the parsed data
    :return: the retrieved data as an array
    """

    async def get(url, auth, filepath: Path = None, **kwargs):

        try:
            params = {"url": url, "auth": auth}
            if filepath is not None:
                params[ns.mode] = PurePath(filepath).suffix[1:]
            elif ns.mode in kwargs:
                params[ns.mode] = kwargs[ns.mode]

            data = await get_url(**params)

            if filepath is not None:
                final_data = await func(data, **kwargs)
                return {
                    ns.filepath: filepath,
                    ns.data: final_data,
                    ns.mode: params[ns.mode],
                }
            return await func(data, **kwargs)

        except TypeError as e:
            EmptyResults(e)
        except Exception as e:
            GenericError(e)

    async def inner(
        urls: Iterable[str],
        auth: Dict = None,
        filepaths: Iterable[str] = None,
        **kwargs,
    ) -> List[Tuple[str, bytes]]:
        if filepaths is not None:
            return await asyncio.gather(
                *[
                    get(url, auth, filepaths[idx], **kwargs)
                    for idx, url in enumerate(urls)
                ]
            )

        return await asyncio.gather(*[get(url, auth, **kwargs) for url in urls])

    return inner


@download
async def download_passthrough(data_input, **kwargs) -> Iterable[Dict]:
    """
    For testing purpose (passthrough)
    :param data: the received data
    :return: the received data
    """

    return data_input


@download
async def download_github_events(
    data, filtered: bool = True, output: str = None, **kwargs
) -> Iterable[Dict]:
    """
    Handles downloads from the GitHub Events API
    :param data: the received data
    :param filtered: allow for production data cleaning (enabled by default)
    :param output: how the data is exported (json array per default)
    :return: the filtered data
    """

    print(data)
    raw_df = pd.DataFrame(data)
    if filtered:
        mask = raw_df["type"].isin(harvester_config.EVENTS)
        df = raw_df[mask]
    else:
        df = raw_df

    print(df.head(5))
    if output == "df":
        return df
    return df.to_dict("records")


async def write(filepath: Path, data: Dict, mode: str, output_dir: Path):
    """
    Writes a file based on a mode and maybe an output directory
    :param filepath: filepath (can have sub-directories)
    :param data: data to write
    :param mode: mode to export the data with
    :param output_dir: output directory
    """

    fullpath = Path(output_dir, filepath)
    if not fullpath.parent.exists():
        fullpath.parent.mkdir(parents=True)

    logger.info(f"Start writing file '{fullpath.name}' ('{mode}' mode) ...")
    with open(fullpath, "w", encoding="utf8") as output_file:
        if mode == "json":
            json.dump(data, output_file, indent=4)
        elif mode in ["csv", "txt"]:
            output_file.write(data.decode("utf-8"))
            output_file.close()
    logger.success("File saved successfully.")


async def write_with_id(
    id: int,
    data: Dict,
    timestamp: str,
    filepath: Union[Path, str] = None,
    output_dir: Path = None,
):
    """
    Writes a file and names it automatically. For now, only create JSON file
    :param id: page position
    :param page: page data
    :param output_dir: directory where to save the files
    :param timestamp: timestamp string for this batch
    :param filepath: for testing purpose, used to bypass the file naming pattern
    :return: write a JSON file
    """

    if output_dir is None:
        output_dir = data_directories.batch
        output_dir.mkdir(parents=True, exist_ok=True)

    if filepath is None:
        filepath = f"{timestamp}_page-{id}.json"

    await write(filepath=filepath, data=data, mode="json", output_dir=output_dir)


async def write_aio(data_array: Iterable[Dict], output_dir: Path = None):
    """
    Write data into JSON files with a trimmed timestamp (date-hour-minute only).
    :param data_array: array of dictionaries
    :param output_dir: the directory where the files will be written
    :return: does its thing
    """

    has_filepaths = False
    if isinstance(data_array[0], Dict):
        keys = list(data_array[0].keys())
        if keys == ns.output_keys:
            has_filepaths = True

    if (
        has_filepaths
    ):  # if it's not a list of rows (when dict array including filepaths is provided)
        await asyncio.gather(
            *[write(**data, output_dir=output_dir) for data in data_array]
        )

    else:  # file auto-naming (only dict array is provided), better used against APIs
        timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M")
        await asyncio.gather(
            *[
                write_with_id(
                    id=idx,
                    data=data,
                    timestamp=timestamp,
                    output_dir=output_dir,
                )
                for idx, data in enumerate(data_array)
            ]
        )
