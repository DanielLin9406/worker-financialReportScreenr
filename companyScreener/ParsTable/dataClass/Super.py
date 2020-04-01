import pandas as pd
import numpy as np
import time
# np.seterr(divide='ignore', invalid='ignore')


class Super:
    def __init__(self, thisYear):
        self.latestYear = str(int(thisYear))
        self.lastYear = str(int(thisYear)-1)
        self.twoYearsAgo = str(int(thisYear)-2)
        self.threeYearsAgo = str(int(thisYear)-3)
        self.fourYearsAgo = str(int(thisYear)-4)
        self.output = pd.DataFrame()

    def getOutput(self):
        return self.output

    def getTotalAssets(self):
        return self.getParsSeries("Total Assets")

    def getTotalLiabilities(self):
        return self.getParsSeries("Total Liabilities")

    def getRevenue(self):
        return self.getParsSeries("Total Revenue")

    def getCostofGoodsSold(self):
        return -self.getParsSeries("Cost of Revenue")

    def getResearch(self):
        return -self.getParsSeries("Research and Development Expenses")

    def getOperatingCashFlow(self):
        return self.getParsSeries("Cash Generated from Operating Activities")

    def getCapitalExpenditures(self):
        parNameList = ['Capital Expenditure, Reported',
                       'Purchase/Sale and Disposal of Property, Plant and Equipment, Net']
        return -self.getParsSeries(parNameList)

    def getCurrentLiabilities(self):
        return self.getParsSeries("Total Current Liabilities")

    def getCurrentAssets(self):
        return self.getParsSeries('Total Current Assets')

    def getStockholdersEquity(self):
        return self.getParsSeries("Total Equity")

    def getPrice(self):
        return pd.Series([self.priceDF.iloc[0]], index=[self.latestYear], dtype="float")

    def getPretaxIncome(self):
        return self.getParsSeries('Pretax Income')

    def getShares(self):
        return self.getParsSeries('Common Shares Issued')

    def getNetIncome(self):
        return self.getParsSeries('Net Income from Continuing Operations')

    def getOperatingIncome(self):
        return self.getParsSeries('Total Operating Profit/Loss')

    def getTotalDividend(self):
        return -self.getParsSeries('Cash Dividends Paid')

    def getOperatingExpenses(self):
        return -self.getParsSeries("Operating Income/Expenses")

    def getDefaultSeries(self):
        return pd.Series([0., 0., 0., 0., 0.], index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def sum(self, SeriesList):
        return np.sum(SeriesList, axis=0)
        # .sort_index(ascending=False)

    def divide(self, SerieA, SerieB):
        # print(np.nonzero(SerieB.tolist()))
        output = np.divide(SerieA, SerieB)
        return output

    def getParsSeries(self, parNamePool, alterNative=None):
        def checkSeriesInDF(parName):
            return parName in self.combinedDF.index

        def getSeriesFromDF(parName):
            if parName in self.combinedDF.index:
                return self.combinedDF.loc[parName]

        def getSeriesFromPlanB(alterNative):
            if alterNative is not None:
                return alterNative()
            else:
                return self.getDefaultSeries()

        if type(parNamePool) == list:
            while(len(parNamePool) > 0):
                parName = parNamePool.pop(0)
                if checkSeriesInDF(parName) == True:
                    return getSeriesFromDF(parName)
            return getSeriesFromPlanB(alterNative)
        else:
            if checkSeriesInDF(parNamePool) == True:
                return getSeriesFromDF(parNamePool)
            else:
                return getSeriesFromPlanB(alterNative)

    def getNetIncomeMargin(self):
        return self.divide(self.getNetIncome(), self.getRevenue())

    def getFinancialLeverage(self):
        return self.divide(self.getTotalAssets(), self.getStockholdersEquity())

    def getAssetTurnoverRatio(self):
        return self.divide(self.getRevenue()*2, self.getTotalAssets().shift(periods=-1)+self.getTotalAssets())

    def getChangeInWorkingCapital(self):
        if (self.getCurrentLiabilities().sum() == 0 and self.getCurrentAssets().sum() == 0):
            return self.getDefaultSeries()
        else:
            # print('Liabilities', self.getCurrentLiabilities())
            # print('assets', self.getCurrentAssets())
            return self.divide(self.getCurrentLiabilities(), self.getCurrentAssets())

    def getDividend(self):
        return self.divide(self.getTotalDividend(), self.getShares()).sort_index(ascending=False)

    def getGrossMargin(self):
        return self.divide(self.getRevenue()-self.getCostofGoodsSold(), self.getRevenue())

    def getFreeCashFlow(self):
        return self.getOperatingCashFlow() - self.getCapitalExpenditures()

    def getEPS(self):
        return self.divide(self.getNetIncome(), self.getShares())

    def getEBIT(self):
        return self.getRevenue()-self.getFreeCashFlow()-self.getOperatingExpenses()

    def getOperatingIncomeGrowth(self):
        latestYear = self.getOperatingIncome().get(self.latestYear)
        lastYear = self.getOperatingIncome().get(self.lastYear)
        twoYearsAgo = self.getOperatingIncome().get(self.twoYearsAgo)
        threeYearsAgo = self.getOperatingIncome().get(self.threeYearsAgo)
        output1 = self.divide((latestYear-lastYear), lastYear)
        output2 = self.divide((lastYear-twoYearsAgo), twoYearsAgo)
        output3 = self.divide((twoYearsAgo-threeYearsAgo), threeYearsAgo)
        return pd.Series([output1, output2, output3], index=[self.latestYear, self.lastYear, self.twoYearsAgo])

    def getEPSGrowth3YearAvg(self):
        return np.power(self.divide(self.getEPS(), self.getEPS().shift(periods=-3)), (np.divide(1, 3)))-1

    def getEPSGrowth(self):
        latestYear = self.getEPS().get(self.latestYear)
        lastYear = self.getEPS().get(self.lastYear)
        output = self.divide((latestYear-lastYear), lastYear)
        return pd.Series([output], index=[self.latestYear])

    def setOutput(self, columnIndex, columnHead, column, year):
        self.output = self.output.rename(columns={columnIndex: columnHead})
        self.output.at[self.company,
                       columnHead] = 0 if pd.isnull(column[year]) else column[year]
