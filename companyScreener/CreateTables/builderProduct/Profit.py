import pandas as pd
import numpy as np
import Config.config as config
from .Super import Super


class Profit(Super):
    def __init__(self, **kwargs):
        thisYear = kwargs.get('reportsDF').columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.ProfitName
        self.reportsDF = kwargs.get('reportsDF')
        self.priceDF = kwargs.get('priceDF')
        self.company = kwargs.get('company')

    def getOperatingMarin(self):
        return self.divide(self.getOperatingIncome(), self.getRevenue())

    def getROS(self):
        return self.divide(self.getNetIncome(), self.getRevenue())

    def getROA(self):
        return self.getNetIncomeMargin()*self.getAssetTurnoverRatio()

    def getROE(self):
        return self.getNetIncomeMargin()*self.getAssetTurnoverRatio()*self.getFinancialLeverage()

    def getYearPercentageOfHighROE(self):
        output = self.divide(
            np.sum(self.getROE().dropna().gt(0.15)), len(self.getROE().dropna()))
        # print(output)
        return pd.Series([output], index=[self.latestYear])

    def getAvgROEin4years(self):
        output = self.getROE().head(4).mean()
        return pd.Series([output], index=[self.latestYear])

    def getMinROEin4Years(self):
        output = self.getROE().head(4).min()
        return pd.Series([output], index=[self.latestYear])

    def getMaxROEin4Years(self):
        output = self.getROE().head(4).max()
        return pd.Series([output], index=[self.latestYear])

    def setEPS(self):
        output = self.getEPS()
        self.setOutput(0, self.colName["EPS"], output, self.latestYear)
        self.setOutput(0, self.colName["EPSn1"], output, self.lastYear)
        self.setOutput(0, self.colName["EPSn2"], output, self.twoYearsAgo)
        self.setOutput(0, self.colName["EPSn3"], output, self.threeYearsAgo)

    def setNetIncome(self):
        output = self.getNetIncome()
        self.setOutput(
            0, self.colName["netIncome"], output, self.latestYear)

    def setOperatingCashFlow(self):
        output = self.getOperatingCashFlow()
        self.setOutput(
            0, self.colName["operatingCashFlow"], output, self.latestYear)

    def setOperatingMarin(self):
        output = self.getOperatingMarin()
        self.setOutput(
            0, self.colName["operatingMargin"], output, self.latestYear)

    def setROS(self):
        output = self.getROS()
        self.setOutput(0, self.colName["ROS"], output, self.latestYear)

    def setROA(self):
        output = self.getROA()
        self.setOutput(0, self.colName["ROA"], output, self.latestYear)

    def setYearPercentageOfHighROE(self):
        output = self.getYearPercentageOfHighROE()
        self.setOutput(
            0, self.colName["yearPercentageOfHighROE"], output, self.latestYear)

    def setMinROEin4Years(self):
        output = self.getMinROEin4Years()
        self.setOutput(
            0, self.colName["minROEinFouryears"], output, self.latestYear)

    def setMaxROEin4Years(self):
        output = self.getMaxROEin4Years()
        self.setOutput(
            0, self.colName["maxROEinFourYears"], output, self.latestYear)

    def setAvgROEin4years(self):
        output = self.getAvgROEin4years()
        self.setOutput(
            0, self.colName["fourYearAverageROE"], output, self.latestYear)

    def setROE(self):
        output = self.getROE()
        self.setOutput(0, self.colName["ROE"], output, self.latestYear)
        self.setOutput(0, self.colName["ROEn1"], output, self.lastYear)
        self.setOutput(0, self.colName["ROEn2"], output, self.twoYearsAgo)
        self.setOutput(0, self.colName["ROEn3"], output, self.threeYearsAgo)
