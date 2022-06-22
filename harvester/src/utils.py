"""
Module containing core functions
"""

from typing import Iterable, Tuple

from config import harvester_config

# pylint: disable=C0103
characters_api_url = "http://gateway.marvel.com/v1/public/characters?"


def get_auth() -> str:
    """
    Generates the url authentication trail
    :return: the url authentication trail
    """
    timestamp, key_hash = harvester_config.generate_auth_parts()
    auth_combination = (
        f"ts={timestamp}&apikey={harvester_config.API_PUBLIC_KEY}&hash={key_hash}"
    )
    return auth_combination


def get_meta(meta) -> Tuple[int, Iterable[str]]:
    """
    From the 1st response header, gathers the total of rows and the URLs to call to fetch all the related data
    :param meta: the 1st response header useful metadata
    :return: the total of rows and the list of URLs
    """

    limit = 100
    n_pages = int(meta["total"] / limit)
    if meta["total"] % limit > 0:
        n_pages += 1

    urls = []
    for page in list(range(n_pages)):
        urls.append(
            f"{characters_api_url}{get_auth()}&offset={page * limit}&limit={limit}"
        )

    return meta["total"], urls
