import pandas as pd
import numpy as np
import Config.config as config
from .Price import Price


class DDM(Price):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config = config.DDM

    def getDiscountRate(self):
        return pd.Series(self.config["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getDividendTerminalForecast(self):
        g5 = self.getPerpetualGrowthRatebyGordonGrowthModel().get(
            str(int(self.latestYear)+5))
        return self.divide(self.getDividendForecast().iloc[0]*(1+g5),
                           self.getDiscountRate().get(self.latestYear)-g5)

    def getDividendForecast(self):
        thisYear = self.getDividend().get(self.latestYear)
        g1 = self.getGrowthRateByPRATModel().get(str(int(self.latestYear)+1))
        g5 = self.getPerpetualGrowthRatebyGordonGrowthModel().get(
            str(int(self.latestYear)+5))
        return self.getGrowthRateForecast(g1, g5).apply(np.prod, axis=1)*thisYear

    def getNPVofTerminalValueDDM(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), [0, 0, 0, 0, 0, self.getDividendTerminalForecast()])

    def getNPVofExplicitPeriodDDM(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), self.getDividendForecast().tolist())

    def getStockPrice(self):
        output = self.getNPVofExplicitPeriodDDM()+self.getNPVofTerminalValueDDM()
        return pd.Series([output], index=[self.latestYear])

    def setPerpetualGrowthRate(self):
        output = self.getPerpetualGrowthRatebyGordonGrowthModel()
        self.setOutput(
            0, self.colName["perpetualGrowthRate"], output, str(int(self.latestYear)+5))

    def setHighGrowthRate(self):
        output = self.getGrowthRateByPRATModel()
        self.setOutput(
            0, self.colName["highGrowthRate"], output, str(int(self.latestYear)+1))

    def setStockPriceDDM(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CPriceDDM"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RPriceDDM"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EPriceDDM"], output, self.latestYear)
