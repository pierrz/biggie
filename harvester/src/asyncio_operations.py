"""
Module dedicated to all Asyncio functions
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import aiohttp


def download(func):
    """
    Decorator function meant to download URLs
    :param func: the function used along this decorator
    :return: the downloaded data
    """
    async def inner(url):
        print(f"Start downloading {url}")
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            data = await resp.json()
        print(f"Done downloading {url}")
        return await func(data)

    return inner


@download
async def download_test(data):
    """
    For testing purpose (passthrough)
    :param data: the received data
    :return: the received data
    """
    return data


@download
async def download_marvel_api_test(data):
    """
    Handles downloads from the Marvel API
    :param data: the received data
    :return: the filtered data
    """
    results = data["data"].pop("results")
    return results, data


@download
async def download_marvel_api(data):
    """
    Handles downloads from the Marvel API
    :param data: the received data
    :return: the filtered data
    """
    results = data["data"].pop("results")
    return results


async def download_aio(urls: Iterable[str]) -> List[Tuple[str, bytes]]:
    """
    Async loop to download a list of urls
    :param urls: the list of urls to download
    :return: the retrieved data as an array
    """
    return await asyncio.gather(*[download_marvel_api(url) for url in urls])


async def write(idx: int, page: Dict, output_dir: Path = None, path: Path = None):
    """

    :param idx: page position
    :param page: page data
    :param output_dir: directory where to save the files
    :param path: for testing purpose, used to bypass the file naming pattern
    :return: write the file
    """
    print(f"Start writing page {idx}")
    if path is None:
        path = Path(output_dir, f"page-{idx}_{datetime.utcnow().isoformat()}.json")
    with open(path, "w", encoding="utf8") as output_file:
        json.dump(page, output_file, indent=4)
    print(f"Done writting page {idx}")


async def write_aio(data: Iterable[Dict], output_dir: Path):
    """
    Write data into JSON files.
    :param data: array of dictionaries
    :param output_dir: the directory where the files will be written
    :return: does its thing
    """
    await asyncio.gather(
        *[write(idx, page, output_dir) for idx, page in enumerate(data)]
    )
