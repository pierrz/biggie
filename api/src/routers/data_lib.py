import numpy as np
import pandas as pd


def dataframe_from_mongo_data(db_data, sort_by: str = None):
    """
    Prepares the data retrieved from Mongo to be compliant with pd.DataFrame and JSONResponse
    :param db_data: data retrieved from Mongo
    :param sort_by: the column to sort the dataframe with
    :return: the prepared/cleaned dataframe
    """

    raw_df = pd.DataFrame(db_data)
    if raw_df.shape[0] > 1:  # at least 2 rows to get an interval
        raw_df.drop(columns=["_id"])
        # drop_duplicates to cover potential overlaps from the GitHub events API
        clean_df = raw_df.drop_duplicates().replace(to_replace=[np.nan], value=[""])

        if sort_by is None:
            return clean_df
        return clean_df.sort_values(by=sort_by)

    return None
