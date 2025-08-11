from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
import os
from pathlib import Path

# Cosmos imports
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakePrivateKeyPemProfileMapping

# ──────────────────────────────
# Step 1: Python ELT Task
# ──────────────────────────────
# Add your custom module path to sys.path
weather_api_dir = '/usr/local/airflow/include/weather_api'  # Path in container
sys.path.append(weather_api_dir)

def run_elt_python():
    from load import load_to_snowflake
    load_to_snowflake()

# ──────────────────────────────
# Step 2: dbt TaskGroup Configuration
# ──────────────────────────────
dbt_project_path = Path("/usr/local/airflow/include/weather_project")  # in container

profile_config = ProfileConfig(
    profile_name="fivetran_project",
    target_name="PROD",
    profile_mapping=SnowflakePrivateKeyPemProfileMapping(
        conn_id="snowflake_default",
        profile_args={
            "database": "FIVETRAN",
            "schema": "GOOGLE_SHEETS",
            "user": "AAKASH_MAHAWAR"
        }
    )
)

# ──────────────────────────────
# Final Combined DAG
# ──────────────────────────────
with DAG(
    dag_id="elt_weather_and_dbt_pipeline",
    description="ELT weather data into Snowflake, then dbt transformations",
    start_date=datetime(2024, 1, 1),
    schedule_interval="*/30 * * * *",  # Every 30 minutes
    catchup=False,
    tags=["elt", "dbt", "snowflake", "weather"],
) as dag:

    # Step 1: Python ELT Task
    etl_task = PythonOperator(
        task_id="run_weather_elt",
        python_callable=run_elt_python,
    )

    # Step 2: dbt TaskGroup
    dbt_group = DbtTaskGroup(
        group_id="dbt_transformations",
        project_config=ProjectConfig(dbt_project_path),
        profile_config=profile_config,
        execution_config=ExecutionConfig(
            dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
        ),
        operator_args={"install_deps": True},
    )

    # Orchestration: ELT → dbt
    etl_task >> dbt_group

