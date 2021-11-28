# LOAD CREDENTIALS
import json

import boto3 as bt3

import psycopg2

import pandas as pd
import numpy as np
from pandasql import sqldf

def handler(input_path = 'xox-ad-silver',input_file = 'olx_imoveis_silver',AWS_REGION=None,ACCESS_ID=None,ACCESS_KEY=None,RDS_DATABASE=None,RDS_USER=None,RDS_PASSWORD=None,RDS_HOST=None,RDS_PORT=None):
    """
    Function to fetch neighborhood data, clustering and find types of location.

    Params:
    - user            : PostgreSQL' user.
    - password        : PostgreSQL' password.
    - host            : PostgreSQL' endpoint. 
    """
    
    # SETUP CONNECTION
    boto3 = bt3.Session(
        region_name = AWS_REGION, 
        aws_access_key_id = ACCESS_ID, 
        aws_secret_access_key = ACCESS_KEY
    )

    conn = psycopg2.connect(
        database=RDS_DATABASE,
        user=RDS_USER,
        password=RDS_PASSWORD,
        host=RDS_HOST,
        port=RDS_PORT
    )

    cur = conn.cursor()

    # IMPORT DATA
    s3 = boto3.client('s3')
    with open(f"/home/airflow/{input_file}.csv", 'wb') as f:
        s3.download_fileobj(input_path, f"{input_file}.csv", f)

    data = pd.read_csv(f"/home/airflow/{input_file}.csv",sep = '\t',encoding='UTF-8')

    # FIXING COLUMN ORDER
    cols = [
        'TITULO','VALOR','DESCRICAO','MUNICIPIO','BAIRRO','CEP','LOGRADOURO','CATEGORIA',
        'TIPO','CONDOMINIO','IPTU','AREA_UTIL','QUARTOS','BANHEIROS','VAGAS_GARAGEM',
        'DETALHES_IMOVEL','DETALHES_CONDOMINIO','FOTOS','URL','DATA_CONSULTA'
        ]

    data = data[cols]

    # INSERT DATA INTO DATABASE
    rows = data.values.tolist()
    
    # inserting row by row
    for row in rows:
        sql = f"""
        INSERT INTO anuncios
            VALUES {tuple(row)};
        """.replace('nan','NULL')

        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()

if __name__ == '__main__':
    handler()