"""
Module dedicated to FastAPI endpoints testing
"""

from test.base_test import EndpointTestBase  # pylint: disable=E0611

import pytest
from fastapi.testclient import TestClient


def test_endpoint_dummy(client: TestClient):
    """
    Test if the api is up
    :param client: current FastAPI test client
    :return: does its thing
    """
    EndpointTestBase(client, "live/dummy")


@pytest.mark.skip(reason="data endpoint are dependent on 'live' (e.g. changing) data")
def test_data_from_api(client: TestClient):  # pylint: disable=W0613
    """wip"""
