import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class EBT(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getEBT(self):
        return self.divide(self.getPretaxIncome(), self.getShares())

    def getEBTPriceRatio(self):
        return self.divide(self.getEBT(), 0.04)

    def setEBTPriceRatio(self):
        output = self.getEBTPriceRatio()
        self.setOutput(
            0, self.colName["CEBTRatio"], output, self.latestYear)
        self.setOutput(
            1, self.colName["REBTRatio"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EEBTRatio"], output, self.latestYear)
