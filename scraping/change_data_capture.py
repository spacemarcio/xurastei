# LOAD CREDENTIALS
import json

import boto3 as bt3

import pandas as pd 

def handler(collect_path = 'xox-ad-links',output_path = 'xox-ad-refresh',refresh_file = 'refresh_links',AWS_REGION=None,ACCESS_ID=None,ACCESS_KEY=None):
    """
    Function to identify links that need to be scraped. That's a CDC strategy.

    Parameters:
    collect_path : S3 bucket where links collections are stored.
    output_path : S3 bucket to save file where links to be scraped are stored.
    refresh_links : file name where links ads to be scraped is stored. 
    """

    # SETUP CONNECTION
    boto3 = bt3.Session(
        region_name = AWS_REGION, 
        aws_access_key_id = ACCESS_ID, 
        aws_secret_access_key = ACCESS_KEY
    )

    # IMPORT MOST RECENT COLLECTION OF LINKS
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(collect_path)
    links_files = bucket.objects.all()
    links_files = [e.key for e in links_files]

    last_link_collect = sorted(links_files,reverse=True)[0]
    last_link_update = sorted(links_files,reverse=True)[1]

    s3 = boto3.client('s3')
    with open(f"/home/airflow/{last_link_collect}", 'wb') as f:
        s3.download_fileobj(collect_path, last_link_collect, f)

    with open(f"/home/airflow/{last_link_collect}") as f:
        most_recent_links = f.readlines()
    most_recent_links = [l.strip() for l in most_recent_links]

    # IMPORT LAST UPDATED LINKS
    with open(f"/home/airflow/{last_link_update}", 'wb') as f:
        s3.download_fileobj(collect_path, f"{last_link_update}", f)

    with open(f"/home/airflow/{last_link_update}") as f:
        last_update_links = f.readlines()
    last_update_links = [l.strip() for l in last_update_links]

    # FIND UN-COLLECTED LINKS
    links_to_refresh = [l for l in most_recent_links if l not in last_update_links]

    # WRITE LINKS IN TEMP FILE
    refresh_links_file = open(f"/home/airflow/{refresh_file}.txt",mode="w",encoding="utf-8")
    refresh_links_file.writelines([link + '\n' for link in links_to_refresh])
    refresh_links_file.close()

    # UPLOAD TO S3
    s3_client = boto3.client('s3')
    s3_client.upload_file(f"/home/airflow/{refresh_file}.txt", output_path, f"{refresh_file}.txt")

if __name__ == '__main__':
    handler()