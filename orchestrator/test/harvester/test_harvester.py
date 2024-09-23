"""
Harvester tests
"""

import os
import shutil
from pathlib import Path

import pandas as pd
import pytest
from config import data_directories, harvester_config
from src.commons.utils import load_json  # pylint: disable=E0611
from src.harvester.asyncio_operations import (
    download_github_events,
    download_passthrough,
    get_url,
    write_aio,
    write_with_id,
)
from src.harvester.auth_parameters import github_params
from src.harvester.github_events_urls import get_events_urls


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


@pytest.mark.asyncio
async def test_asyncio_download_github_events_unfiltered_records():
    """
    Tests the asyncio loop download function
    :return: does its thing
    :return:
    """

    event_urls = await get_events_urls()
    unfiltered_json_data = await download_github_events(
        event_urls, filtered=False, auth=github_params, mode="json"
    )
    array = unfiltered_json_data.pop(0)  # keep only 1st page ?
    for idx, part in enumerate(unfiltered_json_data):
        array += part
    count = len(array)

    try:
        assert len(array) == len(event_urls) * harvester_config.PER_PAGE
    except AssertionError:
        # sometimes the last page is not full ...
        assert (
            (len(event_urls) - 1) * (harvester_config.PER_PAGE)
            < count
            < len(event_urls) * harvester_config.PER_PAGE
        )


@pytest.mark.asyncio
async def test_asyncio_download_github_events_filtered_df():
    """
    Tests the asyncio loop download function
    :return: does its thing
    :return:
    """

    event_urls = await get_events_urls()
    df_list = await download_github_events(
        event_urls, output="df", auth=github_params, mode="json"
    )
    grouped_series = pd.concat(df_list).groupby(["type"]).size()

    try:
        columns = sorted(grouped_series.index.to_list())
        assert columns == harvester_config.EVENTS
    # sometimes 1 event type is missing from the tested batch, hence test each type individually
    except AssertionError:
        for event in columns:
            assert event in harvester_config.EVENTS

    # there should always be at least 1 entry from the required events
    valid_data_check = grouped_series.gt(0).any()
    assert valid_data_check
