import psutil

class ProcessServiceInterface:

    # def isThunderbirdRunning(self) -> bool:
    #     """Is Thunderbird mail client running"""
    #     pass

    def isThunderbirdRunning(self) -> bool:
        if self.getProcessName() in (p.name() for p in psutil.process_iter()):
            return True
        else:
            return False

    def getProcessName(self) -> str:
        """Get platform specific process name"""
        pass
