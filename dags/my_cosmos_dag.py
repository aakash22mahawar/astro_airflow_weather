from datetime import datetime
import os
from cosmos import DbtDag, ProjectConfig, ProfileConfig, ExecutionConfig
from cosmos.profiles import SnowflakeUserPasswordProfileMapping,SnowflakePrivateKeyPemProfileMapping
from pathlib import Path

dbt_project_path = Path("/usr/local/airflow/include/weather_project") #this is actually docker container path where target project is located

profile_config = ProfileConfig(
    profile_name="fivetran_project",
    target_name="PROD",
    profile_mapping=SnowflakePrivateKeyPemProfileMapping(
        conn_id="snowflake_default",
        profile_args={
            "database": "FIVETRAN",
            "schema": "GOOGLE_SHEETS",
            "user": "AAKASH_MAHAWAR"  # Matches "login" in Airflow conn
        }
    )
)

dbt_snowflake_dag = DbtDag(
    project_config=ProjectConfig(dbt_project_path),
    operator_args={"install_deps": True},
    profile_config=profile_config,
    execution_config=ExecutionConfig(
        dbt_executable_path=f"{os.environ['AIRFLOW_HOME']}/dbt_venv/bin/dbt"
    ),
    schedule_interval=None,
    start_date=datetime(2023, 9, 10),
    catchup=False,
    dag_id="dbt_snowflake_dag"
)

