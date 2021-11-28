#!/bin/bash 

apt-get update
apt-get -y install wget unzip
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt install ./google-chrome-stable_current_amd64.deb
wget https://chromedriver.storage.googleapis.com/96.0.4664.45/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
mv chromedriver /home/airflow/
chmod +rwx /home/airflow/chromedriver