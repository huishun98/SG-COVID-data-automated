from __future__ import print_function

from settings import SPREADSHEET_ID, DEPLOY
import pygsheets

class SheetsService():
    def __init__(self) -> None:
        self.gc = pygsheets.authorize(service_account_env_var = 'GDRIVE_API_CREDENTIALS') if DEPLOY else pygsheets.authorize(service_file='keys.json')

    def getWorksheet(self, worksheet_title):
        return self.gc.open_by_key(SPREADSHEET_ID).worksheet_by_title(worksheet_title)
