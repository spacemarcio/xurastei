# LOAD CREDENTIALS
import json

import boto3 as bt3

# SCRAPING FUNCTIONS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

import pandas as pd
from datetime import datetime

def handler(output_path = 'xox-ad-links',prefix_output_file = 'olx_imoveis_links',AWS_REGION=None,ACCESS_ID=None,ACCESS_KEY=None):
    """
    Function to collect links from properties ads in OLX and saving in S3.
    
    Parameters:
    output_path         : S3 bucket to save links.
    prefix_output_file  : prefix to saving the file. The final name is compose by 'prefix_output_file' + actual timestamp + '.txt' 
    """

    # SETUP CONNECTION
    boto3 = bt3.Session(
        region_name = AWS_REGION, 
        aws_access_key_id = ACCESS_ID, 
        aws_secret_access_key = ACCESS_KEY
    )

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

    # CRAWLING DATA
    url_root = 'https://pe.olx.com.br/grande-recife/recife'

    # search properties by neighborhood
    neighborhoods = [
        'aflitos','apipucos','barro','boa-viagem','boa-vista','campo-grande',
        'casa-amarela','casa-forte','caxanga','cidade-universitaria','cordeiro',
        'curado','derby','encruzilhada','espinheiro','estancia','gracas',
        'ilha-do-leite','ilha-do-retiro','imbiribeira','iputinga','jaqueira',
        'macaxeira','madalena','monteiro','paissandu','parnamirim','pina',
        'poco-da-panela','prado','santo-amaro','tamarineira','tejipio','torre',
        'torreao','zumbi'
    ]

    links = [] 
    for n in neighborhoods:
        stop = False
        page = 1
        
        while stop == False:

            print(f"""
            Scrapping ads from {n}
            Page {page} 
            """)
        
            url_query = f"{url_root}/{n}/imoveis/aluguel?o={page}"

            web.get(url_query)

            # checking if we passed the last page
            try:
                response = web.find_element_by_xpath("//*[contains(text(), 'Nenhum anúncio foi encontrado.')]").text
                
                if response:
                    stop = True

                print(f"{len(links)} fetched")

                print('Going to the next neighborhood...')

            # if not passed, then get ads links
            except:
                properties_elements = web.find_elements_by_tag_name('a')
                properties_links = [e.get_attribute('href') for e in properties_elements]
                properties_links = [l for l in properties_links if l is not None]
                properties_links = [l for l in properties_links if l[-9:].isnumeric()] # an ad link finish with 9 digits code

                links += properties_links                
                page += 1

    web.close()

    # WRITE LINKS IN TEMP FILE
    output_file = f"{prefix_output_file}_{int(datetime.now().timestamp())}"

    links_file = open(f"/home/airflow/{output_file}.txt",mode="w",encoding="utf-8")
    links_file.writelines([link + '\n' for link in links])
    links_file.close()

    # UPLOAD TO S3
    s3_client = boto3.client('s3')
    s3_client.upload_file(f"/home/airflow/{output_file}.txt", output_path, f"{output_file}.txt")

if __name__ == '__main__':
    handler()