import gspread
from google.oauth2.service_account import Credentials

import os

base = os.getcwd()                  
path = os.path.dirname(base)



class ConnectGoogleSheet : 
    def __init__(self, json_name) : 
        # Define the scope and path to your credentials file
        SCOPE = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        SERVICE_ACCOUNT_FILE = f"{path}/gg_sheet/{json_name}"

        # Load credentials
        self.credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPE)

        # Authorize gspread client
        
    def loadSheet_WorkSheet(self, spreedsheet_id , workset_name) : 

        try : 
            gc = gspread.authorize(self.credentials)
            spreadsheet = gc.open_by_key(spreedsheet_id)
            self.worksheet = spreadsheet.worksheet(workset_name)
            return self.worksheet
        except Exception as e : 
            print ("Error : ", e)

        