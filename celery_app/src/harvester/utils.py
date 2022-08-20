"""
Module containing core functions
"""

from typing import Dict

import aiohttp
from config import harvester_config  # TEST_MODE,
# if TEST_MODE:
from src.harvester.auth_parameters import github_params
from src.harvester.errors import APILimitError, GenericError


async def get_url(auth: Dict = None, **kwargs):

    url = kwargs["url"]
    print(f"Start downloading {url}")
    try:
        async with aiohttp.ClientSession() as client:

            if isinstance(auth, Dict):
                print(f"=> Authenticated call: {auth}")
                response = await client.get(url, headers=auth)

            else:
                response = await client.get(url)
            print(f"Done downloading {url}")

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
            # print(status)
            # print(headers)
            # # return (status, headers)
            # return response

    except KeyError as e:
        APILimitError(e)
    except Exception as e:
        GenericError(e)


async def get_events_urls():

    base_url = f"https://api.github.com/events?per_page={harvester_config.PER_PAGE}"
    response = await get_url(url=base_url, auth=github_params, mode="response")
    try:
        last_page = int(str(response.links["last"]["url"])[-1])
        urls = []
        for page in list(range(1, last_page + 1)):
            url = f"{base_url}&page={page}"
            urls.append(url)

        return urls

    except KeyError as e:
        APILimitError(e)
    except Exception as e:
        GenericError(e)
