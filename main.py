#!/usr/bin/env python3
__author__ = 'Bivoj'
import os
import platform
import sys
import getopt
import socket
import pprint


class Main:

    def __init__(self, argv):
        self.argv = argv
        host = platform.system()
        if host == 'Windows':
            print("Loading windows modules")
            from windows import folderService, compressor
        else:
            print("Loading linux modules")
            from linux import folderService, compressor

        # file services
        from gdrive import service
        self.storage = service.BaseService()

        self.folderService = folderService.FolderService()
        self.compressor = compressor.Compressor()
        self.hostname = socket.gethostname()
        self.defaultFolder = self.folderService.getDefaultProfileFolder()

    # action for creating new snapshot
    def action_upload(self):
        filename = self.compressor.compress(self.defaultFolder, self.folderService.getTempFolder(), self.hostname)
        print("Begin upload")
        try:
            self.storage.upload(filename)
        finally:
            print("Cleaning up")
            os.remove(filename)
        print("Finished")

    # action for downloading latest backup
    def action_download(self):
        print("Begin download")
        filename = self.storage.download(self.folderService)
        print("Start decompression")
        try:
            self.compressor.decompress(filename, self.folderService.getDefaultProfileFolder())
        finally:
            print("Cleaning up")
            os.remove(filename)

    def action_clean(self):
        print("Begin cleaning cloud data")
        files = self.storage.clean()
        print('Cleaned files:')
        pprint.pprint(files)
        print('Cleaning complete')

    def action_clean_all(self):
        print("Begin cleaning all cloud data")
        files = self.storage.clean(deleteAll=True)
        print('Cleaned files:')
        pprint.pprint(files)
        print('Cleaning all complete')

    def action_list(self):
        print("List of files:")
        files = self.storage.list()
        pprint.pprint(files)

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
                print('main.py -a <download/upload/list/clean/clean-all>')
                sys.exit()
            elif opt in ("-a", "--action"):
                action = arg

        if action == "upload":
            self.action_upload()
        elif action == "download":
            self.action_download()
        elif action == "list":
            self.action_list()
        elif action == "clean":
            if input("This will leave only the latest backup. Are you sure? (y/n)") != "y":
                exit()
            self.action_clean()
        elif action == "clean-all":
            if input("This will clean all your backups in cloud. Are you sure? (y/n)") != "y":
                exit()
            self.action_clean_all()
        elif action:
            print("Action not found")

        print("Exit")


if __name__ == "__main__":
    program = Main(sys.argv[1:])
    program.run()
