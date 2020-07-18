import pickle
import os.path
from datetime import date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from gpt3 import generateCommand

class SheetsAPI:
    def __init__(self, sheetId=''):
        # If modifying these scopes, delete the file token.pickle.
        self.SCOPES = ['https://www.googleapis.com/auth/drive']

        self.TEMPLATE_ID = '17bnwsQya4yrbk9h8cR2-2fiVEYU2Eo-aA7LbowoRPzc'

        self.current_sheet_id = sheetId

        self.get_cell = {
            # Current Assets
            'Cash': 'B5',
            'Accounts Receivable': 'B6',
            'Inventory': 'B7',
            'Prepaid Expenses': 'B8',
            'Short-Term Investment': 'B9',

            # Non-Current Assets
            'Long-Term Investments': 'B13',
            'Property, Plant, Equipment': 'B14',
            '(Less Accumulated Depreciation)': 'B15',
            'Intangible Assets': 'B16',

            # Current Liabilities
            'Accounts Payable': 'E5',
            'Short-Term Loans': 'E6',
            'Income Taxes Payable': 'E7',
            'Accrued Salaries and Wages': 'E8',
            'Unearned Revenue': 'E9',
            'Current Portion of Long-Term Debt': 'E10',

            # Non-Current Liabilities
            'Long-Term Debt': 'E14',
            'Deferred Income Tax': 'E15',
            'Non-Current Liabilities Other': 'E16',

            # Owner's Equity
            'Owner\'s Investment': 'E20',
            'Retained Earnings': 'E21',
            'Owner\'s Equity Other': 'E22'
        }

        self.service = self.sheets_auth()

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
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        service = build('sheets', 'v4', credentials=creds)
        return service

    def create_sheet_from_template(self):

        service = self.service

        spreadsheet = {
            'properties': {
                'title': 'Personalized Balance Sheet'
            }
        }

        spreadsheet = service.spreadsheets().create(
            body=spreadsheet, fields='spreadsheetId').execute()

        newSheetId = spreadsheet.get('spreadsheetId')

        self.current_sheet_id = newSheetId

        copy_sheet_to_another_spreadsheet_request_body = {
            'destination_spreadsheet_id': newSheetId,
        }

        request = service.spreadsheets().sheets().copyTo(spreadsheetId=self.TEMPLATE_ID,
                                                         sheetId=0, body=copy_sheet_to_another_spreadsheet_request_body)
        response = request.execute()

        deleteData = {
            "requests": [
                {
                    "deleteSheet": {
                        "sheetId": 0
                    }
                }
            ]
        }

        deleteSheet = service.spreadsheets().batchUpdate(
            spreadsheetId=self.current_sheet_id, body=deleteData).execute()
        
        # Sets the date on the spreadsheet to today's date        
        body = {
            'values': [[str(date.today())]]
        }
        
        resultSet = service.spreadsheets().values().update(
            spreadsheetId=self.current_sheet_id, range='D1', valueInputOption='USER_ENTERED', body=body).execute()

        # TODO: Change code below to process the `response` dict:
        print(response)
        return response

    def add(self, amount, section, sheetId=None):
        if sheetId == None and self.current_sheet_id == '':
            if self.current_sheet_id == '':
                self.create_sheet_from_template()
            else:
                self.current_sheet_id = sheetId
        print(self.current_sheet_id)

        cell = self.get_cell[section]

        service = self.service

        resultGet = service.spreadsheets().values().get(
            spreadsheetId=self.current_sheet_id, range=cell).execute()
        vals = resultGet.get('values', [])
        if len(vals) == 0:
            vals = [[0]]
        vals[0][0] = str(round(float(vals[0][0]) + float(amount), 2))

        body = {
            'values': vals
        }

        resultSet = service.spreadsheets().values().update(
            spreadsheetId=self.current_sheet_id, range=cell, valueInputOption='USER_ENTERED', body=body).execute()

        print(resultSet)


if __name__ == '__main__':
    # create_sheet_from_template()
    sheet = SheetsAPI()
    command = generateCommand("I bought $3000 software to be repaid in 1 month")
    sheet.add(command[1], command[2])
