import pickle
from datetime import datetime
from logger import logging

import pandas as pd
import numpy as np

from app.models import Cyclone

def classify(data):
    logging.info("starting machine learning classification")

    # load ML model
    # the weights contains the pre-processing step
    logging.info("loading machine learning model's weights")
    with open("base_best_model_rfr.pkl", "rb") as f:
        loaded_model = pickle.load(f)

    # categorizing
    logging.info("categorizing new data")

    answer = ""

    return answer


def check_form_submit(data):

    logging.debug("checking form submit content")
    logging.debug(data)
    logging.debug(type(data))
    logging.debug(data["season"])
    logging.debug(type(data["season"]))

    # wind
    logging.debug("checking wind")

    if type(data["wind"]) is not int:
        raise ValueError("Wind needs to be a number")

    logging.debug("checking season")

    # season
    try:
        datetime.strptime(data["season"], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise ValueError(
            "Invalid date format for season. Expected 'YYYY-MM-DD HH:MM:SS'."
        )

    # basin
    logging.debug("checking basin")

    basin_list = ["NA", "EP", "WP", "NI", "SI", "SP", "SA"]
    if data["basin"].upper() not in basin_list:
        raise ValueError("Basin input invalid")

    # nature
    logging.debug("checking nature")

    nature_list = ["DS", "TS", "ET", "SS", "NR", "MX"]
    if data["nature"].upper() not in nature_list:
        raise ValueError("Nature input invalid")

    # latitude
    logging.debug("checking latitude")

    if type(data["latitude"]) is not int:
        raise ValueError("Latitude needs to be an integer")

    # longitude
    logging.debug("checking longitude")

    if type(data["longitude"]) is not int:
        raise ValueError("longitude needs to be an integer")

    # dist2land
    logging.debug("checking dist2land")

    if type(data["dist2land"]) is not int:
        raise ValueError("The distance to land needs to be an integer")

    # storm_speed
    logging.debug("checking storm_speed")

    if type(data["storm_speed"]) is not int:
        raise ValueError("The storm speed needs to be an integer")

    # storm_dir
    logging.debug("checking storm_dir")

    if type(data["storm_dir"]) is not int:
        raise ValueError("The storm direction needs to be an integer")

    logging.debug("form submit checked")


def populate_database():
    logging.debug("populating the database")

    df = pd.read_parquet("../data/app_db.parquet", engine="pyarrow")

    # Get the most recent row for each ID
    latest_rows = df.sort_values('ISO_TIME', ascending=False).drop_duplicates(subset='SID')

    # Select the top 10 most recent IDs
    top_10_ids = latest_rows.nlargest(10, 'ISO_TIME')['SID']

    # Filter all rows corresponding to these IDs
    result_df = df[df['SID'].isin(top_10_ids)]

    logging.debug("inserting into database")

    for _, row in result_df.iterrows():    
    
        Cyclone.objects.create(
            cyclone_id=row["SID"],
            season=datetime.strftime(row["ISO_TIME"], "%Y-%m-%d %H:%M:%S"),
            basin=row["BASIN"],
            nature=row["NATURE"],
            latitude=row["LAT"],
            longitude=row["LON"],
            wind=row["WIND"],
            dist2land=row["DIST2LAND"],
            storm_dir=row["STORM_SPEED"],
            storm_speed=row["STORM_DIR"],
            stage=row["TD9636_STAGE"]
        )

    logging.debug("Database populated")
