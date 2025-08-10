from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Add your custom module path to sys.path
weather_api_dir = '/usr/local/airflow/include/weather_api'  # Update if different
sys.path.append(weather_api_dir)

# Python function that runs your ELT script
def run_elt_python():
    from load import load_to_snowflake  # Ensure correct module import
    load_to_snowflake()

# Define the DAG
with DAG(
    dag_id='elt_weather_python',
    description='Python-based ELT to process and weather data into Snowflake',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Trigger manually or via another DAG
    catchup=False,
    tags=["elt", "weather", "snowflake"],
) as dag:

    etl_task = PythonOperator(
        task_id='run_weather_elt',
        python_callable=run_elt_python,
    )

