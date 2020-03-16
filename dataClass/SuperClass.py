import pandas as pd
import numpy as np


class Super:
    def __init__(self, *args):
        self.latestYear = "2019"
        self.lastYear = "2018"
        self.twoYearsAgo = "2017"
        self.threeYearsAgo = "2016"
        self.fourYearsAgo = "2015"
        self.output = pd.DataFrame()

    def getOutput(self):
        return self.output

    def getTotalAssets(self):
        return self.combinedDF.loc["Total Assets"]

    def getRevenue(self):
        return self.combinedDF.loc["Total Revenue"]

    def getCostofGoodsSold(self):
        return -self.combinedDF.loc["Cost of Goods and Services"]

    def getOperatingCashFlow(self):
        return self.combinedDF.loc["Cash Generated from Operating Activities"]

    def getCapitalExpenditures(self):
        return -self.combinedDF.loc["Purchase/Sale and Disposal of Property, Plant and Equipment, Net"]

    def getCurrentLiabilities(self):
        return self.combinedDF.loc["Total Current Liabilities"]

    def getCurrentAssets(self):
        return self.combinedDF.loc['Total Current Assets']

    def getStockholdersEquity(self):
        return self.combinedDF.loc["Total Equity"]

    def getPrice(self):
        return self.priceDF.loc[0, "close"]

    def getShares(self):
        return self.combinedDF.loc['Common Shares Issued']

    def getNetIncome(self):
        return self.combinedDF.loc['Net Income from Continuing Operations']

    def getOperatingIncome(self):
        return self.combinedDF.loc['Total Operating Profit/Loss']

    def getTotalDividend(self):
        return -self.combinedDF.loc['Cash Dividends Paid']

    def getDividend(self):
        return np.divide(self.getTotalDividend(), self.getShares()).dropna().sort_index(ascending=False)

    def getGrossMargin(self):
        return np.divide(self.getRevenue()-self.getCostofGoodsSold(), self.getRevenue())

    def getFreeCashFlow(self):
        return self.getOperatingCashFlow() - self.getCapitalExpenditures()

    def setOutput(self, columnIndex, columnHead, column, year):
        self.output = self.output.rename(columns={columnIndex: columnHead})
        self.output.at[self.company,
                       columnHead] = column[year]
