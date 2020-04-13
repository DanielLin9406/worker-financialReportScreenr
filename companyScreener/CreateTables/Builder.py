from abc import ABC, abstractmethod, abstractproperty


class Director(object):
    def __init__(self):
        self._builder = None

    @property
    def builder(self):
        return self._builder

    @builder.setter
    def builder(self, builder):
        self._builder = builder

    def constructPars(self):
        self._builder.constructPars()

    def getOutput(self):
        return self._builder.getOutput()


class Builder(ABC):
    @abstractmethod
    def constructPars(self):
        pass

    def getOutput(self):
        return self._cell.getOutput()

    def getStockPrice(self):
        return self._cell.getStockPrice()
