"""
Harvester tests
"""

import os
import shutil
from pathlib import Path

import pytest

from harvester.config import harvester_config
from harvester.src.asyncio_operations import (download_aio,
                                              download_marvel_api_test,
                                              download_test, write, write_aio)
from harvester.src.json_utils import load_json  # pylint: disable=E0611
from harvester.src.utils import get_auth


@pytest.mark.asyncio
async def test_download_sample():
    """
    Tests the download function onto a basic url
    :return: does its thing
    """

    url = "https://dog.ceo/api/breeds/image/random"
    response = await download_test(url)

    assert response["message"].startswith("https://images.dog.ceo/breeds")
    assert response["status"] == "success"


@pytest.mark.asyncio
async def test_download_from_marvel_api(stan_lee_baseurl):
    """
    Tests the download function onto a Marvel API url
    :return: does its thing
    """
    # results, meta = await download_marvel_api(f"{stan_lee_baseurl}{get_auth()}")
    results, meta = await download_marvel_api_test(f"{stan_lee_baseurl}{get_auth()}")

    assert meta["code"] == 200
    assert results[0]["fullName"] == "Stan Lee"
    assert (
        results[0]["resourceURI"] == "http://gateway.marvel.com/v1/public/creators/30"
    )


@pytest.mark.asyncio
async def test_write_data_to_file(json_sample_dict):
    """
    Tests the write function
    :return: does its thing
    """

    if not harvester_config.OUTPUT_DIR.exists():
        os.mkdir(harvester_config.OUTPUT_DIR)

    filepath = Path(harvester_config.OUTPUT_DIR, "write-test.json")
    await write(11, json_sample_dict, path=filepath)

    assert filepath.exists()
    assert json_sample_dict == load_json(filepath)
    os.remove(filepath)


@pytest.mark.asyncio
async def test_asyncio_write_loop(json_array_dict):
    """
    Tests the asyncio loop write function
    :return: does its thing
    """

    test_output_dir = Path(harvester_config.OUTPUT_DIR, "test")
    os.mkdir(test_output_dir)
    await write_aio(json_array_dict, test_output_dir)

    assert len(list(os.scandir(test_output_dir))) == len(json_array_dict)
    shutil.rmtree(test_output_dir)


@pytest.mark.asyncio
async def test_asyncio_download_loop(stan_lee_baseurl):
    """
    Tests the asyncio loop download function
    :return: does its thing
    :return:
    """

    test_urls = []
    size = 3
    i = 0

    while i < size:     # iteration to regenerate the auth parameters
        test_urls.append(f"{stan_lee_baseurl}{get_auth()}")
        i += 1

    results = await download_aio(test_urls)

    assert len(results) == size
