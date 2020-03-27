import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class DDM(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getDividendGrowthRatebyGordonGrowthModel(self):
        currentPrice = self.getPrice().get(self.latestYear)
        R = self.getCostofEquity().get(self.latestYear)
        D0 = self.getDividend().get(self.latestYear)
        output = self.divide(currentPrice*R-D0, currentPrice+D0)
        return pd.Series([output], index=[str(int(self.latestYear)+5)])

    def getDividendTerminalForecast(self):
        g5 = self.getDividendGrowthRatebyGordonGrowthModel().get(str(int(self.latestYear)+5))
        return self.divide(self.getDividendForecast().iloc[0]*(1+g5),
                           self.getCostofEquity().get(self.latestYear)-g5)

    def getDividendForecast(self):
        thisYear = self.getDividend().get(self.latestYear)
        g1 = self.getGrowthRatebyPRATModel().get(str(int(self.latestYear)+1))
        g5 = self.getDividendGrowthRatebyGordonGrowthModel().get(str(int(self.latestYear)+5))
        return self.getGrowthRateForecast(g1, g5).apply(np.prod, axis=1)*thisYear

    def getNPVofTerminalValueDDM(self):
        return np.npv(self.getCostofEquity().get(self.latestYear), [0, 0, 0, 0, 0, self.getDividendTerminalForecast()])

    def getNPVofExplicitPeriodDDM(self):
        return np.npv(self.getCostofEquity().get(self.latestYear), self.getDividendForecast().tolist())

    def getStockPriceDDM(self):
        output = self.getNPVofExplicitPeriodDDM()+self.getNPVofTerminalValueDDM()
        return pd.Series([output], index=[self.latestYear])

    def setStockPriceDDM(self):
        output = self.getStockPriceDDM()
        self.setOutput(
            0, self.colName["CPriceDDM"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RPriceDDM"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EPriceDDM"], output, self.latestYear)
