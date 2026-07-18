from datetime import datetime

import sys

sys.path.append("/opt/airflow")

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.extract.get_flights import extract_flights
from src.transform.clean_flights import clean_flights
from src.transform.create_gold import create_gold
from src.load.load_postgres import load_to_postgres


def run_clean_flights(ti):
    bronze_file = ti.xcom_pull(task_ids="extract_flights")
    return clean_flights(bronze_file)


def run_create_gold(ti):
    silver_file = ti.xcom_pull(task_ids="clean_flights")
    return create_gold(silver_file)


def run_load_postgres(ti):
    gold_file = ti.xcom_pull(task_ids="create_gold")
    return load_to_postgres(gold_file)


with DAG(
    dag_id="flight_pipeline",
    start_date=datetime(2026, 7, 18),
    schedule="*/5 * * * *",
    catchup=False,
) as dag:

    extract_task = PythonOperator(
        task_id="extract_flights",
        python_callable=extract_flights,
    )

    clean_task = PythonOperator(
        task_id="clean_flights",
        python_callable=run_clean_flights,
    )

    gold_task = PythonOperator(
        task_id="create_gold",
        python_callable=run_create_gold,
    )

    load_task = PythonOperator(
        task_id="load_postgres",
        python_callable=run_load_postgres,
    )

    extract_task >> clean_task >> gold_task >> load_task