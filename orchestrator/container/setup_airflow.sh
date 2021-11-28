#!/bin/bash 

mkdir ./dags ./logs ./plugins
echo "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env
docker-compose up airflow-init
docker-compose up -d