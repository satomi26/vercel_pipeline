from http.server import BaseHTTPRequestHandler
from google.oauth2 import service_account
from apiclient import discovery
import urllib3
import json
import os
 
def get_data_lambda():
    http = urllib3.PoolManager()
    url = "https://cloud.iexapis.com/stable/stock/tsla/previous?token=" + os.environ.get("IEX_API_KEY")
    resp = http.request("GET", url)
    values = json.loads(resp.data)
    return values
 
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SAMPLE_SPREADSHEET_ID = '1HWCWi7gHWyRqxdmPSWgpnq0EnceAJcqGgwwGN4LoicE'
SAMPLE_RANGE_NAME = 'A1:AA1000'
 
class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        values = get_data_lambda()
        service_account_credentials = {
            "type": os.environ.get("TYPE"),
            "project_id": os.environ.get("PROJECT_ID"),
            "private_key_id": os.environ.get("PRIVATE_KEY_ID"),
            "private_key": os.environ.get("PRIVATE_KEY"),
            "client_email": os.environ.get("CLIENT_EMAIL"),
            "client_id": os.environ.get("CLIENT_ID"),
            "auth_uri": os.environ.get("AUTH_URI"),
            "token_uri": os.environ.get("TOKEN_URI"),
            "auth_provider_x509_cert_url": os.environ.get("AUTH_PROVIDER"),
            "client_x509_cert_url": os.environ.get("CLIENT_URL")
        }
        credentials = service_account.Credentials.from_service_account_info(
            service_account_credentials, scopes=SCOPES)
        service = discovery.build('sheets', 'v4', credentials=credentials)
        #values_list = list(values.values())
        final_list = []
        #final_list.append(values_list)

        final_list.append(values['date'])
        final_list.append(values['close'])

        dict_me = dict(values=final_list)
        service.spreadsheets().values().append(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            valueInputOption='RAW',
            range=SAMPLE_RANGE_NAME,
            body=dict_me).execute()
 
        print('Sheet successfully Updated')
        return
    
