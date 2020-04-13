import pandas as pd
import numpy as np
import Config.config as config
from .Price import Price


class FCFE(Price):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = config.FCFE

    def getDiscountRate(self):
        return pd.Series(self.config["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getFCFE(self):
        return (self.getNetCashFromOperation()+self.getShortTermDebtIssuance() +
                self.getNetBorrowings()-self.getCapitalExpenditures())

    def getTerminalForecast(self):
        g5 = self.getPerpetualGrowthRatebySingleStageModel().get(str(int(self.latestYear)+5))
        return self.divide(self.getFCFEForecast().iloc[0]*(1+g5),
                           self.getDiscountRate().get(self.latestYear)-g5)

    def getFCFEForecast(self):
        thisYear = self.getFCFE().get(self.latestYear)
        g1 = self.getGrowthRateByPRATModel().get(str(int(self.latestYear)+1))
        g5 = self.getPerpetualGrowthRatebySingleStageModel().get(str(int(self.latestYear)+5))
        return self.getGrowthRateForecast(g1, g5).apply(np.prod, axis=1)*thisYear

    def getNPVofTerminalValue(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), [0, 0, 0, 0, 0, self.getTerminalForecast()])

    def getNPVofExplicitPeriod(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), self.getFCFEForecast().tolist())

    def getEquityValue(self):
        return self.sum([self.getNPVofExplicitPeriod(), self.getNPVofTerminalValue()])

    def getStockPrice(self):
        return self.divide(self.getEquityValue(), self.getShares())

    def setPerpetualGrowthRate(self):
        output = self.getPerpetualGrowthRatebySingleStageModel()
        self.setOutput(
            0, self.colName["perpetualGrowthRate"], output, str(int(self.latestYear)+5))

    def setHighGrowthRate(self):
        output = self.getGrowthRateByPRATModel()
        self.setOutput(
            0, self.colName["highGrowthRate"], output, str(int(self.latestYear)+1))

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CPriceFCFE"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RPriceFCFE"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EPriceFCFE"], output, self.latestYear)
