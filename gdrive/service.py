from gdrive import helper
import apiclient.discovery
import apiclient.http
import os

class BaseService:

    def __init__(self):
        self.helper = helper.Helper()

    def upload(self, filename):
        # Metadata about the file.
        MIMETYPE = 'application/octet-stream'
        DESCRIPTION = 'ThunderBack backup file.'
        TITLE = os.path.basename(filename)

        # Check if upload folder exists
        folder_id = self.helper.get_fileid_by_name(helper.UPLOADFOLDER)
        if folder_id is None:
            #create the folder
            folder_id = self.helper.crete_folder(helper.UPLOADFOLDER)

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
        new_file = self.helper.get_fileid_by_name(TITLE, False)
        if new_file is None:
            # insert new file
            print("Creating new file ...")
            new_file = self.helper.service.files().insert(body=body, media_body=media_body).execute()
        else:
            # update existing file
            print("Updating existing file ...")
            new_file = self.helper.service.files().update(fileId=new_file, body=body, media_body=media_body).execute()

        return new_file

    def download(self, folder_service_callback):
        uploadFolder = self.helper.get_fileid_by_name(helper.UPLOADFOLDER)
        # get newest file download url
        downloadInfo = self.helper.get_newest_file_down_info(uploadFolder)

        # download file
        print('Downloading latest backup ...')
        resp, content = self.helper.service._http.request(downloadInfo['downloadUrl'])
        if resp.status == 200:
            filename = folder_service_callback.getTempFolder()+downloadInfo['title']
            f = open(filename,'wb')
            f.write(content)
            return filename
        else:
            print( 'An error occurred: %s' % resp)
            exit(1)

#upload("D:/Capture.JPG")









