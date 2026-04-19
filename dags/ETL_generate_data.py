from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from scripts.pipelines.task import export_csv_s3, load_locations, load_dates, load_products, load_customers, load_orders
from scripts.pipelines.task_failure import task_failure_alert


default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2025, 3, 16),
    'retries' : 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': task_failure_alert,
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
    op_kwargs={'count': 50},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_dates = PythonOperator(
    task_id="generating_date_ids",
    python_callable=load_dates,
    op_kwargs={'count': 50},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_products = PythonOperator(
    task_id="generating_product_ids",
    python_callable=load_products,
    op_kwargs={'count': 20},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_customers = PythonOperator(
    task_id='generating_customer_ids',
    python_callable=load_customers,
    op_kwargs={'count': 50},
    provide_context=True,
    sla=timedelta(minutes=10),
    dag=dag
)

generating_orders = PythonOperator(
    task_id='generating_orders',
    python_callable=load_orders,
    op_kwargs={'count': 100},
    provide_context=True,
    sla=timedelta(minutes=15),
    dag=dag
)

# dbt_run = BashOperator(
#     task_id='dbt_run',
#     bash_command='dbt run',
#     sla=timedelta(minutes=10),
#     dag=dag
# )

# dbt_test = BashOperator(
#     task_id='dbt_test',
#     bash_command='dbt test',
#     sla=timedelta(minutes=10),
#     dag=dag
# )

export_top_customers = PythonOperator(
    task_id='export_top_customers_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'top_customers_by_region'},
    dag=dag
)

export_revenue = PythonOperator(
    task_id='export_revenue_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'revenue_by_category'},
    dag=dag
)

export_monthly = PythonOperator(
    task_id='export_monthly_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'monthly_sales'},
    dag=dag
)

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from scripts.pipelines.task import export_csv_s3, load_locations, load_dates, load_products, load_customers, load_orders
from scripts.pipelines.task_failure import task_failure_alert


default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2025, 3, 16),
    'retries' : 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': task_failure_alert,
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
    op_kwargs={'count': 50},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_dates = PythonOperator(
    task_id="generating_date_ids",
    python_callable=load_dates,
    op_kwargs={'count': 50},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_products = PythonOperator(
    task_id="generating_product_ids",
    python_callable=load_products,
    op_kwargs={'count': 20},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_customers = PythonOperator(
    task_id='generating_customer_ids',
    python_callable=load_customers,
    op_kwargs={'count': 50},
    provide_context=True,
    sla=timedelta(minutes=10),
    dag=dag
)

generating_orders = PythonOperator(
    task_id='generating_orders',
    python_callable=load_orders,
    op_kwargs={'count': 100},
    provide_context=True,
    sla=timedelta(minutes=15),
    dag=dag
)

# dbt_run = BashOperator(
#     task_id='dbt_run',
#     bash_command='dbt run',
#     sla=timedelta(minutes=10),
#     dag=dag
# )

# dbt_test = BashOperator(
#     task_id='dbt_test',
#     bash_command='dbt test',
#     sla=timedelta(minutes=10),
#     dag=dag
# )

export_top_customers = PythonOperator(
    task_id='export_top_customers_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'top_customers_by_region'},
    dag=dag
)

export_revenue = PythonOperator(
    task_id='export_revenue_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'revenue_by_category'},
    dag=dag
)

export_monthly = PythonOperator(
    task_id='export_monthly_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'monthly_sales'},
    dag=dag
)

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from scripts.pipelines.task import export_csv_s3, load_locations, load_dates, load_products, load_customers, load_orders
from scripts.pipelines.task_failure import task_failure_alert


default_args = {
    'owner' : 'nf_01',
    "start_date" : datetime(2025, 3, 16),
    'retries' : 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': task_failure_alert,
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
    op_kwargs={'count': 50},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_dates = PythonOperator(
    task_id="generating_date_ids",
    python_callable=load_dates,
    op_kwargs={'count': 50},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_products = PythonOperator(
    task_id="generating_product_ids",
    python_callable=load_products,
    op_kwargs={'count': 20},
    sla=timedelta(minutes=5),
    dag=dag
)

generating_customers = PythonOperator(
    task_id='generating_customer_ids',
    python_callable=load_customers,
    op_kwargs={'count': 50},
    provide_context=True,
    sla=timedelta(minutes=10),
    dag=dag
)

generating_orders = PythonOperator(
    task_id='generating_orders',
    python_callable=load_orders,
    op_kwargs={'count': 100},
    provide_context=True,
    sla=timedelta(minutes=15),
    dag=dag
)

dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='cd /opt/airflow/dbt && dbt run --profiles-dir /opt/airflow/dbt',
    sla=timedelta(minutes=10),
    dag=dag
)

dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='cd /opt/airflow/dbt && dbt test --profiles-dir /opt/airflow/dbt',
    sla=timedelta(minutes=10),
    dag=dag
)

export_top_customers = PythonOperator(
    task_id='export_top_customers_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'top_customers_by_region'},
    dag=dag
)

export_revenue = PythonOperator(
    task_id='export_revenue_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'revenue_by_category'},
    dag=dag
)

export_monthly = PythonOperator(
    task_id='export_monthly_to_s3',
    python_callable=export_csv_s3,
    op_kwargs={'table_name': 'monthly_sales'},
    dag=dag
)

[generating_location, generating_dates, generating_products] \
    >> generating_customers \
    >> generating_orders \
    >> dbt_run \
    >> dbt_test \
    >> [export_top_customers, export_revenue, export_monthly]