resource "aws_s3_bucket_object" "links" {
  bucket = aws_s3_bucket.functions.id
  key = "fetch_ads_links.py"
  acl = "public-read-write"
  source = "../scraping/fetch_ads_links.py"
  etag = filemd5("../scraping/fetch_ads_links.py")
}

resource "aws_s3_bucket_object" "data" {
  bucket = aws_s3_bucket.functions.id
  key = "fetch_ads_data.py"
  acl = "public-read-write"
  source = "../scraping/fetch_ads_data.py"
  etag = filemd5("../scraping/fetch_ads_data.py")
}

resource "aws_s3_bucket_object" "cdc" {
  bucket = aws_s3_bucket.functions.id
  key = "change_data_capture.py"
  acl = "public-read-write"
  source = "../scraping/change_data_capture.py"
  etag = filemd5("../scraping/change_data_capture.py")
}

resource "aws_s3_bucket_object" "clean-data" {
  bucket = aws_s3_bucket.functions.id
  key = "clean_ads_data.py"
  acl = "public-read-write"
  source = "../scraping/clean_ads_data.py"
  etag = filemd5("../scraping/clean_ads_data.py")
}

resource "aws_s3_bucket_object" "insert-data" {
  bucket = aws_s3_bucket.functions.id
  key = "load_into_database.py"
  acl = "public-read-write"
  source = "../scraping/load_into_database.py"
  etag = filemd5("../scraping/load_into_database.py")
}

resource "aws_s3_bucket_object" "clustering" {
  bucket = aws_s3_bucket.functions.id
  key = "clustering.py"
  acl = "public-read-write"
  source = "../modeling/clustering.py"
  etag = filemd5("../modeling/clustering.py")
}

resource "aws_s3_bucket_object" "ads-dataframe" {
  bucket = aws_s3_bucket.ads-bronze.id
  key = "olx_imoveis_bronze.csv"
  acl = "private"
  source = "../scraping/dataframe_layouts/olx_imoveis_bronze.csv"
  etag = filemd5("../scraping/dataframe_layouts/olx_imoveis_bronze.csv")
}

resource "aws_s3_bucket_object" "ads-links" {
  bucket = aws_s3_bucket.ads-links.id
  key = "olx_imoveis_links_1000000000.txt"
  acl = "private"
  source = "../scraping/dataframe_layouts/olx_imoveis_links_1000000000.txt"
  etag = filemd5("../scraping/dataframe_layouts/olx_imoveis_links_1000000000.txt")
}

resource "aws_s3_bucket_object" "airflow-variables" {
  bucket = aws_s3_bucket.credentials.id
  key = "airflow-variables.json"
  acl = "private"
  source = "../orchestrator/airflow-variables.json"
  etag = filemd5("../orchestrator/airflow-variables.json")
}