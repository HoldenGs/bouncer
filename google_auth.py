from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

def get_authenticated_google_service(service_name, version, SCOPES):

    SERVICE_ACCOUNT_FILE = os.environ.get('GOOGLE_SERVICE_ACCOUNT_CREDS')
    if SERVICE_ACCOUNT_FILE is None:
        print("Please set your GOOGLE_SERVICE_ACCOUNT_CREDS to the path of your service account file")
        exit()

    creds = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    return build(service_name, version, credentials=creds)