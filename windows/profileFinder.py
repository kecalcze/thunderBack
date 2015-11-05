__author__ = 'Jakub'
import getpass
import os

class ProfileFinder:

    def getProfileFolder(self):
        uName = getpass.getuser()

        thunderbirdPath = 'C:/Users/'+uName+'/AppData/Local/Thunderbird/Profiles'
        for x in os.listdir(thunderbirdPath):
            if ".default" in x:
                profielPath = thunderbirdPath + "/" + x

                break

        return profielPath