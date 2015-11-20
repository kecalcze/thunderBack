"""Google Drive Quickstart in Python.
This script uploads a single file to Google Drive.
"""

from gdrive import helper
import httplib2
import apiclient.discovery
import apiclient.http
import os

class fileService:

    def upload(self, filename):
        # Metadata about the file.
        MIMETYPE = 'application/octet-stream'
        DESCRIPTION = 'A shiny new text document about hello world.'
        TITLE = os.path.basename(filename)

        # Create an authorized Drive API client.
        credentials = helper.get_credentials()
        http = credentials.authorize(httplib2.Http())
        drive_service = apiclient.discovery.build('drive', 'v2', http=http)

        # Check if upload folder exists
        folder_id = helper.get_fileid_by_name(helper.UPLOADFOLDER)
        if folder_id is None:
            #create the folder
            folder_id = helper.crete_folder(helper.UPLOADFOLDER)

        # Insert a file. Files are comprised of contents and metadata.
        # MediaFileUpload abstracts uploading file contents from a file on disk.
        media_body = apiclient.http.MediaFileUpload(
            filename,
            resumable=True
        )
        # The body contains the metadata for the file.
        body = {
          'title': TITLE,
          'description': DESCRIPTION,
          'mimeType': MIMETYPE,
          'parents': [{'id': folder_id}]
        }

        # look if file exists, then update it or create new
        new_file = helper.get_fileid_by_name(TITLE, False)
        if new_file is None:
            # insert new file
            print("Creating new file ...")
            new_file = drive_service.files().insert(body=body, media_body=media_body).execute()
        else:
            # update existing file
            print("Updating existing file ...")
            new_file = drive_service.files().update(fileId=new_file, body=body, media_body=media_body).execute()

        return new_file

    def download(self, folderServiceCallback):
        # Create an authorized Drive API client.
        credentials = helper.get_credentials()
        http = credentials.authorize(httplib2.Http())
        drive_service = apiclient.discovery.build('drive', 'v2', http=http)

        # get newest fiel download url

        # download file
        # extract file to default folder
        return True

#upload("D:/Capture.JPG")









