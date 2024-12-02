from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

import sys
sys.path.insert(0, '/Users/hanan-nawaz/Documents/Projects/Pakistan_AQI_Analysis')
from etl.extract import main as main_extract

default_args = {
    "owner" : "Abdul_Hanan_Nawaz",
    "retries": 5,
    "retry_delay":  timedelta(seconds=60)
}

etl_dag = DAG(
    'etl_open_weather',
    default_args=default_args,
    start_date= datetime(2024, 12, 1),
    schedule_interval= "0 7 * * *"
)

extract_task = PythonOperator(
    task_id = 'extract_from_api',
    python_callable= main_extract,
    retries=3,  # Max retries before failing
    retry_delay=timedelta(minutes=5),  # Wait 5 minutes between retries
    execution_timeout=timedelta(minutes=30),  # Max time for task execution
    dag=etl_dag
    )

extract_task
