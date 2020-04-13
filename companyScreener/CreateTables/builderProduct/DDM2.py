import pandas as pd
import numpy as np
import Config.config as config
from .Price import Price


class DDM2(Price):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = config.DDM2

    def getDiscountRate(self):
        return pd.Series(self.config["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getPerpetualGrowthRate(self):
        return pd.Series(self.config["perpetualGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthRate(self):
        return pd.Series(self.config["highGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthPeriod(self):
        return pd.Series(self.config["highGrowthPeriod"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getTerminalValue(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getPerpetualGrowthRate())
        section2 = self.divide(np.power(1+self.getHighGrowthRate(), self.getHighGrowthPeriod()),
                               np.power(1+self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*section2

    def getExplicitPeriod(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getHighGrowthRate())
        section2 = self.divide(np.power(1+self.getHighGrowthRate(), self.getHighGrowthPeriod()),
                               np.power(1+self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*(1-section2)

    def getStockPrice(self):
        return self.getExplicitPeriod()+self.getTerminalValue()

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CPriceDDM2"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RPriceDDM2"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EPriceDDM2"], output, self.latestYear)

    def setPerpetualGrowthRate(self):
        output = self.getPerpetualGrowthRate()
        self.setOutput(
            0, self.colName["perpetualGrowthRate"], output, self.latestYear)

    def setHighGrowthRate(self):
        output = self.getHighGrowthRate()
        self.setOutput(
            0, self.colName["highGrowthRate"], output, self.latestYear)

    def setHighGrowthPeriod(self):
        output = self.getHighGrowthPeriod()
        self.setOutput(
            0, self.colName["highGrowthPeriod"], output, self.latestYear)
