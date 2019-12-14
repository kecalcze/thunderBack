import inspect
import os
import pickle
from httplib2 import Http
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request


SCOPES = 'https://www.googleapis.com/auth/drive.file'
CLIENT_SECRET_FILE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/client_secret.json'
APPLICATION_NAME = 'ThunderBack'
ROOTPARENT = 'root'
UPLOADFOLDER = 'ThunderBack'

class Helper:

    def __init__(self):

        creds = self.get_credentials()
        self.service = build('drive', 'v3', credentials=creds)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """
        creds = None
        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir, 'thuderback_token.pickle')

        if os.path.exists(credential_path):
            with open(credential_path, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Http())
            else:
                flow = Flow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES, redirect_uri='urn:ietf:wg:oauth:2.0:oob')
                auth_url, _ = flow.authorization_url(prompt='consent')

                print('Please go to this URL: {}'.format(auth_url))

                code = input('Enter the authorization code: ')
                flow.fetch_token(code=code)
                creds = flow.credentials
                # Save the credentials for the next run
            with open(credential_path, 'wb') as token:
                pickle.dump(creds, token)

            print('Storing credentials to ' + credential_path)
        return creds

    def get_fileid_by_name(self, name, inroot=True):

        if inroot:
            results = self.service.files().list(q="name = '"+name+"' and 'root' in parents and trashed = false and mimeType = 'application/vnd.google-apps.folder'").execute()
        else:
            results = self.service.files().list(q="name = '"+name+"' and trashed = false and mimeType = 'application/vnd.google-apps.folder'").execute()


        items = results.get('files', [])
        if not items:
            print('FileID not found.')
            return None
        else:
            return items[0]['id']

    # returns file id and download url
    def get_newest_file_down_info(self):
        results = self.service.files().list(orderBy='createdTime', q='trashed = false', ).execute()
        files = results.get('files', [])
        request = self.service.files().get_media(fileId=files[0]['id'])
        if not results:
            print('Could`t get file info. Check your connection. Exiting.')
            exit(1)
        else:
            return dict(id=files[0]['id'], title=files[0]['name'], request=request)

    def get_all_files_info(self):
        results = self.service.files().list(orderBy='createdTime', q='trashed = false', fields='files(id,size,name)').execute()
        files = results.get('files', [])
        return files
