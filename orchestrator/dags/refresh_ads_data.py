# DEFAULT LIBRARIES
from datetime import timedelta

from airflow import DAG
from airflow.models import Variable
from airflow.operators.python import PythonOperator, PythonVirtualenvOperator

from airflow.utils.dates import days_ago

# SCRAPE SCRIPTS
import boto3 as bt3

boto3 = bt3.Session(
    region_name = Variable.get("AWS_REGION"), 
    aws_access_key_id=Variable.get("ACCESS_ID"), 
    aws_secret_access_key=Variable.get("ACCESS_KEY")
)

s3_resource = boto3.resource('s3')

bucket = s3_resource.Bucket('xox-functions')
functions_files = bucket.objects.all()
functions_files = [f.key for f in functions_files]

s3 = boto3.client('s3')
for file in functions_files:
    s3.download_file('xox-functions', file, file)

import fetch_ads_links
import change_data_capture
import fetch_ads_data
import clean_ads_data
import load_into_database

# SETUP DAG
with DAG(
    dag_id='refresh_ads_data',
    default_args={
        'owner': 'marcio',
        'depends_on_past': False,
        'email': ['delucasmarcio@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False,
    },
    dagrun_timeout=timedelta(hours=1),
    start_date=days_ago(1),
    schedule_interval='@daily',
    tags=['xurastei'],
) as dag:
    fetch_ads_links = PythonOperator(
        task_id='fetch_ads_links',
        python_callable=fetch_ads_links.handler,
        op_kwargs={"AWS_REGION" : Variable.get("AWS_REGION"),"ACCESS_ID" : Variable.get("ACCESS_ID"),"ACCESS_KEY" : Variable.get("ACCESS_KEY")}
    )

    change_data_capture = PythonOperator(
        task_id='change_data_capture',
        python_callable=change_data_capture.handler,
        op_kwargs={"AWS_REGION" : Variable.get("AWS_REGION"),"ACCESS_ID" : Variable.get("ACCESS_ID"),"ACCESS_KEY" : Variable.get("ACCESS_KEY")}
    )

    fetch_ads_data = PythonOperator(
        task_id='fetch_ads_data',
        python_callable=fetch_ads_data.handler,
        op_kwargs={"AWS_REGION" : Variable.get("AWS_REGION"),"ACCESS_ID" : Variable.get("ACCESS_ID"),"ACCESS_KEY" : Variable.get("ACCESS_KEY")}
    )

    clean_ads_data = PythonOperator(
        task_id='clean_ads_data',
        python_callable=clean_ads_data.handler,
        op_kwargs={"AWS_REGION" : Variable.get("AWS_REGION"),"ACCESS_ID" : Variable.get("ACCESS_ID"),"ACCESS_KEY" : Variable.get("ACCESS_KEY")}
    )
    
    load_into_database = PythonOperator(
        task_id='load_into_database',
        python_callable=load_into_database.handler,
        op_kwargs={"AWS_REGION" : Variable.get("AWS_REGION"),"ACCESS_ID" : Variable.get("ACCESS_ID"),"ACCESS_KEY" : Variable.get("ACCESS_KEY"),"RDS_DATABASE" : Variable.get("RDS_DATABASE"),"RDS_USER" : Variable.get("RDS_USER"),"RDS_PASSWORD" : Variable.get("RDS_PASSWORD"),"RDS_HOST" : Variable.get("RDS_HOST"),"RDS_PORT" : Variable.get("RDS_PORT")}
    )

    fetch_ads_links >> change_data_capture >> fetch_ads_data >> clean_ads_data >> load_into_database