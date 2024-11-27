__author__ = 'Jakub'
import getpass

from Interfaces.PlatformFolderServiceInterface import PlatformFolderServiceInterface


class FolderService(PlatformFolderServiceInterface):

    def getDefaultProfileFolder(self):
        uName = getpass.getuser()
        thunderbirdProfileConfigPath = 'C:/Users/' + uName + '/AppData/Roaming/Thunderbird/profiles.ini'
        thunderbirdProfileDataPath = 'C:/Users/' + uName + '/AppData/Roaming/Thunderbird/Profiles/'

        profilePath = self.getCurrentActiveProfileFolderName(
            thunderbirdProfileConfigPath=thunderbirdProfileConfigPath
        )

        return thunderbirdProfileDataPath + profilePath

    def getTempFolderName(self):
        return "C:/Windows/temp/"