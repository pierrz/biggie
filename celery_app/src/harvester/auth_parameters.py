from config import harvester_config

github_params = {
    "Authorization": f"token {harvester_config.TOKEN_GITHUB_API}",
    "Accept": "application/vnd.github+json",
}
