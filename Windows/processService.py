import psutil

from Interfaces.ProcessServiceInterface import ProcessServiceInterface


class ProcessService(ProcessServiceInterface):

    def getProcessName(self) -> str:
        return "thunderbird.exe"