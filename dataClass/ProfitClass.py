import pandas as pd
import numpy as np
from dataClass.SuperClass import Super


class Profit(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.combinedDF = args[0]
        self.priceDF = args[1]
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

    def setFreeCashFlow(self):
        output = self.getFreeCashFlow()
        self.setOutput(12, "Free Cash Flow", output, self.latestYear)

    def setOperatingCashFlow(self):
        output = self.getOperatingCashFlow()
        self.setOutput(11, "Operating Cash Flow", output, self.latestYear)

    def setOperatingMarin(self):
        output = self.getOperatingMarin()
        self.setOutput(10, "Operating Margin", output, self.latestYear)

    def setGrossMargin(self):
        output = self.getGrossMargin()
        self.setOutput(9, "Gross Margin", output, self.latestYear)

    def setROA(self):
        output = self.getROA()
        self.setOutput(8, "ROA", output, self.latestYear)

    def setMinROEin5Years(self):
        output = self.getMinROEin5Years()
        self.setOutput(7, "Min ROE in 5-years", output, self.latestYear)

    def setMaxROEin5Years(self):
        output = self.getMaxROEin5Years()
        self.setOutput(6, "Max ROE in 5-years", output, self.latestYear)

    def setAvgROEin5years(self):
        output = self.getAvgROEin5years()
        self.setOutput(5, "5-years Average ROE", output, self.latestYear)

    def setROE(self):
        output = self.getROE()
        self.setOutput(4, "ROE(n-4)", output, self.fourYearsAgo)
        self.setOutput(3, "ROE(n-3)", output, self.threeYearsAgo)
        self.setOutput(2, "ROE(n-2)", output, self.twoYearsAgo)
        self.setOutput(1, "ROE(n-1)", output, self.lastYear)
        self.setOutput(0, "ROE", output, self.latestYear)
