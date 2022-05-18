from config import app_config

characters_api_url = "http://gateway.marvel.com/v1/public/characters?"


def get_auth():
    timestamp, key_hash = app_config.generate_auth_parts()
    auth_combination = (
        f"ts={timestamp}&apikey={app_config.API_PUBLIC_KEY}&hash={key_hash}"
    )
    return auth_combination


def get_meta(meta):

    limit = 100
    n = meta["total"] / limit

    if meta["total"] % limit > 0:
        n = int(n) + 1
    else:
        n = int(n)

    urls = []
    for page in list(range(n)):
        urls.append(
            f"{characters_api_url}{get_auth()}&offset={page * limit}&limit={limit}"
        )

    return meta["total"], urls
