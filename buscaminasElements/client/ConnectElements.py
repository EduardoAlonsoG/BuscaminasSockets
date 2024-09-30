class ConnectElements:
    def __init__(self , hostIP , hostPort, matchName = "Normal match"):
        self._hostIP = hostIP
        self._hostPort = hostPort
        self._matchName = matchName

    def getHostIp(self):
        return self._hostIP

    def getHostPort(self):
        return self._hostPort

    def getMatchName(self):
        return self._matchName + " located at " + self._hostIP

