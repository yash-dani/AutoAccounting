import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class SheetsAPI:
    def __init__(self):
        # If modifying these scopes, delete the file token.pickle.
        SCOPES = ['https://www.googleapis.com/auth/drive']

        TEMPLATE_ID = '17bnwsQya4yrbk9h8cR2-2fiVEYU2Eo-aA7LbowoRPzc'


    def sheets_auth(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        return service


    def create_sheet_from_template(self):

        service = self.sheets_auth()

        spreadsheet = {
            'properties': {
                'title': 'Personalized Balance Sheet'
            }
        }

        spreadsheet = service.spreadsheets().create(
            body=spreadsheet, fields='spreadsheetId').execute()
        print('Spreadsheet ID: {0}'.format(spreadsheet.get('spreadsheetId')))


    def add(self, amount, cell, sheetId):

        service = sheets_auth()
        resultGet = service.spreadsheets().values().get(
            spreadsheetId=sheetId, range=cell).execute()
        vals = resultGet.get('values', [])
        vals[0][0] = str(round(float(vals[0][0]) + float(amount), 2))

        body = {
            'values': vals
        }

        resultSet = service.spreadsheets().values().update(
            spreadsheetId=sheetId, range=cell, valueInputOption='USER_ENTERED', body=body).execute()


if __name__ == '__main__':
    # create_sheet_from_template()
    sheet = SheetsAPI()
    sheet.add(10, 'B5', TEMPLATE_ID)
