from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import boto3
from pprint import pprint

from google_auth import get_authenticated_google_service

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
table = dynamodb.Table('coders-league-members')


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1prySnX7D6LSeYwkrS-cpJHI4VJllq7vSL_MDgQajHJU'
SAMPLE_RANGE_NAME = 'A2:D'

def main():

    service = get_authenticated_google_service("sheets", "v4", SCOPES)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                                range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])

    if not values:
        print('No data found in google sheets.')
    else:
        for row in values:

            response = table.get_item(
                    Key={'student_id': row[2]},
                )

            if 'Item' in response:
                print('Found student {}'.format(row[2]))
                
            else:

                print("\nDidn't find student {}, making record...".format(row[2]))

                response = table.put_item(
                    Item={
                            'personal_email_address': row[1],
                            'student_id': row[2],
                            'full_name': row[3],
                            'welcome_email': "no",
                        }
                    )
                
            


if __name__ == '__main__':
    main()

