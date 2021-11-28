# LOAD CREDENTIALS
import pandas as pd
import json

import boto3 as bt3

# SCRAPING FUNCTIONS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

def handler(input_path = 'xox-ad-refresh',input_file = 'refresh_links',output_path = 'xox-ad-bronze',output_file = 'olx_imoveis_bronze',AWS_REGION=None,ACCESS_ID=None,ACCESS_KEY=None):
    """
    Function to capture data from ads' links. Run this function to update properties registers.

    Parameters:
    input_path      : S3 bucket where links list is stored.
    input_file      : file name where links list is stored.
    output_path      : S3 bucket where data from properties ads is stored.
    output_file      : file name where data from properties ads is stored. 
    """
    
    print('Starting')

    # SETUP CONNECTION
    boto3 = bt3.Session(
        region_name = AWS_REGION, 
        aws_access_key_id = ACCESS_ID, 
        aws_secret_access_key = ACCESS_KEY
    )

    # IMPORT ADS LINKS
    s3 = boto3.client('s3')
    with open(f"/home/airflow/{input_file}.txt", 'wb') as f:
        s3.download_fileobj(input_path, f"{input_file}.txt", f)

    with open(f"/home/airflow/{input_file}.txt") as f:
        links = f.readlines()
    links = [l.strip() for l in links]

    # CRAWLING DATA FROM ADS
    with open(f"/home/airflow/{output_file}.csv", 'wb') as f:
        s3.download_fileobj(output_path, f"{output_file}.csv", f)

    data_ads = pd.read_csv(f"/home/airflow/{output_file}.csv",sep = '\t',encoding='UTF-8')

    print("Setting up WebDriver")

    # SETUP WEB DRIVER
    webdriver_options = Options()
    webdriver_options.add_argument('--no-sandbox')
    webdriver_options.add_argument('--headless')
    webdriver_options.add_argument('--disable-gpu')
    webdriver_options.add_argument('--disable-dev-shm-usage')

    web = webdriver.Chrome(
        executable_path='/home/airflow/chromedriver',
        options=webdriver_options
    )

    print(f"Getting data from URLs")
    for url in links:
        
        print(f"""
        PROGRESS: {round((links.index(url) + 1) * 100 / len(links),2)}%
        """)

        # DEFAULT VALUES    
        ad_titulo = ''
        ad_preco = ''
        ad_descricao = ''
        ad_municipio = ''
        ad_bairro = ''
        ad_cep = ''
        ad_logradouro = ''
        ad_categoria = ''
        ad_tipo = ''
        ad_condominio = ''
        ad_iptu = ''
        ad_area_util = ''
        ad_quartos = ''
        ad_banheiros = ''
        ad_vagas_na_garagem = ''
        ad_detalhes_imovel = ''
        ad_detalhes_condominio = ''

        try:
            web.get(url)
        
            ad_titulo = web.find_element_by_class_name('sc-45jt43-0').text
            ad_preco = web.find_element_by_class_name('sc-1wimjbb-0').text
            
            ad_descricao = web.find_element_by_class_name('sc-1sj3nln-1').text
            ad_descricao = ' '.join(ad_descricao.split()) # remove extra spaces

            ad_properties = web.find_elements_by_xpath("//div[@data-testid='ad-properties']")[0].text.split('\n')
            for i in range(len(ad_properties)):
                if ad_properties[i] == 'Categoria':
                    ad_categoria = ad_properties[i+1]
                elif ad_properties[i] == 'Tipo':
                    ad_tipo = ad_properties[i+1]
                elif ad_properties[i] == 'Condomínio':
                    ad_condominio = ad_properties[i+1]
                elif ad_properties[i] == 'IPTU':
                    ad_iptu = ad_properties[i+1]
                elif ad_properties[i] == 'Área útil':
                    ad_area_util = ad_properties[i+1]
                elif ad_properties[i] == 'Quartos':
                    ad_quartos = ad_properties[i+1]
                elif ad_properties[i] == 'Banheiros':
                    ad_banheiros = ad_properties[i+1]
                elif ad_properties[i] == 'Vagas na garagem':
                    ad_vagas_na_garagem = ad_properties[i+1]
                elif ad_properties[i] == 'Detalhes do imóvel':
                    ad_detalhes_imovel = ad_properties[i+1]
                elif ad_properties[i] == 'Detalhes do condominio':
                    ad_detalhes_condominio = ad_properties[i+1]
            
            ad_location = web.find_elements_by_xpath("//div[@data-testid='ad-properties']")[1].text.split('\n')
            for i in range(len(ad_location)):
                if ad_location[i] == 'CEP':
                    ad_cep = ad_location[i+1]
                elif ad_location[i] == 'Município':
                    ad_municipio = ad_location[i+1]
                elif ad_location[i] == 'Bairro':
                    ad_bairro = ad_location[i+1]
                elif ad_location[i] == 'Logradouro':
                    ad_logradouro = ad_location[i+1]

            ad_photos = web.find_elements_by_tag_name('img')
            ad_photos = [p.get_attribute('src') for p in ad_photos]
            ad_photos = [p for p in ad_photos if p.startswith('https://img.olx.com.br/images/')] # ad photos has same url pattern
            ad_photos = list(set(ad_photos)) # removing duplicates
            ad_photos = '|'.join(ad_photos)
            print(f"Data fetched")

        except:
            print(f"corrupted URL:\n{url}")

        if ad_titulo:
            
            ad_data = {
                'TITULO'                : [ad_titulo],
                'VALOR'                 : [ad_preco],
                'DESCRICAO'             : [ad_descricao],
                'MUNICIPIO'             : [ad_municipio],
                'BAIRRO'                : [ad_bairro],
                'CEP'                   : [ad_cep],
                'LOGRADOURO'            : [ad_logradouro],
                'CATEGORIA'             : [ad_categoria],
                'TIPO'                  : [ad_tipo],
                'CONDOMINIO'            : [ad_condominio],
                'IPTU'                  : [ad_iptu],
                'AREA_UTIL'             : [ad_area_util],
                'QUARTOS'               : [ad_quartos],
                'BANHEIROS'             : [ad_banheiros],
                'VAGAS_GARAGEM'         : [ad_vagas_na_garagem],
                'DETALHES_IMOVEL'       : [ad_detalhes_imovel],
                'DETALHES_CONDOMINIO'   : [ad_detalhes_condominio],
                'FOTOS'                 : [ad_photos],
                'URL'                   : [url]  
            }

            print(print(json.dumps(ad_data, sort_keys=True, indent=4)))

            print("\n\n\nSAVING DATA\n\n\n")

            ad_dataframe = pd.DataFrame(ad_data)
            data_ads = data_ads.append(ad_dataframe, ignore_index=True)

        else:
            print('Skipping for the next link')

    print("Finished!")
    web.close()

    # UPLOADING DATA DO S3
    data_ads.to_csv(f"/home/airflow/{output_file}.csv",sep='\t',encoding='UTF-8',index=False)
    
    s3_client = boto3.client('s3')
    s3_client.upload_file(f"/home/airflow/{output_file}.csv", output_path, f"{output_file}.csv")

if __name__ == '__main__':
    handler()