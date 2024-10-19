__author__ = 'Jakub'
import getpass
import os

from Interfaces.PlatformFolderServiceInterface import PlatformFolderServiceInterface


class FolderService(PlatformFolderServiceInterface):

    def getDefaultProfileFolder(self):
        uName = getpass.getuser()
        thunderbirdPath = 'C:/Users/'+uName+'/AppData/Roaming/Thunderbird/Profiles'

        profilePath = self.getCurrentActiveProfileFolderName(thunderbirdProfilePath=thunderbirdPath)

        return profilePath

    def getTempFolder(self):
        return "C:/Windows/temp/"