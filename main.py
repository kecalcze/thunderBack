import gdrive

__author__ = 'Bivoj'
import os
import platform
import pip
import sys
import getopt
#custom imports

'System depended loader'
class Main():
    def iai(self, package): # import and isnstall
        import importlib
        try:
            importlib.import_module(package)
        except ImportError:
            import pip
            pip.main(['install', package])
        finally:
            globals()[package] = importlib.import_module(package)


    #iai('transliterate')

    def __init__(self, argv):
        self.argv = argv
        host = platform.system()
        if host is 'Windows':
            from windows import foldersService, compressor
            print("Loading windows modules")
        else:
            from linux import profileFinder
            print("Loading linux modules")

        # file services
        self.storage =  gdrive.service.BaseService()


        self.folderService = foldersService.FoldersService()
        self.compressor = compressor.Compressor()
        self.hostname = os.environ['COMPUTERNAME']
        self.defaultfolder = self.folderService.getDefaulProfileFolder()

    # action for creating new snapshot
    def action_upload(self):
        filename = self.compressor.compress(self.defaultfolder, self.folderService.getTempFolder(), self.hostname)
        print("Begin upload")
        self.storage.upload(filename)
        print("Cleaning up")
        os.remove(filename)
        print("Finished")

    # action for downloading latest backup
    def action_download(self):
        self.gdrive.download(self.folderService)
        self.compressor.decompress("D:/test.zip", "D:/BORDELCODE/gapi/test/")
        return True

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



