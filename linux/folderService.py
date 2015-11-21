__author__ = 'Jakub'
import getpass
import os

class FolderService:

    def getDefaultProfileFolder(self):
        uName = getpass.getuser()

        thunderbirdPath = '/home/'+uName+'/.thunderbird'
        for x in os.listdir(thunderbirdPath):
            if ".default" in x:
                profilePath = thunderbirdPath + "/" + x
                break

        return profilePath

    def getTempFolder(self):
        return "/var/tmp/"