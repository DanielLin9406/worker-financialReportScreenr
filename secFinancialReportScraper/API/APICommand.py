from abc import ABC, abstractmethod, abstractproperty
from Worker.worker import requestRetrySession, fetchUrlWithLog, saveDFtoFile, isCacheExist, getDF


class APICommand(ABC):

    @abstractmethod
    def execute(self) -> None:
        pass

    def fetchDataViaAPI(self, url, urlName, fetchFunction=requestRetrySession):
        return fetchUrlWithLog(url, fetchFunction, urlName)

    def saveDFtoFile(self, df, company, fileName):
        return saveDFtoFile(df, company, fileName)

    def dumpData(self):
        if (self._parNameCollection is 'fullKeyList'):
            return self.getFullKeyList()
        elif(self._parNameCollection is 'fullData'):
            return self.getFullData()
        else:
            return self.getParticularData()

    def getParticularData(self):
        if (self.isCacheExist(self._parNameCollection, self._fileName)):
            return self.getDF(
                self._parNameCollection, self._fileName)
        else:
            content = self.fetchDataViaAPI(self._url, self._urlName)
            df = self.APICallback(content)
            return self.saveDFtoFile(df, self._parNameCollection, self._fileName)

    def getFullKeyList(self):
        return self.getFullData().axes[0].values

    def getFullData(self):
        if (self.isCacheExist(None, self._fileName)):
            return self.getDF(None, self._fileName)
        else:
            content = self.fetchDataViaAPI(self._url, self._urlName)
            df = self.APICallback(content)
            return self.saveDFtoFile(df, None, self._fileName)

    def isCacheExist(self, key, name):
        return isCacheExist(key, name)

    def getDF(self, key, name):
        return getDF(key, name)

    def execute(self) -> None:
        return self.dumpData()


class CommandInvoker:
    def __init__(self):
        self._command = None

    def setCommand(self, command: APICommand):
        self._command = command

    def getDataFromAPI(self) -> None:
        if isinstance(self._command, APICommand):
            return self._command.execute()
