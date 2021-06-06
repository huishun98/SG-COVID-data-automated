# SG COVID-19 Spread Visualisation Data Preparation (Automated)
This code automates the update of the Google Sheets used in the [Singapore COVID-19 Spread Tableau dashboard](https://public.tableau.com/views/SingaporeCOVIDSpreadBookAutoUpdate/Dashboard?:language=en-US&:display_count=n&:origin=viz_share_link).

View the Google Sheets with the updated data [here](https://docs.google.com/spreadsheets/d/19EPRvGyAMnYZn9LwfFa4UqYrt-MQ94-qEUg76vbl2Gs/edit?usp=sharing).

## Files
### Main files
1. start.py — obtains raw data from the [Public Places Visited by Singapore Covid-19 Cases
dataset](https://query.data.world/s/7baz2qq6fm2f7evlwjxcyqusw6bktk) on data.world, and prepare and export the data to Google Sheets for use in [Tableau visualisation](https://public.tableau.com/views/SingaporeCOVIDSpreadBookAutoUpdate/Dashboard?:language=en-US&:display_count=n&:origin=viz_share_link)
2. service/sheets.py — Google Sheets Service
3. settings.py — config for Google Sheets
4. requirements.txt — required python packages
### Secret files
5. .env file — environment variables (to be created by user)
6. keys.json — Service Account credentials obtained from Google Console (to be created by user)

## Setting Up
Initialise credentials and settings to connect to Google Sheets API
1. Start a [Google Cloud Platform Project](https://developers.google.com/sheets/api/quickstart/python). Get/download the service account credentials, store the downloaded json as keys.json and the following keys as environment variables in a .env file:
- type
- project_id
- private_key_id
- private_key
- client_email
- client_id
- auth_uri
- token_uri
- auth_provider_x509_cert_url
- client_x509_cert_url
2. Update settings file (settings.py) with relevant details.
3. Create a virtual environment and install required packages by running:
```
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
## Automating the script
Automate the execution of the script using Docker and Crontab in Mac. 

1. Install [Docker for Mac](https://www.docker.com/products/docker-desktop)
2. Create docker image by running `docker build <custom-image-name> .`
3. Create shell script to run the docker image
```
#!/bin/bash
PATH=/usr/local/bin:/usr/local/sbin:~/bin:/usr/bin:/bin:/usr/sbin:/sbin
open --background -a Docker &&
  while ! docker system info > /dev/null 2>&1; do sleep 1; done &&
  docker run -t <image-name>
```
4. Schedule the cron job to run the shell script, using Crontab. Follow [this tutorial](https://www.jcchouinard.com/python-automation-with-cron-on-mac/).
5. Remember to make code executable by running `chmod +x <path-to-shell-script>`

## Notes
Other methods tried:
1. Deployment on Heroku — Heroku's free dynos is insufficient for this project.
2. AWS Lambda — This project has many dependencies and deployment and testing on AWS Lambda takes too much time.

## References
https://www.jcchouinard.com/python-automation-with-cron-on-mac/
https://forums.docker.com/t/restart-docker-from-command-line/9420
