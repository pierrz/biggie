import subprocess

from worker import celery, logger


@celery.task(name="run-harvester-container")
def run_harvester_container():
    """
    """
    logger.info("-- START --")
    subprocess.run(["docker", "run", "-it", "ghcr.io/pierrz/biggie_harvester_img:latest", "python3", "-m", "__init__"])
