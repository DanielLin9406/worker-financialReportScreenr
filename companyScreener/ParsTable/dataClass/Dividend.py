import pandas as pd
import numpy as np
import config
from ParsTable.dataClass.Super import Super


class Dividend(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.ShareHolderName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
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
        output = self.divide((latestYear-fourYearsAgo), fourYearsAgo)
        return pd.Series([output], index=[self.latestYear])

    def getDividendGrowthin3Years(self):
        latestYear = self.getDividend().get(self.latestYear)
        twoYearsAgo = self.getDividend().get(self.twoYearsAgo)
        output = self.divide((latestYear-twoYearsAgo), twoYearsAgo)
        return pd.Series([output], index=[self.latestYear])

    def isDividendGrowthin3Years(self):
        sortByYear = self.getDividend().head(3)
        sortByDividend = self.getDividend().head(3).sort_values(ascending=False)
        output = sortByYear.equals(sortByDividend)
        return pd.Series([output], index=[self.latestYear])

    def getDividendYield(self):
        return self.divide(self.getDividend(), self.getPrice())

    def getPayoutRatio(self):
        return self.divide(self.getTotalDividend(), self.getNetIncome())

    def setPayoutRatio(self):
        output = self.getPayoutRatio()
        self.setOutput(9, self.colName["payoutRatio"], output, self.latestYear)

    def setDividendYield(self):
        output = self.getDividendYield()
        self.setOutput(
            8, self.colName["dividendYield"], output, self.latestYear)

    def setDividendGrowthin5Years(self):
        output = self.getDividendGrowthin5Years()
        self.setOutput(7, self.colName["fiveYearAverageDividendGrowth"],
                       output, self.latestYear)

    def setDividendGrowthin3Years(self):
        output = self.getDividendGrowthin3Years()
        self.setOutput(6, self.colName["threeYearAverageDividendGrowth"],
                       output, self.latestYear)

    def setIsDividendGrowthin3Years(self):
        output = self.isDividendGrowthin3Years()
        self.setOutput(5, self.colName["dividendGrowthinThreeYear"],
                       output, self.latestYear)

    def setMinDividendin5Years(self):
        output = self.getMinDividendin5Years()
        self.setOutput(
            4, self.colName["minDividendinFiveYears"], output, self.latestYear)

    def setMaxDividendin5Years(self):
        output = self.getMaxDividendin5Years()
        self.setOutput(
            3, self.colName["maxDividendinFiveYears"], output, self.latestYear)

    def setAvgDividendin5years(self):
        output = self.getAvgDividendin5years()
        self.setOutput(
            2, self.colName["fiveYearAverageDividend"], output, self.latestYear)

    def setTotalDivideds(self):
        output = self.getTotalDividend()
        self.setOutput(
            1, self.colName["totalDividend"], output, self.latestYear)

    def setDividend(self):
        output = self.getDividend()
        self.setOutput(0, self.colName["dividend"], output, self.latestYear)
