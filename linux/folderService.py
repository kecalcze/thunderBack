__author__ = 'Jakub'

import getpass

from Interfaces.PlatformFolderServiceInterface import PlatformFolderServiceInterface


class FolderService(PlatformFolderServiceInterface):

    def getDefaultProfileFolder(self):
        global profileFolderName
        uName = getpass.getuser()
        thunderbirdProfileDataPath = '/home/' + uName + '/.thunderbird'
        thunderbirdProfileConfigPath = thunderbirdProfileDataPath + '/profiles.ini'

        profileFolderName = self.getCurrentActiveProfileFolderName(
            thunderbirdProfileConfigPath=thunderbirdProfileConfigPath
        )

        profilePath = thunderbirdProfileDataPath + "/" + profileFolderName

        return profilePath

    def getTempFolder(self):
        return "/var/tmp/"
