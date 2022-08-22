"""
Harvests paginated data from the GitHub Events API
"""

import asyncio
import os
import time
from pathlib import Path
from typing import List

import pandas as pd
from config import data_directories
from src.commons import names as ns
from src.commons.logs import dataframe_info_log
from src.db.postgres import pg_engine
from src.harvester.asyncio_operations import download_passthrough, write_aio
from src.harvester.get_poc_input_data import (get_idp_df,
                                              get_refugees_by_country_df,
                                              get_refugees_df, requests_meta)
from src.pyspark.jobs import ToPostgresFromVA
from src.pyspark.postgres_connectors import PostgresReader
from worker import celery, logger

input_dir = data_directories.ukr_dp


def prepare_dataframes() -> List[pd.DataFrame]:
    last_timestamp = sorted(os.listdir(Path(input_dir, ns.refugees)), reverse=True)[0]

    refugees_df = get_refugees_df(Path(input_dir, ns.refugees, last_timestamp))
    idps_df = get_idp_df(Path(input_dir, ns.idps, last_timestamp))
    refugees_by_country_df = get_refugees_by_country_df(
        Path(input_dir, ns.countries, last_timestamp)
    )

    names = [ns.refugees, ns.idps, ns.countries]
    df_list = [refugees_df, idps_df, refugees_by_country_df]
    dataframe_info_log(zip(names, df_list))
    return df_list


def load_pg(dfs_list):
    zips = list(zip(dfs_list, [ns.refugees, ns.idps, ns.countries]))
    logger.info("Loading data into Postgres ...")
    for pack in zips:
        df, name = pack
        df.to_sql(f"{name}_view", con=pg_engine)
    logger.info("=> data loaded")


def load_pg_with_spark(dfs_list):
    zips = list(zip(dfs_list, [ns.refugees, ns.idps, ns.countries]))
    logger.info("Initiating data loading task to Postgres ...")
    for pack in zips:
        df, table = pack
        try:

            if table == "idps":     # issue with specific column (2 types in it)
                df = df.astype({"Source URL": "str"})

            ToPostgresFromVA(dataframe=df,
                             table=table,
                             check_columns=list(df.columns),
                             reader_class=PostgresReader)
            logger.info(f"=> Data loaded successfully for table {table}.")

        except Exception as e:
            print(e)
            print("Issue with the data ...")


@celery.task(name="ukr-dp-data-acquisition")
def run_ukr_dp_da():
    """
    Starts the whole module
    """

    try:

        urls, filepaths = requests_meta()
        logger.info(f"Retrieved {len(urls)} urls")

        if len(urls) == len(filepaths):

            # check/create data directories
            for dir in [ns.refugees, ns.idps, ns.countries]:
                dir_path = Path(input_dir, dir)
                if not dir_path.exists():
                    dir_path.mkdir(parents=True)

            # get data
            start_time = time.time()
            data_array = asyncio.run(download_passthrough(urls, filepaths=filepaths))
            asyncio.run(write_aio(data_array=data_array, output_dir=input_dir))
            logger.info(
                f"Getting and saving data locally took {time.time() - start_time} seconds"
            )

            # data -> postgres
            dfs_list = prepare_dataframes()
            # load_pg(dfs_list)
            load_pg_with_spark(dfs_list)

        else:
            logger.info("Issue with gathering the metadata ...")

    except Exception as exception:  # pylint: disable=W0703
        logger.info(exception)
