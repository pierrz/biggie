from config import harvester_config
from src.harvester.commons.asyncio_operations import get_url
from src.harvester.commons.errors import APILimitError, GenericError

from .auth_parameters import github_params


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
