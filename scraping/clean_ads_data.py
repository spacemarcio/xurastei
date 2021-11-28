# LOAD CREDENTIALS
import json

import boto3 as bt3

import pandas as pd
import numpy as np

from re import findall, sub
from datetime import datetime, timezone

def extract_numbers(value):
    if value is not None:
        try:
            numbers = ''.join(findall('[0-9]+',value))
            if len(numbers) > 0:
                return int(numbers)
            else:
                return None
        except:
            return None
    else:
        return None

def extract_array(value):
    if value is not None:
        if ',' in value:    
            return '|'.join(value.split(','))
        else:
            return value
    else:
        return None

def handler(input_path = 'xox-ad-bronze',input_file = 'olx_imoveis_bronze',output_path = 'xox-ad-silver',output_file = 'olx_imoveis_silver',AWS_REGION=None,ACCESS_ID=None,ACCESS_KEY=None):
    """
    Function to capture data from ads' links. Run this function to update properties registers.

    Parameters:
    input_path      : S3 bucket where links list is stored.
    input_file      : file name where links list is stored.
    output_path      : S3 bucket where data from properties ads is stored.
    output_file      : file name where data from properties ads is stored. 
    """
    
    # SETUP CONNECTION
    boto3 = bt3.Session(
        region_name = AWS_REGION, 
        aws_access_key_id = ACCESS_ID, 
        aws_secret_access_key = ACCESS_KEY
    )

    # IMPORT ADS DATA
    s3 = boto3.client('s3')
    with open(f"/home/airflow/{input_file}.csv", 'wb') as f:
        s3.download_fileobj(input_path, f"{input_file}.csv", f)

    data = pd.read_csv(f"/home/airflow/{input_file}.csv",sep = '\t',encoding='UTF-8')
    
    # FIXING COLUMNS

    # numeric columns
    data['CEP'] = [extract_numbers(v) for v in data['VALOR'].values.tolist()]
    data['VALOR'] = [extract_numbers(v) for v in data['VALOR'].values.tolist()]
    data['CONDOMINIO'] = [extract_numbers(v) for v in data['CONDOMINIO'].values.tolist()]
    data['IPTU'] = [extract_numbers(v) for v in data['IPTU'].values.tolist()]
    data['AREA_UTIL'] = [extract_numbers(v) for v in data['AREA_UTIL'].values.tolist()]
    data['QUARTOS'] = [extract_numbers(v) for v in data['QUARTOS'].values.tolist()]
    data['BANHEIROS'] = [extract_numbers(v) for v in data['BANHEIROS'].values.tolist()]
    data['VAGAS_GARAGEM'] = [extract_numbers(v) for v in data['VAGAS_GARAGEM'].values.tolist()]
    
    # array columns
    data['DETALHES_IMOVEL'] = data['DETALHES_IMOVEL'].replace(np.nan, 'None')
    data['DETALHES_IMOVEL'] = [extract_array(v) for v in data['DETALHES_IMOVEL'].values.tolist()]

    data['DETALHES_CONDOMINIO'] = data['DETALHES_CONDOMINIO'].replace(np.nan, 'None')
    data['DETALHES_CONDOMINIO'] = [extract_array(v) for v in data['DETALHES_CONDOMINIO'].values.tolist()]

    # string columns
    data['TITULO'] = [sub(r'[^\w\s]',' ', v) for v in data['TITULO'].values.tolist()]
    data['DESCRICAO'] = [sub(r'[^\w\s]',' ', v).strip() if v is not None else None for v in data['DESCRICAO'].values.tolist()]

    # ADDING LOAD DATE COLUMN
    data['DATA_CONSULTA'] = pd.to_datetime('today').normalize()

    # FIXING COLUMN ORDER
    cols = [
        'TITULO','VALOR','DESCRICAO','MUNICIPIO','BAIRRO','CEP','LOGRADOURO','CATEGORIA',
        'TIPO','CONDOMINIO','IPTU','AREA_UTIL','QUARTOS','BANHEIROS','VAGAS_GARAGEM',
        'DETALHES_IMOVEL','DETALHES_CONDOMINIO','FOTOS','URL','DATA_CONSULTA'
        ]

    data = data[cols]

    # UPLOADING DATA DO S3
    data.to_csv(f"/home/airflow/{output_file}.csv",sep='\t',encoding='UTF-8',index=False)
    
    s3_client = boto3.client('s3')
    s3_client.upload_file(f"/home/airflow/{output_file}.csv", output_path, f"{output_file}.csv")