import pandas as pd
import numpy as np


class Super:
    def __init__(self):
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

    def getTotalLiabilities(self):
        return self.combinedDF.loc["Total Liabilities"]

    def getRevenue(self):
        return self.combinedDF.loc["Total Revenue"]

    def getCostofGoodsSold(self):
        return -self.getDFfilter("Cost of Revenue")

    def getOperatingCashFlow(self):
        return self.combinedDF.loc["Cash Generated from Operating Activities"]

    def getCapitalExpenditures(self):
        if 'Capital Expenditure, Reported' in self.combinedDF.index:
            return -self.combinedDF.loc["Capital Expenditure, Reported"]
        else:
            return -self.combinedDF.loc["Purchase/Sale and Disposal of Property, Plant and Equipment, Net"]

    def getCurrentLiabilities(self):
        return self.combinedDF.loc["Total Current Liabilities"]

    def getCurrentAssets(self):
        return self.combinedDF.loc['Total Current Assets']

    def getStockholdersEquity(self):
        return self.combinedDF.loc["Total Equity"]

    def getPrice(self):
        return pd.Series(self.priceDF.loc[0, "close"], index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getPretaxIncome(self):
        return self.combinedDF.loc['Pretax Income']

    def getShares(self):
        return self.combinedDF.loc['Common Shares Issued']

    def getNetIncome(self):
        return self.combinedDF.loc['Net Income from Continuing Operations']

    def getOperatingIncome(self):
        return self.combinedDF.loc['Total Operating Profit/Loss']

    def getTotalDividend(self):
        return -self.combinedDF.loc['Cash Dividends Paid']

    def getOperatingExpenses(self):
        return -self.combinedDF.loc["Operating Income/Expenses"]

    def getAssetTurnoverRatio(self):
        return np.divide(self.getRevenue()*2, self.getTotalAssets().shift(periods=-1)+self.getTotalAssets())

    def getDFfilter(self, parName):
        if parName in self.combinedDF.index:
            return self.combinedDF.loc[parName].fillna(0)
        else:
            return pd.Series([0., 0., 0., 0., 0., 0.], index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo, 'TTM'])

    def getChangeInWorkingCapital(self):
        return np.divide(self.getCurrentLiabilities(), self.getCurrentAssets())

    def getDividend(self):
        return np.divide(self.getTotalDividend(), self.getShares()).dropna().sort_index(ascending=False)

    def getGrossMargin(self):
        return np.divide(self.getRevenue()-self.getCostofGoodsSold(), self.getRevenue())

    def getFreeCashFlow(self):
        return self.getOperatingCashFlow() - self.getCapitalExpenditures()

    def getEPS(self):
        return np.divide(self.getNetIncome(), self.getShares())

    def getEBIT(self):
        return self.getRevenue()-self.getFreeCashFlow()-self.getOperatingExpenses()

    def getOperatingIncomeGrowth(self):
        latestYear = self.getOperatingIncome().get(self.latestYear)
        lastYear = self.getOperatingIncome().get(self.lastYear)
        twoYearsAgo = self.getOperatingIncome().get(self.twoYearsAgo)
        threeYearsAgo = self.getOperatingIncome().get(self.threeYearsAgo)
        output1 = np.divide((latestYear-lastYear), lastYear)
        output2 = np.divide((lastYear-twoYearsAgo), twoYearsAgo)
        output3 = np.divide((twoYearsAgo-threeYearsAgo), threeYearsAgo)
        return pd.Series([output1, output2, output3], index=[self.latestYear, self.lastYear, self.twoYearsAgo])

    def getEPSGrowth(self):
        latestYear = self.getEPS().get(self.latestYear)
        lastYear = self.getEPS().get(self.lastYear)
        output = np.divide((latestYear-lastYear), lastYear)
        return pd.Series([output], index=[self.latestYear])

    def setOutput(self, columnIndex, columnHead, column, year):
        self.output = self.output.rename(columns={columnIndex: columnHead})
        self.output.at[self.company,
                       columnHead] = column[year]
