from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os

# Add your custom module path to sys.path
CASH_FLOW_DIR = '/usr/local/airflow/include/cash_flow'  # Update if different
sys.path.append(CASH_FLOW_DIR)

# Python function that runs your ETL script
def run_elt_python():
    from cash_main import main  # Ensure correct module import
    main()

# Define the DAG
with DAG(
    dag_id='etl_cashflow_python',
    description='Python-based ETL to process and load cash flow data into Snowflake',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,  # Trigger manually or via another DAG
    catchup=False,
    tags=["etl", "cashflow", "snowflake"],
) as dag:

    etl_task = PythonOperator(
        task_id='run_cashflow_etl',
        python_callable=run_etl_python,
    )

