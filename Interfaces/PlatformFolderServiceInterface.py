import configparser

class PlatformFolderServiceInterface:
    def getDefaultProfileFolder(self) -> str:
        """Get default thunderbird profile folder for current user"""
        pass

    def getTempFolder(self) -> str:
        """Get platform specific temp folder"""
        pass

    def getCurrentActiveProfileFolderName(self, thunderbirdProfilePath: str) -> str:
        global profileFolderName
        profilesConfigPath = thunderbirdProfilePath + '/profiles.ini'

        config = configparser.ConfigParser()
        config.read(profilesConfigPath)

        for sectionName in config.sections():
            if sectionName.startswith('Profile'):
                if ('Default' in config[sectionName] and
                        config[sectionName]['Default'] == '1'):
                    profileFolderName = config[sectionName]['Path']

        return profileFolderName