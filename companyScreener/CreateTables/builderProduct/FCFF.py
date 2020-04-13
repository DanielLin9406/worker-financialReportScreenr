import pandas as pd
import numpy as np
import Config.config as config
from .Price import Price


class FCFF(Price):
    def __init__(self, *args):
        super().__init__(*args)
        self.config = config.FCFF

    def getPerpetualGrowthRate(self):
        return pd.Series(self.config["perpetualGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getDiscountRate(self):
        return pd.Series(self.config["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getTaxRate(self):
        return pd.Series(self.config["taxRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getFCFF(self):
        return (self.getEBIT()*(1-self.getTaxRate()) + self.getDepreciation() +
                self.getChangeInWorkingCapital() - self.getCapitalExpenditures())

    def getNPVofExplicitPeriodFCFF(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), self.getFCFF().tolist())

    def getNPVofTerminalValueFCFF(self):
        return self.divide(self.getFCFF().get(self.latestYear)*(1+self.getPerpetualGrowthRate().get(self.latestYear)), self.getDiscountRate().get(self.latestYear)-self.getPerpetualGrowthRate().get(self.latestYear))

    def getEnterpriceValue(self):
        return self.getNPVofTerminalValueFCFF()+self.getNPVofExplicitPeriodFCFF()

    def getEquityValue(self):
        return self.getEnterpriceValue()+self.getFreeCashFlow()-self.getTotalLiabilities()

    def getStockPrice(self):
        return self.divide(self.getEquityValue(), self.getShares())

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CPriceFCFF"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RPriceFCFF"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EPriceFCFF"], output, self.latestYear)
