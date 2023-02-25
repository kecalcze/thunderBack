import inspect
import os

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from appdirs import *

SCOPES = ['https://www.googleapis.com/auth/drive.appdata']
CLIENT_SECRETS_FILE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/client_secret.json'
APP_NAME = 'ThunderBack'
APP_AUTHOR = 'kecalcze'
TOKEN = user_data_dir(APP_NAME, APP_AUTHOR) + '/token.json'
ROOTPARENT = 'root'
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


class Helper:

    def __init__(self):

        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        creds = None
        print(CLIENT_SECRETS_FILE)
        print(TOKEN)

        if os.path.exists(TOKEN):
            creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
        else:
            os.makedirs(name=os.path.dirname(TOKEN), exist_ok=True)
        if not creds or not creds.valid:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
            creds = flow.run_local_server(host='localhost',
                                            port=8080,
                                            authorization_prompt_message='Please visit this URL: {url}',
                                            success_message='The auth flow is complete; you may close this window.',
                                            open_browser=True)
            with open(TOKEN, 'w') as token:
                token.write(creds.to_json())

        return build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    def get_file_id_by_name(self, name):

        results = self.service.files().list(spaces='appDataFolder', q="name = '" + name + "' and trashed = false and mimeType != "
                                                                      "'application/vnd.google-apps.folder'").execute()

        items = results.get('files', [])
        if len(items) <= 0:
            print('FileID not found.')
            return None
        else:
            return items[0]['id']

    # returns file id and download url
    def get_newest_file_down_info(self):
        results = self.service.files().list(spaces='appDataFolder', orderBy='createdTime', q='trashed = false').execute()

        if not results:
            print('Could`t get file info. Check your connection. Exiting.')
            exit(1)

        files = results.get('files', [])

        if len(files) <= 0:
            print('No backup file found! Exiting.')
            exit(1)

        request = self.service.files().get_media(fileId=files[0]['id'])

        return dict(id=files[0]['id'], title=files[0]['name'], request=request)

    def get_all_files_info(self):
        results = self.service.files().list(spaces='appDataFolder', orderBy='createdTime', q='trashed = false',
                                            fields='files(id,size,name)').execute()
        files = results.get('files', [])
        return files
