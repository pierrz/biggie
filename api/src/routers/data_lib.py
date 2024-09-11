from typing import List, Type

import numpy as np
import pandas as pd
from pydantic import BaseModel
from pymongo.command_cursor import CommandCursor


def dataframe_from_mongo_data(
    db_data: CommandCursor, sort_by: str = None
) -> pd.DataFrame:
    """
    Prepares the data retrieved from Mongo to be compliant with pd.DataFrame and JSONResponse
    :param db_data: data retrieved from Mongo
    :param sort_by: the column to sort the dataframe with
    :return: the prepared/cleaned pandas dataframe
    """

    raw_df = pd.DataFrame(db_data)
    clean_df = raw_df.drop_duplicates().replace(to_replace=[np.nan], value=[""])
    if sort_by is None:
        return clean_df
    return clean_df.sort_values(by=sort_by)


def validate_data(data: CommandCursor, model: Type[BaseModel]) -> List[BaseModel]:
    """
    Validate data (from Postgres or Mongo) based on a specific Pydantic model.
    Convert the validated data into a list to pass it into Pandas later on.
    :return: a list of instances of Pydantic models
    """

    valid_data = [model(**doc).dict() for doc in data]
    return valid_data
