from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.load_data import Pipeline 


def run_pipeline():
    print("Pipeline started...")
    A = Pipeline()
    A.run(records=5)
    print("✅ Pipeline finished")


default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2025, 3, 16),
    'retries' : 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    dag_id='ecommerce_gen_data',
    description='Generating data for vault_db',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False
)

generating_location_ids = PythonOperator(
    task_id="generating_location_ids",
    python_callable=run_pipeline,
    dag=dag
)

generating_location_ids