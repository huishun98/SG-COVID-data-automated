from settings import SPREADSHEET_ID, DEPLOY, SCOPES
from google.oauth2 import service_account
import pygsheets
from os import getenv

# define service
class SheetsService():
    def __init__(self) -> None:
        if DEPLOY:
            service_account_info = {
                "type": getenv('type'),
                "project_id": getenv('project_id'),
                "private_key_id": getenv('private_key_id'),
                "private_key": getenv('private_key').replace('\\n', '\n'),
                "client_email": getenv('client_email'),
                "client_id": getenv('client_id'),
                "auth_uri": getenv('auth_uri'),
                "token_uri": getenv('token_uri'),
                "auth_provider_x509_cert_url": getenv('auth_provider_x509_cert_url'),
                "client_x509_cert_url": getenv('client_x509_cert_url')
            }
            creds = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
            self.gc = pygsheets.authorize(custom_credentials=creds)
        else:
            self.gc = pygsheets.authorize(service_file='keys.json')

    def getWorksheet(self, worksheet_title):
        return self.gc.open_by_key(SPREADSHEET_ID).worksheet_by_title(worksheet_title)