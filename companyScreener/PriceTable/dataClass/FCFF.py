import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class FCFF(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getFCFF(self):
        return (self.getEBIT()*(1-self.getTaxRate()) + self.getDepreciation() +
                self.getChangeInWorkingCapital() - self.getCapitalExpenditures())

    def getNPVofExplicitPeriodFCFF(self):
        return np.npv(self.getCostOfCapital().get(self.latestYear), self.getFCFF().tolist())

    def getNPVofTerminalValueFCFF(self):
        return self.divide(self.getFCFF().get(self.latestYear)*(1+self.getInfiniteGrowthRateFCFF().get(self.latestYear)), self.getCostOfCapital().get(self.latestYear)-self.getInfiniteGrowthRateFCFF().get(self.latestYear))

    def getEnterpriceValueFCFF(self):
        return self.getNPVofTerminalValueFCFF()+self.getNPVofExplicitPeriodFCFF()

    def getEquityValueFCFF(self):
        return self.getEnterpriceValueFCFF()+self.getFreeCashFlow()-self.getTotalLiabilities()

    def getStockPriceFCFF(self):
        return self.divide(self.getEquityValueFCFF(), self.getShares())

    def setStockPriceFCFF(self):
        output = self.getStockPriceFCFF()
        self.setOutput(
            0, self.colName["CPriceFCFF"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RPriceFCFF"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EPriceFCFF"], output, self.latestYear)
