import pandas as pd


class ReadLocalFile:
    def __init__(self, **kwargs):
        self._fileList = self.iterator2List(kwargs.get('fileIterator'))
        self.setData()

    def iterator2List(self, fileIterator):
        return [ele for ele in fileIterator]

    def isInputExist(self):
        if (len(self._fileList) == 0):
            return False
        return True

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
