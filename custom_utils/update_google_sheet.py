
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

try:
    credentials = ServiceAccountCredentials.from_json_keyfile_name('../data/client_secret.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open('cooked_complete_dataset')

    with open('../data/cooked_data/cooked_complete_dataset.csv', 'r') as file_obj:
        content = file_obj.read()
        client.import_csv(spreadsheet.id, data=content) 
except:
    pass