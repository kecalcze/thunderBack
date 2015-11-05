__author__ = 'Bivoj'
#from pydrive.auth import GoogleAuth
#from pydrive.drive import GoogleDrive
import os, socket
import platform
import lzma
import pip

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

    def __init__(self):
        host = platform.system()
        if host is 'Windows':
            from windows import profileFinder, compressor
            print("Loading windows modules")
        else:
            from linux import profileFinder
            print("Loading linux modules")

        self.profileFinder = profileFinder.ProfileFinder()
        self.compressor = compressor.Compressor()

    def run(self):
        hostname = os.name
        hostname = self.profileFinder.getProfileFolder()
        print(hostname)
        self.compressor.compress(hostname, "D:/")
        #try:
        #lzma.open("file")


program = Main()
program.run()



