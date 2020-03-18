import pandas as pd
import numpy as np
import config
from dataClass.SuperData import Super


class Profit(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.colName = config.ProfitName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getOperatingMarin(self):
        return np.divide(self.getOperatingIncome(), self.getRevenue())

    def getROA(self):
        return np.divide(self.getOperatingIncome(), self.getTotalAssets())

    def getROE(self):
        return np.divide(self.getNetIncome(), self.getStockholdersEquity())

    def getAvgROEin5years(self):
        output = self.getROE().head(5).mean()
        return pd.Series([output], index=[self.latestYear])

    def getMinROEin5Years(self):
        output = self.getROE().head(5).min()
        return pd.Series([output], index=[self.latestYear])

    def getMaxROEin5Years(self):
        output = self.getROE().head(5).max()
        return pd.Series([output], index=[self.latestYear])

    def setEPS(self):
        output = self.getEPS()
        self.setOutput(17, self.colName["EPSn3"], output, self.threeYearsAgo)
        self.setOutput(16, self.colName["EPSn2"], output, self.twoYearsAgo)
        self.setOutput(15, self.colName["EPSn1"], output, self.lastYear)
        self.setOutput(14, self.colName["EPS"], output, self.latestYear)

    def setFreeCashFlow(self):
        output = self.getFreeCashFlow()
        self.setOutput(
            13, self.colName["freeCashFlow"], output, self.latestYear)

    def setNetIncome(self):
        output = self.getNetIncome()
        self.setOutput(
            12, self.colName["netIncome"], output, self.latestYear)

    def setOperatingCashFlow(self):
        output = self.getOperatingCashFlow()
        self.setOutput(
            11, self.colName["operatingCashFlow"], output, self.latestYear)

    def setOperatingMarin(self):
        output = self.getOperatingMarin()
        self.setOutput(
            10, self.colName["operatingMargin"], output, self.latestYear)

    def setGrossMargin(self):
        output = self.getGrossMargin()
        self.setOutput(9, self.colName["grossMargin"], output, self.latestYear)

    def setROA(self):
        output = self.getROA()
        self.setOutput(8, self.colName["ROA"], output, self.latestYear)

    def setMinROEin5Years(self):
        output = self.getMinROEin5Years()
        self.setOutput(
            7, self.colName["minROEinFiveyears"], output, self.latestYear)

    def setMaxROEin5Years(self):
        output = self.getMaxROEin5Years()
        self.setOutput(
            6, self.colName["maxROEinFiveyears"], output, self.latestYear)

    def setAvgROEin5years(self):
        output = self.getAvgROEin5years()
        self.setOutput(
            5, self.colName["fiveYearAverageROE"], output, self.latestYear)

    def setROE(self):
        output = self.getROE()
        self.setOutput(4, self.colName["ROEn4"], output, self.fourYearsAgo)
        self.setOutput(3, self.colName["ROEn3"], output, self.threeYearsAgo)
        self.setOutput(2, self.colName["ROEn2"], output, self.twoYearsAgo)
        self.setOutput(1, self.colName["ROEn1"], output, self.lastYear)
        self.setOutput(0, self.colName["ROE"], output, self.latestYear)
