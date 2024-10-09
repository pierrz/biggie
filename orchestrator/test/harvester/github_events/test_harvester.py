"""
Harvester tests for the Github events section
"""

import pandas as pd
import pytest
from config import harvester_config
from src.harvester.commons.asyncio_operations import download_github_events
from src.harvester.github_events.auth_parameters import github_params
from src.harvester.github_events.github_events_urls import get_events_urls


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
