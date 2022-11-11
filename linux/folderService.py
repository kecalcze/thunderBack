__author__ = 'Jakub'
import getpass
import os

class FolderService:

    def getDefaultProfileFolder(self):
        uName = getpass.getuser()

        profilePath = False

        thunderbirdPath = '/home/'+uName+'/.thunderbird'
        for x in os.listdir(thunderbirdPath):
            if x.endswith(".default"):
                profilePath = thunderbirdPath + "/" + x
                break

        return profilePath

    def getTempFolder(self):
        return "/var/tmp/"