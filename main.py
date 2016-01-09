#!/usr/bin/env python3
__author__ = 'Bivoj'
import os
import platform
import sys
import getopt
import socket
#custom imports

'System depended loader'
class Main():

    def __init__(self, argv):
        self.argv = argv
        host = platform.system()
        if host is 'Windows':
            from windows import folderService, compressor
            print("Loading windows modules")
        else:
            from linux import folderService, compressor
            print("Loading linux modules")

        # file services
        from gdrive import service
        self.storage =  service.BaseService()


        self.folderService = folderService.FolderService()
        self.compressor = compressor.Compressor()
        self.hostname = socket.gethostname()
        self.defaultFolder = self.folderService.getDefaultProfileFolder()

    # action for creating new snapshot
    def action_upload(self):
        filename = self.compressor.compress(self.defaultFolder, self.folderService.getTempFolder(), self.hostname)
        print("Begin upload")
        self.storage.upload(filename)
        print("Cleaning up")
        os.remove(filename)
        print("Finished")

    # action for downloading latest backup
    def action_download(self):
        print("Begin download")
        filename = self.storage.download(self.folderService)
        print("Start decompression")
        self.compressor.decompress(filename, self.folderService.getDefaultProfileFolder())
        print("Cleaning up")
        os.remove(filename)

    # main routine
    def run(self):
        action = ''
        try:
            opts, args = getopt.getopt(self.argv, "ha:", ["action="])
        except getopt.GetoptError:
            print('main.py -a <download/upload>')
            sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print('main.py -a <download/upload>')
                sys.exit()
            elif opt in ("-a", "--action"):
                action = arg

        if action == "upload":
            self.action_upload()
        elif action == "download":
            self.action_download()
        elif action:
            print("Action not found")

        print("Exit")


if __name__ == "__main__":
    program = Main(sys.argv[1:])
    program.run()



