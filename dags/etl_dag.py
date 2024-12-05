from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

default_args = {
    "owner" : "Abdul_Hanan_Nawaz",
    "retries": 5,
    "retry_delay":  timedelta(seconds=60)
}

etl_dag = DAG(
    'etl_aqi_pakistan_v01',
    default_args=default_args,
    start_date= datetime(2024, 12, 1),
    schedule_interval= "0 7 * * *"
)

def extraction_start():
    print("**** Extraction Begins ****")

def extraction_end():
    print("**** Extraction Ends ****")

extraction_begin = PythonOperator(
    task_id = 'extraction_begin',
    python_callable = extraction_start,
    dag = etl_dag
)

extraction_under_progress = BashOperator(
    task_id = 'extract_from_api',
    bash_command = 'python3 /Users/hanan-nawaz/Documents/Projects/Pakistan_AQI_Analysis/etl/etl.py',
    retries = 3,  # Max retries before failing
    retry_delay = timedelta(minutes=5),  # Wait 5 minutes between retries
    execution_timeout = timedelta(minutes=30),  # Max time for task execution
    dag = etl_dag
    )

extraction_complete = PythonOperator(
    task_id = 'extraction_end',
    python_callable = extraction_end,
    dag = etl_dag
)

extraction_begin >> extraction_under_progress >> extraction_complete
