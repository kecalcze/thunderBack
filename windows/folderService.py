__author__ = 'Jakub'
import getpass
import os

class FolderService:

    def getDefaultProfileFolder(self):
        uName = getpass.getuser()

        thunderbirdPath = 'C:/Users/'+uName+'/AppData/Local/Thunderbird/Profiles'
        for x in os.listdir(thunderbirdPath):
            if ".default" in x:
                profielPath = thunderbirdPath + "/" + x
                break

        return profielPath

    def getTempFolder(self):
        return "C:/Windows/temp/"