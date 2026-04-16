from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from scripts.pipelines.task import load_locations, load_dates, load_products, load_customers, load_orders


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

generating_location = PythonOperator(
    task_id="generating_location_ids",
    python_callable=load_locations,
    dag=dag
)

generating_dates = PythonOperator(
    task_id="generating_date_ids",
    python_callable=load_dates,
    dag=dag
)

generating_products = PythonOperator(
    task_id="generating_product_ids",
    python_callable=load_products,
    dag=dag
)

generating_customers = PythonOperator(
    task_id='generating_customer_ids',
    python_callable=load_customers,
    op_kwargs={
        "location_ids": "{{ ti.xcom_pull(task_ids='generating_location_ids') }}"
    },
)

generating_orders = PythonOperator(
    task_id='generating_orders',
    python_callable=load_orders,
    op_kwargs={
        "customer_ids": "{{ ti.xcom_pull(task_ids='generating_customer_ids') }}",
        "date_ids": "{{ ti.xcom_pull(task_ids='generating_date_ids') }}",
        "product_ids_with_prices": "{{ ti.xcom_pull(task_ids='generating_product_ids') }}",
        "location_ids": "{{ ti.xcom_pull(task_ids='generating_location_ids') }}"
    },
)

generating_location >> generating_dates >> generating_products >> generating_customers >> generating_orders