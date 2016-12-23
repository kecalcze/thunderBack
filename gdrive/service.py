from gdrive import helper
import apiclient.discovery
from apiclient.http import MediaIoBaseDownload
from apiclient.errors import HttpError
import httplib2
import os
import io
import time
import random

class BaseService:

    # Retry transport and file IO errors.
    RETRYABLE_ERRORS = (httplib2.HttpLib2Error, IOError)

    # Number of times to retry failed downloads.
    NUM_RETRIES = 5

    def __init__(self):
        self.helper = helper.Helper()

    def handle_progressless_iter(self, error, progressless_iters):
        if progressless_iters > self.NUM_RETRIES:
            print
            'Failed to make progress for too many consecutive iterations.'
            raise error

        sleeptime = random.random() * (2 ** progressless_iters)
        print('Caught exception (%s). Sleeping for %s seconds before retry #%d.'
              % (str(error), sleeptime, progressless_iters))

        time.sleep(sleeptime)

    def upload(self, filename):
        # Metadata about the file.
        MIMETYPE = 'application/octet-stream'
        DESCRIPTION = 'ThunderBack backup file.'
        TITLE = os.path.basename(filename)
        progressless_iters = 0

        # Check if upload folder exists
        folder_id = self.helper.get_fileid_by_name(helper.UPLOADFOLDER)
        if folder_id is None:
            #create the folder
            folder_id = self.helper.create_folder(helper.UPLOADFOLDER)

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
            uploader = self.helper.service.files().insert(body=body, media_body=media_body)
        else:
            # update existing file
            print("Updating existing file ...")
            uploader = self.helper.service.files().update(fileId=new_file, body=body, media_body=media_body)

        done = False
        while not done:
            error = None
            try:
                status, done = uploader.next_chunk()
                print("Upload %d%%" % int(status.progress() * 100), end="\r")

            except HttpError as err:
                error = err
                if err.resp.status < 500:
                    raise

            except self.RETRYABLE_ERRORS as err:
                error = err

            if error:
                progressless_iters += 1
                self.handle_progressless_iter(error, progressless_iters)
            else:
                progressless_iters = 0

        return new_file

    def download(self, folder_service_callback):
        uploadFolder = self.helper.get_fileid_by_name(helper.UPLOADFOLDER)
        # get newest file download url
        downloadInfo = self.helper.get_newest_file_down_info(uploadFolder)
        progressless_iters = 0

        # download file
        print('Downloading latest backup ...')
        filename = folder_service_callback.getTempFolder() + downloadInfo['title']
        fh = io.FileIO(filename, 'wb')
        downloader = MediaIoBaseDownload(fh, downloadInfo['request'])
        done = False
        while not done:
            error = None
            try:
                status, done = downloader.next_chunk()
                print("Download %d%%." % int(status.progress() * 100), end="\r")

            except HttpError as err:
                error = err
                if err.resp.status < 500:
                    raise

            except self.RETRYABLE_ERRORS as err:
                error = err


            if error:
                progressless_iters += 1
                self.handle_progressless_iter(error, progressless_iters)
            else:
                progressless_iters = 0

        return filename

#upload("D:/Capture.JPG")









