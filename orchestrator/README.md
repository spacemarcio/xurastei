## Step-by-step to setup Airflow

1. Setup infrastructure
2. Acess Airflow EC2 instance [SSH connection]
3. Move files from folder `orchestrator` to EC2 instance [SCP protocol]
4. Execute `install_docker.sh` script
5. Execute `setup_airflow.sh` script [ I made changes in docker compose to add some custom packages]
6. Acess Airflow Worker container [ docker ps ]
7. Execute the `setup_worker.sh` script to install google-chrome, fetch chromedriver and give chromedriver file execution permission to web scraping