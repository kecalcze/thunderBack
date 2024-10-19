__author__ = 'Jakub'

import getpass

from Interfaces.PlatformFolderServiceInterface import PlatformFolderServiceInterface


class FolderService(PlatformFolderServiceInterface):

    def getDefaultProfileFolder(self):
        global profileFolderName
        uName = getpass.getuser()
        thunderbirdPath = '/home/' + uName + '/.thunderbird'

        profileFolderName = self.getCurrentActiveProfileFolderName(thunderbirdProfilePath=thunderbirdPath)

        profilePath = thunderbirdPath + "/" + profileFolderName

        return profilePath

    def getTempFolder(self):
        return "/var/tmp/"
