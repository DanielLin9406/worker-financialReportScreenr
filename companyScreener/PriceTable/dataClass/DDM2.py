import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class DDM2(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getTerminalValueDDM2(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getTerminalYieldGrowth())
        section2 = self.divide(np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod()),
                               np.power(1+self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*section2

    def getExplicitPeriodDDM2(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getYieldGrowthRate())
        section2 = self.divide(np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod()),
                               np.power(1+self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*(1-section2)

    def getStockPriceDDM2(self):
        return self.getExplicitPeriodDDM2()+self.getTerminalValueDDM2()

    def setStockPriceDDM2(self):
        output = self.getStockPriceDDM2()
        self.setOutput(
            0, self.colName["CPriceDDM2"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RPriceDDM2"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EPriceDDM2"], output, self.latestYear)
