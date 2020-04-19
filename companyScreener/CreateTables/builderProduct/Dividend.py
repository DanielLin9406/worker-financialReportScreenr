import pandas as pd
import numpy as np
import Config.config as config
from .Super import Super


class Dividend(Super):
    def __init__(self, **kwargs):
        thisYear = kwargs.get('reportsDF').columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.ShareHolderName
        self.reportsDF = kwargs.get('reportsDF')
        self.priceDF = kwargs.get('priceDF')
        self.company = kwargs.get('company')

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
        trimedDividend = self.getDividend()
        series = self.divide(trimedDividend,
                             trimedDividend.shift(periods=-1)).dropna()-1
        output = series.mean()
        return pd.Series([output], index=[self.latestYear])

    def getDividendGrowthin3Years(self):
        trimedDividend = self.getDividend().head(4)
        series = self.divide(trimedDividend,
                             trimedDividend.shift(periods=-1)).dropna()-1
        output = series.mean()
        return pd.Series([output], index=[self.latestYear])

    def getDividendGrowthin2Years(self):
        trimedDividend = self.getDividend().head(3)
        series = self.divide(trimedDividend,
                             trimedDividend.shift(periods=-1)).dropna()-1
        output = series.mean()
        return pd.Series([output], index=[self.latestYear])

    def isDividendGrowthin3Years(self):
        sortByYear = self.getDividend().head(4).drop('TTM').dropna()
        sortByDividend = sortByYear.sort_values(ascending=False)
        output = sortByYear.equals(sortByDividend)
        return pd.Series([str(output)], index=[self.latestYear])

    def getDividendYield(self):
        return self.divide(self.getDividend(), self.getPrice())

    def getPayoutRatio(self):
        return self.divide(self.getTotalDividend(), self.getFreeCashFlow())

    def getDividendGrowth(self):
        latestYear = self.getDividend().get(self.latestYear)
        lastYear = self.getDividend().get(self.lastYear)
        twoYearsAgo = self.getDividend().get(self.twoYearsAgo)
        threeYearsAgo = self.getDividend().get(self.threeYearsAgo)
        output1 = self.divide((latestYear-lastYear), lastYear)
        output2 = self.divide((lastYear-twoYearsAgo), twoYearsAgo)
        output3 = self.divide((twoYearsAgo-threeYearsAgo), threeYearsAgo)
        return pd.Series([output1, output2, output3], index=[self.latestYear, self.lastYear, self.twoYearsAgo])

    def setPayoutRatio(self):
        output = self.getPayoutRatio()
        self.setOutput(0, self.colName["payoutRatio"], output, self.latestYear)

    def setDividendYield(self):
        output = self.getDividendYield()
        self.setOutput(
            0, self.colName["dividendYield"], output, self.latestYear)

    def setDividendGrowthin5Years(self):
        output = self.getDividendGrowthin5Years()
        self.setOutput(0, self.colName["fiveYearAverageDividendGrowth"],
                       output, self.latestYear)

    def setDividendGrowthin3Years(self):
        output = self.getDividendGrowthin3Years()
        self.setOutput(0, self.colName["threeYearAverageDividendGrowth"],
                       output, self.latestYear)

    def setDividendGrowthin2Years(self):
        output = self.getDividendGrowthin2Years()
        self.setOutput(0, self.colName["threeYearAverageDividendGrowth"],
                       output, self.latestYear)

    def setMinDividendin5Years(self):
        output = self.getMinDividendin5Years()
        self.setOutput(
            0, self.colName["minDividendinFiveYears"], output, self.latestYear)

    def setMaxDividendin5Years(self):
        output = self.getMaxDividendin5Years()
        self.setOutput(
            0, self.colName["maxDividendinFiveYears"], output, self.latestYear)

    def setAvgDividendin5years(self):
        output = self.getAvgDividendin5years()
        self.setOutput(
            0, self.colName["fiveYearAverageDividend"], output, self.latestYear)

    def setTotalDivideds(self):
        output = self.getTotalDividend()
        self.setOutput(
            0, self.colName["totalDividend"], output, self.latestYear)

    def setDividendGrowth(self):
        output = self.getDividendGrowth()
        # print(output)
        self.setOutput(
            0, self.colName["dividendGrowth"], output, self.latestYear)
        self.setOutput(
            0, self.colName["dividendGrowthn1"], output, self.lastYear)
        self.setOutput(
            0, self.colName["dividendGrowthn2"], output, self.twoYearsAgo)

    def setDividend(self):
        output = self.getDividend()
        # print(output)
        self.setOutput(0, self.colName["dividend"], output, self.latestYear)
        self.setOutput(0, self.colName["dividendn1"], output, self.lastYear)
        self.setOutput(0, self.colName["dividendn2"], output, self.twoYearsAgo)
