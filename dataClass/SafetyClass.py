import pandas as pd
import numpy as np
from dataClass.SuperClass import Super


class Safety(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.combinedDF = args[0]
        self.priceDF = args[1]
        self.company = args[2]

    def getLongTermDebt(self):
        return self.combinedDF.loc["Long Term Debt"]

    def getShortTermDebt(self):
        return self.combinedDF.loc["Current Debt"]

    def getTotalLiabilities(self):
        return self.combinedDF.loc["Total Liabilities"]

    def getTotalAssests(self):
        return self.combinedDF.loc["Total Assets"]

    def getOtherCurrentAssets(self):
        return self.combinedDF.loc["Other Current Assets"]

    def getInventory(self):
        return self.combinedDF.loc["Inventories"]

    def getCurrentRatio(self):
        return np.divide(self.getCurrentAssets(), self.getCurrentLiabilities())

    def getQuickRatio(self):
        return np.divide(self.getCurrentAssets()-self.getOtherCurrentAssets()-self.getInventory(), self.getCurrentLiabilities())

    def getDebtEquityRatio(self):
        return np.divide(self.getTotalLiabilities(), self.getStockholdersEquity())

    def getDebtCapitalRatio(self):
        return np.divide(self.getShortTermDebt()+self.getLongTermDebt(), self.getShortTermDebt()+self.getLongTermDebt()+self.getStockholdersEquity())

    def getDebtAssetsRatio(self):
        return np.divide(self.getTotalLiabilities(), self.getTotalAssests())

    def getDividendsFCFRatio(self):
        return np.divide(self.getDividend(), self.getFreeCashFlow())

    def getSharesCapital(self):
        return self.getShares()

    def setSharesCapital(self):
        output = self.getSharesCapital()
        self.setOutput(11, "Share Capital", output, self.lastYear)
        self.setOutput(10, "Share Capital", output, self.latestYear)

    def setDividendsFCFRatio(self):
        output = self.getDividendsFCFRatio()
        self.setOutput(9, "Dividends/FCF Ratio", output, self.latestYear)

    def setDebtAssetsRatio(self):
        output = self.getDebtAssetsRatio()
        self.setOutput(8, "Debt/Assets Ratio", output, self.latestYear)

    def setDebtCapitalRatio(self):
        output = self.getDebtCapitalRatio()
        self.setOutput(7, "Debt/Capital Ratio", output, self.latestYear)

    def setDebtEquityRatio(self):
        output = self.getDebtEquityRatio()
        self.setOutput(6, "Debt/Equity Ratio", output, self.latestYear)

    def setQuickRatio(self):
        output = self.getQuickRatio()
        self.setOutput(5, "Quick Ratio", output, self.latestYear)

    def setCurrentRatio(self):
        output = self.getCurrentRatio()
        self.setOutput(4, "Current Ratio(N-1)", output, self.lastYear)
        self.setOutput(3, "Current Ratio", output, self.latestYear)

    def setLongTermDebt(self):
        output = self.getLongTermDebt()
        self.setOutput(1, "Long-Term Debt(N-1)", output, self.lastYear)
        self.setOutput(0, "Long-Term Debt", output, self.latestYear)
