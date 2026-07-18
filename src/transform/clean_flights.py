import pandas as pd
from pathlib import Path
from src.utils.logger import logger
import json


COLUMNS = [
    "icao24",
    "callsign",
    "origin_country",
    "time_position",
    "last_contact",
    "longitude",
    "latitude",
    "baro_altitude",
    "on_ground",
    "velocity",
    "true_track",
    "vertical_rate",
    "sensors",
    "geo_altitude",
    "squawk",
    "spi",
    "position_source",
]


def clean_flights(bronze_file):

    print("\n========== SILVER LAYER ==========")

    with open(bronze_file, "r") as f:
        data = json.load(f)

    flights = data["states"]

    df = pd.DataFrame(flights, columns=COLUMNS)

    df = df.drop(columns=["sensors"])
    df = df.dropna(subset=["latitude", "longitude"])
    df = df.drop_duplicates()
    df["callsign"] = df["callsign"].str.strip()
    df["time_position"] = pd.to_datetime(
    df["time_position"],
    unit="s",
    errors="coerce"
)

    df["last_contact"] = pd.to_datetime(
    df["last_contact"],
    unit="s"
)
    
    SILVER_PATH = Path("data/silver")
    SILVER_PATH.mkdir(parents=True, exist_ok=True)

    silver_path = SILVER_PATH / "flights_latest.parquet"

    df.to_parquet(silver_path, index=False)

    logger.info(f"Silver data saved to: {silver_path}")

    print(df.head())

    print("\nRows:", len(df))
    print("Columns:", len(df.columns))
    print("\n========== DATA TYPES ==========")
    print(df.dtypes)

    print("\n========== MISSING VALUES ==========")
    print(df.isnull().sum())

    print("\n========== DUPLICATE ROWS ==========")
    print(df.duplicated().sum())

    print("\n========== NUMERIC SUMMARY ==========")
    print(df.describe())

    return str(silver_path)