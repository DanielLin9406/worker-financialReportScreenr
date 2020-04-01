import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class DDMH(Price):
    def __init__(self, *args):
        super().__init__(*args)
        self.config = config.DDMH

    def getDiscountRate(self):
        return pd.Series(self.config["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getPerpetualGrowthRate(self):
        return pd.Series(self.config["perpetualGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthRate(self):
        return pd.Series(self.config["highGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthPeriod(self):
        return pd.Series(self.config["highGrowthPeriod"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getExplicitPeriod(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getPerpetualGrowthRate())
        return self.getDividend()*section1

    def getTerminalValue(self):
        section1 = self.divide(self.getHighGrowthRate(
        )-self.getPerpetualGrowthRate(), self.getDiscountRate()-self.getPerpetualGrowthRate())
        return self.getDividend()*self.getHighGrowthPeriod()*section1

    def getStockPrice(self):
        return self.getExplicitPeriod()+self.getTerminalValue()

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CPriceDDMH"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RPriceDDMH"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EPriceDDMH"], output, self.latestYear)

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
