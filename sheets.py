'''
author @george

Sheets API integration to duplicate balance sheet template and add to it
'''

import pickle
import os.path
from datetime import date
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


class balanceSheet():
    def __init__(self, sheetId=''):
        '''
        Initializes SheetsAPI
        '''
        # auth scope for sheets API, if modifying, delete token.pickle
        self.SCOPES = ['https://www.googleapis.com/auth/drive']

        # balance sheet template
        self.TEMPLATE_ID = '17bnwsQya4yrbk9h8cR2-2fiVEYU2Eo-aA7LbowoRPzc'

        self.current_sheet_id = sheetId

        # dictionary of mapping of cell title with cell index
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
        print("sheetid", self.current_sheet_id)
        
        self.create_sheet_from_template()

    def sheets_auth(self):
        '''
        Gets authorization to modify sheets
        '''
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
        '''
        Creates new blank sheet, duplicated the template balance sheet into it and deletes
        the intial empty sheet.
        '''

        # Get authenitcated service
        service = self.service

        spreadsheet = {
            'properties': {
                'title': 'Personalized Balance Sheet'
            }
        }

        # Create a new spreadsheet
        spreadsheet = service.spreadsheets().create(
            body=spreadsheet, fields='spreadsheetId').execute()

        newSheetId = spreadsheet.get('spreadsheetId')

        self.current_sheet_id = newSheetId

        copy_sheet_to_another_spreadsheet_request_body = {
            'destination_spreadsheet_id': newSheetId,
        }

        # Copy template sheet to the new spreadsheet
        request = service.spreadsheets().sheets().copyTo(spreadsheetId=self.TEMPLATE_ID,
                                                         sheetId=0, body=copy_sheet_to_another_spreadsheet_request_body)
        response = request.execute()

        # Delete the empty intial sheet in the new spreadsheet
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

        return response

    def update(self, function, amount, section, sheetId=None):
        '''
        Modifies a cell in the spreadsheet by adding to it.
        '''

        # Get cell being updated with error handling
        try:
            cell = self.get_cell[section]
        except KeyError:
            print("Field not found")
            return

        # add or remove handling
        if function == "remove":
            amount *= -1.0

        # Set object sheet ID if one is provided
        if sheetId:
            self.current_sheet_id = sheetId

        # Get authenitcated service
        service = self.service

        # Get the current value in the cell to be modified
        resultGet = service.spreadsheets().values().get(
            spreadsheetId=self.current_sheet_id, range=cell).execute()
        vals = resultGet.get('values', [])

        if len(vals) == 0:
            vals = [[0]]

        # Add to the cell
        vals[0][0] = str(round(float(vals[0][0]) + float(amount), 2))

        # Update cell in sheet
        body = {
            'values': vals
        }

        resultSet = service.spreadsheets().values().update(
            spreadsheetId=self.current_sheet_id, range=cell, valueInputOption='USER_ENTERED', body=body).execute()
