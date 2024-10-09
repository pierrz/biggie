"""
Harvester tests
"""

import os
import shutil
from pathlib import Path

import pytest
from config import data_directories
from src.commons.utils import load_json  # pylint: disable=E0611
from src.harvester.commons.asyncio_operations import (
    download_passthrough,
    get_url,
    write_aio,
    write_with_id,
)


@pytest.mark.asyncio
async def test_download_sample(dog_sample_urls):
    """
    Tests the download function onto a basic url
    :return: does its thing
    """

    response = await get_url(url=dog_sample_urls["test"], mode="response")
    async with response:
        data = await response.json()
        assert response.status == 200
        assert data["message"].startswith(dog_sample_urls["result-url-prefix"])
        assert data["status"] == "success"


@pytest.mark.asyncio
async def test_write_data_to_file(json_sample_dict):
    """
    Tests the write function
    :return: does its thing
    """

    filename = "write-test.json"
    await write_with_id(
        id=json_sample_dict["id"],
        data=json_sample_dict,
        timestamp="1984-12-31T07:59",
        filepath=filename,
    )

    test_filepath = Path(data_directories.batch, filename)
    assert test_filepath.exists()
    assert json_sample_dict == load_json(test_filepath)
    os.remove(test_filepath)


@pytest.mark.asyncio
async def test_asyncio_write_loop(json_array_dict, test_dir):
    """
    Tests the asyncio loop write function
    :return: does its thing
    """

    test_dir.mkdir(parents=True, exist_ok=True)
    await write_aio(json_array_dict, output_dir=test_dir)

    assert len(list(os.scandir(test_dir))) == len(json_array_dict)
    shutil.rmtree(test_dir)


@pytest.mark.asyncio
async def test_asyncio_download_loop(dog_sample_urls):
    """
    Tests the asyncio loop download function
    :return: does its thing
    :return:
    """

    size = 3
    test_urls = [dog_sample_urls["test"]] * size

    # todo: retrieve only the response
    results = await download_passthrough(test_urls, mode="json")
    status = [part["status"] for part in results]
    messages = [
        part["message"].startswith(dog_sample_urls["result-url-prefix"])
        for part in results
    ]

    assert len(results) == size
    assert status == ["success"] * size
    assert messages == [True] * size
