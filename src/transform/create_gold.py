from pathlib import Path
from datetime import datetime
from src.utils.logger import logger
import pandas as pd

GOLD_PATH = Path("data/gold")


def create_gold(silver_file):

    df = pd.read_parquet(silver_file)

    total_flights = len(df)

    summary = (
        df.groupby("origin_country")
        .agg(
            active_flights=("icao24", "count"),
            on_ground=("on_ground", "sum"),
            avg_speed=("velocity", "mean"),
            max_speed=("velocity", "max"),
            avg_altitude=("geo_altitude", "mean"),
            max_altitude=("geo_altitude", "max"),
        )
        .reset_index()
    )

    summary["in_air"] = (
        summary["active_flights"] - summary["on_ground"]
    )

    summary["flight_percentage"] = (
        summary["active_flights"] / total_flights * 100
    ).round(2)

    summary["snapshot_time"] = datetime.now()
    summary["pipeline_run"] = datetime.now().strftime("%Y%m%d_%H%M%S")

    summary = summary.sort_values(
        by="active_flights",
        ascending=False
    )

    GOLD_PATH.mkdir(parents=True, exist_ok=True)

    file_path = GOLD_PATH / "flight_summary_latest.parquet"

    summary.to_parquet(file_path, index=False)

    logger.info(f"Gold data saved to: {file_path}")

    return str(file_path)