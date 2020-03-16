import pandas as pd
import numpy as np
from dataClass.SuperClass import Super


class Dividend(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.combinedDF = args[0]
        self.priceDF = args[1]
        self.company = args[2]

    def getAvgDividendin5years(self):
        output = self.getDividend().head(5).mean()
        return pd.Series([output], index=[self.latestYear])

    def getMinDividendin5Years(self):
        output = self.getDividend().head(5).min()
        return pd.Series([output], index=[self.latestYear])

    def getMaxDividendin5Years(self):
        output = self.getDividend().head(5).max()
        return pd.Series([output], index=[self.latestYear])

    def getDividendGrowthin5Years(self):
        latestYear = self.getDividend().get(self.latestYear)
        fourYearsAgo = self.getDividend().get(self.fourYearsAgo)
        output = np.divide((latestYear-fourYearsAgo), fourYearsAgo)
        return pd.Series([output], index=[self.latestYear])

    def getDividendGrowthin3Years(self):
        latestYear = self.getDividend().get(self.latestYear)
        twoYearsAgo = self.getDividend().get(self.twoYearsAgo)
        output = np.divide((latestYear-twoYearsAgo), twoYearsAgo)
        return pd.Series([output], index=[self.latestYear])

    def isDividendGrowthin3Years(self):
        sortByYear = self.getDividend().head(3)
        sortByDividend = self.getDividend().head(3).sort_values(ascending=False)
        output = sortByYear.equals(sortByDividend)
        return pd.Series([output], index=[self.latestYear])

    def getDividendYield(self):
        return np.divide(self.getDividend(), self.getPrice())

    def getPayoutRatio(self):
        return np.divide(self.getTotalDividend(), self.getNetIncome())

    def setPayoutRatio(self):
        output = self.getPayoutRatio()
        self.setOutput(9, "Payout ratio", output, self.latestYear)

    def setDividendYield(self):
        output = self.getDividendYield()
        self.setOutput(8, "Divided Yield", output, self.latestYear)

    def setDividendGrowthin5Years(self):
        output = self.getDividendGrowthin5Years()
        self.setOutput(7, "5-year Average Divided Growth",
                       output, self.latestYear)

    def setDividendGrowthin3Years(self):
        output = self.getDividendGrowthin3Years()
        self.setOutput(6, "3-year Average Divided Growth",
                       output, self.latestYear)

    def setIsDividendGrowthin3Years(self):
        output = self.isDividendGrowthin3Years()
        self.setOutput(5, "Is Divided Growth in 3 year",
                       output, self.latestYear)

    def setMinDividendin5Years(self):
        output = self.getMinDividendin5Years()
        self.setOutput(4, "Min Divided in 5-years", output, self.latestYear)

    def setMaxDividendin5Years(self):
        output = self.getMaxDividendin5Years()
        self.setOutput(3, "Max Divided in 5-years", output, self.latestYear)

    def setAvgDividendin5years(self):
        output = self.getAvgDividendin5years()
        self.setOutput(2, "5-years Average Divided", output, self.latestYear)

    def setTotalDivideds(self):
        output = self.getTotalDividend()
        self.setOutput(1, "Total Divideds", output, self.latestYear)

    def setDividend(self):
        output = self.getDividend()
        self.setOutput(0, "Divided", output, self.latestYear)
