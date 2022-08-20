"""
Module gathering all the code from Guilherme's notebook.
"""

import os
from datetime import datetime, timezone
from pathlib import Path, PurePath

import pandas as pd
from config import data_directories
from src.commons import names as ns

output_dir = data_directories.github_out


def requests_meta():
    timestamp = datetime.now(timezone.utc).isoformat()
    refugees_url = "https://data.unhcr.org/population/get/timeseries?widget_id=324084&sv_id=54&population_group=5460&frequency=day&fromDate=1900-01-01"
    refugees_filepath = Path(ns.refugees, timestamp, f"{ns.refugees}.json")
    idps_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQIdedbZz0ehRC0b4fsWiP14R7MdtU1mpmwAkuXUPElSah2AWCURKGALFDuHjvyJUL8vzZAt3R1B5qg/pub?output=csv"
    idps_filepath = Path(ns.idps, timestamp, f"{ns.idps}.csv")
    refugees_by_country_urls, refugees_by_country_paths = get_refugees_by_country_data(
        timestamp
    )
    return (refugees_url, idps_url, *refugees_by_country_urls), (
        refugees_filepath,
        idps_filepath,
        *refugees_by_country_paths,
    )


def get_refugees_df(dir_path):
    df = pd.read_json(Path(dir_path, f"{ns.refugees}.json"))
    timeseries = df.iloc[1]["data"]
    refugees = pd.DataFrame(timeseries)
    return refugees


def get_idp_df(dir_path):
    idps = pd.read_csv(Path(dir_path, f"{ns.idps}.csv"), skiprows=1)
    return idps[["IDPs", "Date", "Source URL"]]


def get_refugees_by_country_data(timestamp):

    countries_ids = {
        "Belarus": 595,
        "Russia": 718,
        "Moldova": 680,
        "Poland": 712,
        "Hungary": 649,
        "Slovakia": 734,
        "Romania": 716,
    }

    urls = []
    filepaths = []
    for key, value in countries_ids.items():
        urls.append(
            "https://data.unhcr.org/population/get/timeseries?"
            f"widget_id=319134&geo_id={value}&sv_id=54&population_group=5457"
            "&frequency=day&fromDate=2022-02-01"
        )
        filepaths.append(Path(ns.countries, timestamp, f"{key}.json"))

    return urls, filepaths


def get_refugees_by_country_df(dir_path):

    df_list = []
    for path in os.scandir(dir_path):
        df = pd.read_json(path)
        country_series = df.loc["timeseries"]["data"]
        refugee_df = pd.DataFrame(country_series)
        refugee_df["origin_country"] = PurePath(path).stem
        df_list.append(refugee_df)

    refugees_by_country = pd.concat(df_list)
    return refugees_by_country
