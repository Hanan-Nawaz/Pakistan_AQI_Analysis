from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator

default_args = {
    "owner" : "Abdul_Hanan_Nawaz",
    "retries": 5,
    "retry_delay":  timedelta(seconds=60)
}

etl_dag = DAG(
    'etl_open_weather',
    default_args=default_args,
    start_date= datetime(2024, 12, 1),
    schedule_interval= "0 7 * * 6"
)

def greet():
    print("Good Morning ! Mr. Hanan")

extract_task = PythonOperator(
    task_id = 'extract_from_api',
    python_callable= greet,
    dag=etl_dag
)

extract_task
