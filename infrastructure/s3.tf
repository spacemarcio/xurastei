resource "aws_s3_bucket" "ads-links" {
  bucket = "xox-ad-links"
  acl    = "private"
}

resource "aws_s3_bucket" "ads-refresh" {
  bucket = "xox-ad-refresh"
  acl    = "private"
}

resource "aws_s3_bucket" "ads-bronze" {
  bucket = "xox-ad-bronze"
  acl    = "private"
}

resource "aws_s3_bucket" "ads-silver" {
  bucket = "xox-ad-silver"
  acl    = "private"
}

resource "aws_s3_bucket" "ads-gold" {
  bucket = "xox-ad-gold"
  acl    = "private"
}

resource "aws_s3_bucket" "functions" {
  bucket = "xox-functions"
  acl    = "public-read-write"
}

resource "aws_s3_bucket" "credentials" {
  bucket = "xox-credentials"
  acl    = "private"
}