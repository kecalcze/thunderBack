import os
import oauth2client
from oauth2client import client
from oauth2client import tools
import httplib2
from apiclient import discovery
import inspect

SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/client_secret.json'
APPLICATION_NAME = 'Desktop Client'
ROOTPARENT = 'root'
UPLOADFOLDER = 'ThunderBack'

class Helper:

    def __init__(self):

        credentials = self.get_credentials()
        http = credentials.authorize(httplib2.Http())
        self.service = discovery.build('drive', 'v2', http=http)

    def get_credentials(self):
        """Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        """

        home_dir = os.path.expanduser('~')
        credential_dir = os.path.join(home_dir, '.credentials')
        if not os.path.exists(credential_dir):
            os.makedirs(credential_dir)
        credential_path = os.path.join(credential_dir,
                                       'drive-python-quickstart.json')

        store = oauth2client.file.Storage(credential_path)
        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
            flow.user_agent = APPLICATION_NAME
            flags = tools.argparser.parse_args(args=[])
            credentials = tools.run_flow(flow, store, flags)

            print('Storing credentials to ' + credential_path)
        return credentials

    def get_fileid_by_name(self, name, inroot=True):

        if inroot:
            results = self.service.files().list(maxResults=1, q="title = '"+name+"' and 'root' in parents and trashed = false").execute()
        else:
            results = self.service.files().list(maxResults=1, q="title = '"+name+"' and trashed = false").execute()

        items = results.get('items', [])
        if not items:
            print('FileID not found.')
            return None
        else:
            return items[0]['id']

    def create_folder(self, name, parentid=ROOTPARENT):

        # The body contains the metadata for the file.
        body = {
          'title': name,
          'description': 'ThunderBack Upload folder',
          'mimeType': 'application/vnd.google-apps.folder',
          'parents': [{'id': parentid}]
        }

        # Perform the request and print the result.
        results = self.service.files().insert(body=body).execute()
        if not results:
            print('Folder not created. Something went wrong.')
            return None
        else:
            return results['id']

    def get_newest_file(self, folder="root"):
        result = self.service.files().list(maxResults=1, q="title = '"+name+"' and 'root' in parents and trashed = false").execute()

#print(get_fileid_by_name("Music"))