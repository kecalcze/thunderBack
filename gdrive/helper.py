import inspect
import os

import google.oauth2.credentials

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/drive.file']
CLIENT_SECRETS_FILE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/client_secret.json'
APPLICATION_NAME = 'ThunderBack'
ROOTPARENT = 'root'
UPLOADFOLDER = 'ThunderBack'
API_SERVICE_NAME = 'drive'
API_VERSION = 'v3'


class Helper:

    def __init__(self):

        self.service = self.get_authenticated_service()

    def get_authenticated_service(self):
        print(CLIENT_SECRETS_FILE)
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(host='localhost',
                                            port=8080,
                                            authorization_prompt_message='Please visit this URL: {url}',
                                            success_message='The auth flow is complete; you may close this window.',
                                            open_browser=True)
        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def get_fileid_by_name(self, name, inroot=True):

        if inroot:
            results = self.service.files().list(q="name = '" + name + "' and 'root' in parents and trashed = false and "
                                                                      "mimeType = "
                                                                      "'application/vnd.google-apps.folder'").execute()
        else:
            results = self.service.files().list(q="name = '" + name + "' and trashed = false and mimeType = "
                                                                      "'application/vnd.google-apps.folder'").execute()

        items = results.get('files', [])
        if not items:
            print('FileID not found.')
            return None
        else:
            return items[0]['id']

    # returns file id and download url
    def get_newest_file_down_info(self):
        results = self.service.files().list(orderBy='createdTime', q='trashed = false and mimeType = "application/vnd.google-apps.file"').execute()

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
        results = self.service.files().list(orderBy='createdTime', q='trashed = false',
                                            fields='files(id,size,name)').execute()
        files = results.get('files', [])
        return files
