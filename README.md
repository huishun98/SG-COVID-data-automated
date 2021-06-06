## Automation

### Data Flow
1. Obtain data from data.world
2. Process data
3. Export to Google Sheets for use in Tableau

## Set up
1. Start [Google Cloud Platform Project](https://developers.google.com/sheets/api/quickstart/python). Get/download the service account credentials, store the following as environment variables and save them in a .env file:
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