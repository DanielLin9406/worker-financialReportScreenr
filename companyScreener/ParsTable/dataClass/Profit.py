import pandas as pd
import config
from ParsTable.dataClass.Super import Super


class Profit(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.ProfitName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getOperatingMarin(self):
        return self.divide(self.getOperatingIncome(), self.getRevenue())

    def getROS(self):
        return self.divide(self.getNetIncome(), self.getRevenue())

    def getROA(self):
        return self.getNetIncomeMargin()*self.getAssetTurnoverRatio()

    def getROE(self):
        return self.getNetIncomeMargin()*self.getAssetTurnoverRatio()*self.getFinancialLeverage()

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
        self.setOutput(14, self.colName["EPS"], output, self.latestYear)
        self.setOutput(15, self.colName["EPSn1"], output, self.lastYear)
        self.setOutput(16, self.colName["EPSn2"], output, self.twoYearsAgo)
        self.setOutput(17, self.colName["EPSn3"], output, self.threeYearsAgo)

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

    # def setGrossMargin(self):
    #     output = self.getGrossMargin()
    #     self.setOutput(9, self.colName["grossMargin"], output, self.latestYear)
    def setROS(self):
        output = self.getROS()
        self.setOutput(9, self.colName["ROS"], output, self.latestYear)

    def setROA(self):
        output = self.getROA()
        self.setOutput(8, self.colName["ROA"], output, self.latestYear)

    def setMinROEin4Years(self):
        output = self.getMinROEin4Years()
        self.setOutput(
            7, self.colName["minROEinFouryears"], output, self.latestYear)

    def setMaxROEin4Years(self):
        output = self.getMaxROEin4Years()
        self.setOutput(
            6, self.colName["maxROEinFouryears"], output, self.latestYear)

    def setAvgROEin4years(self):
        output = self.getAvgROEin4years()
        self.setOutput(
            5, self.colName["fourYearAverageROE"], output, self.latestYear)

    def setROE(self):
        output = self.getROE()
        self.setOutput(0, self.colName["ROE"], output, self.latestYear)
        self.setOutput(1, self.colName["ROEn1"], output, self.lastYear)
        self.setOutput(2, self.colName["ROEn2"], output, self.twoYearsAgo)
        self.setOutput(3, self.colName["ROEn3"], output, self.threeYearsAgo)
        # self.setOutput(4, self.colName["ROEn4"], output, self.fourYearsAgo)
