import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class DDMH(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getExplicitPeriodDDMH(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getTerminalYieldGrowth())
        return self.getDividend()*section1

    def getTerminalValueDDMH(self):
        section1 = self.divide(self.getYieldGrowthRate(
        )-self.getTerminalYieldGrowth(), self.getDiscountRate()-self.getTerminalYieldGrowth())
        return self.getDividend()*self.getHighGrowthPeriod()*section1

    def getStockPriceDDMH(self):
        return self.getExplicitPeriodDDMH()+self.getTerminalValueDDMH()

    def setStockPriceDDMH(self):
        output = self.getStockPriceDDMH()
        self.setOutput(
            0, self.colName["CPriceDDMH"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RPriceDDMH"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EPriceDDMH"], output, self.latestYear)
