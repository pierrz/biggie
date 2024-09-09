from typing import Iterable, Tuple

import pandas as pd
from src import logger


def dataframe_info_log(pairs: Iterable[Tuple[str, pd.DataFrame]]):
    """Celery logs with basic dataframe overview
    :param pairs: list of pairs name/dataframe
    """
    for pair in pairs:
        name, df = pair
        logger.info(
            "'{}' dataframe with {} columns and {} rows".format(name, *df.shape)
        )
        logger.info(df.head(5))
