from sqlalchemy import create_engine
import pandas as pd
from src.utils.logger import logger

DATABASE_URL = "postgresql+psycopg2://postgres:postgres@host.docker.internal:5432/flights_db"

engine = create_engine(DATABASE_URL)


def load_to_postgres(gold_file):

    df = pd.read_parquet(gold_file)

    df.to_sql(
        name="flight_summary",
        con=engine,
        if_exists="append",
        index=False
    )

    logger.info("Gold data loaded into PostgreSQL.")