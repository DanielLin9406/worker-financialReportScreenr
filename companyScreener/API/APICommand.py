from Worker.worker import isColumnExist, isCacheExist, readJSONContent, readAPIContent, getDF, fetchUrlWithLog, requestRetrySession, saveDFtoFile


class CommandInvoker:
    def __init__(self):
        self._command = None

    def setCommand(self, command: APICommand):
        self._command = command

    def getDataFromAPI(self) -> None:
        if isinstance(self._command, APICommand):
            self._command.execute()


class APICommand(ABC):
    """
    The Command interface declares a method for executing a command.
    """

    @abstractmethod
    def execute(self) -> None:
        pass

    def isCacheExist(self, key, name):
        return isCacheExist(key, name)

    def getDF(self, key, name):
        return getDF(key, name)

    def fetchDataViaAPI(self, url, urlName, fetchFunction=requestRetrySession):
        return fetchUrlWithLog(url, fetchFunction, urlName)

    def saveDF2File(self, df, company, fileName):
        return saveDFtoFile(df, company, fileName)

    def readJSONAsDF(self, content):
        return readJSONContent(content)

    def readCSVAsDF(self, content):
        return readAPIContent(content)

    def dumpData(self, parNameCollection):
        if (self.isCacheExist(parNameCollection, self._fileName)):
            return self.getDF(
                parNameCollection, self._fileName)
        else:
            content = self.fetchDataViaAPI(self.url, self._urlName)
            df = self.APICallback(content)
            return self.saveDFtoFile(df, parNameCollection, self._fileName)

    def execute(self) -> None:
        return self.dumpDF(self._parNameCollection)
