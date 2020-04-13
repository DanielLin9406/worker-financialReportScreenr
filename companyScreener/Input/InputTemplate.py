from abc import ABC, abstractmethod, abstractproperty
import pandas as pd


class AbstractInputTemplate(ABC):
    def templateMethod(self):
        self.readData()
        self.filterData()

    def isFileExist(self):
        pass

    def readData(self):
        pass

    def filterData(self):
        pass


class InputTemplateFromFile(AbstractInputTemplate):
    def __init__(self, **kwargs):
        self._fileList = self.iterator2List(kwargs.get('fileIterator'))
        self.setData()

    def iterator2List(self, fileIterator):
        return [ele for ele in fileIterator]

    def isInputExist(self):
        if (len(self._fileList) == 0):
            return False
        return True

    def setData(self):
        Dict = {}
        for file in self._fileList:
            tabName = file.name.split(' ')[0].lower()
            Dict[tabName] = pd.read_excel(file, index_col=0)
        self._dict = Dict

    def getData(self):
        return self._dict


# class InputFromAPIFactory(AbstractInput):
