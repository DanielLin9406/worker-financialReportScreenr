import pandas as pd
import numpy as np
import Config.config as config
from .Price import Price


class EBT(Price):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getEBT(self):
        return self.divide(self.getPretaxIncome(), self.getShares())

    def getStockPrice(self):
        return self.divide(self.getEBT(), 0.04)

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CEBTRatio"], output, self.latestYear)
        self.setOutput(
            0, self.colName["REBTRatio"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EEBTRatio"], output, self.latestYear)
