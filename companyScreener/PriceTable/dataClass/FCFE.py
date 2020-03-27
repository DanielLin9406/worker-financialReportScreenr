import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class FCFE(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getFCFEGrowthRatebySingleStageModel(self):
        equityMarketValue = self.getPrice().get(self.latestYear) * \
            self.getShares().get(self.latestYear)
        R = self.getCostofEquity().get(self.latestYear)
        FCFE0 = self.getFCFE().get(self.latestYear)
        output = self.divide(equityMarketValue*R-FCFE0,
                             equityMarketValue+FCFE0)
        return pd.Series([output], index=[str(int(self.latestYear)+5)])

    def getFCFE(self):
        return (self.getNetCashFromOperation()+self.getShortTermDebtIssuance() +
                self.getNetBorrowings()-self.getCapitalExpenditures())

    def getFCFETerminalForecast(self):
        g5 = self.getFCFEGrowthRatebySingleStageModel().get(str(int(self.latestYear)+5))
        return self.divide(self.getFCFEForecast().iloc[0]*(1+g5),
                           self.getCostofEquity().get(self.latestYear)-g5)

    def getFCFEForecast(self):
        thisYear = self.getFCFE().get(self.latestYear)
        g1 = self.getGrowthRatebyPRATModel().get(str(int(self.latestYear)+1))
        g5 = self.getFCFEGrowthRatebySingleStageModel().get(str(int(self.latestYear)+5))
        return self.getGrowthRateForecast(g1, g5).apply(np.prod, axis=1)*thisYear

    def getNPVofTerminalValueFCFE(self):
        return np.npv(self.getCostofEquity().get(self.latestYear), [0, 0, 0, 0, 0, self.getFCFETerminalForecast()])

    def getNPVofExplicitPeriodFCFE(self):
        return np.npv(self.getCostofEquity().get(self.latestYear), self.getFCFEForecast().tolist())

    def getEquityValueFCFE(self):
        return self.sum([self.getNPVofExplicitPeriodFCFE(), self.getNPVofTerminalValueFCFE()])

    def getStockPriceFCFE(self):
        return self.divide(self.getEquityValueFCFE(), self.getShares())

    def setStockPriceFCFE(self):
        output = self.getStockPriceFCFE()
        self.setOutput(
            0, self.colName["CPriceFCFE"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RPriceFCFE"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EPriceFCFE"], output, self.latestYear)
