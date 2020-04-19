import pandas as pd


class ReadLocalFile:
    def __init__(self, **kwargs):
        self._company = kwargs.get('company')
        self._localFileDict = kwargs.get('localFileDict')
        self._dict = None
        self.init()

    def init(self):
        if(self.isFileExist()):
            self.setReportList()
            self.setData()

    def setReportList(self):
        self._fileList = self.getReportList()

    def getReportList(self):
        return self._localFileDict.get(self._company).get('reportList')

    def isReportExist(self):
        if (self.isLocalFolderExist()):
            return self._localFileDict.get(self._company).get('isReportExist')
        return False

    def isLocalFolderExist(self):
        return self._company in self._localFileDict

    def isFileExist(self):
        return self.isReportExist()

    def concatTable(self, dict):
        balanceDF = dict["balance"]
        cashDF = dict["cash"]
        incomeDF = dict["income"]
        return pd.concat([balanceDF, cashDF, incomeDF])

    def readFile(self):
        Dict = {}
        for file in self._fileList:
            tabName = file.name.split(' ')[0].lower()
            Dict[tabName] = pd.read_excel(file, index_col=0)
        return self.concatTable(Dict)

    def setData(self):
        self._dict = self.readFile()

    def getData(self):
        return self._dict
