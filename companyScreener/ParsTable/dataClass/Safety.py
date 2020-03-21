import pandas as pd
import numpy as np
import config
from ParsTable.dataClass.Super import Super


class Safety(Super):
    def __init__(self, *args):
        Super.__init__(self)
        self.colName = config.SafetyName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getLongTermDebt(self):
        return self.combinedDF.loc["Long Term Debt"]

    def getShortTermDebt(self):
        return self.combinedDF.loc["Financial Liabilities, Current"]

    def getTotalAssests(self):
        return self.combinedDF.loc["Total Assets"]

    def getOtherCurrentAssets(self):
        return self.combinedDF.loc["Other Current Assets"]

    def getInventory(self):
        return self.getDFfilter("Inventories")

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
        self.setOutput(
            10, self.colName["shareCapital"], output, self.latestYear)
        self.setOutput(
            11, self.colName["shareCapitaln1"], output, self.lastYear)

    def setDividendsFCFRatio(self):
        output = self.getDividendsFCFRatio()
        self.setOutput(
            9, self.colName["dividendsFCFRatio"], output, self.latestYear)

    def setDebtAssetsRatio(self):
        output = self.getDebtAssetsRatio()
        self.setOutput(
            8, self.colName["debtAssetRatio"], output, self.latestYear)

    def setDebtCapitalRatio(self):
        output = self.getDebtCapitalRatio()
        self.setOutput(
            7, self.colName["debtCapitalRatio"], output, self.latestYear)

    def setDebtEquityRatio(self):
        output = self.getDebtEquityRatio()
        self.setOutput(
            6, self.colName["debtEquityRatio"], output, self.latestYear)

    def setQuickRatio(self):
        output = self.getQuickRatio()
        self.setOutput(5, self.colName["quickRatio"], output, self.latestYear)

    def setCurrentRatio(self):
        output = self.getCurrentRatio()
        self.setOutput(
            3, self.colName["currentRatio"], output, self.latestYear)
        self.setOutput(
            4, self.colName["currentRation1"], output, self.lastYear)

    def setLongTermDebt(self):
        output = self.getLongTermDebt()
        self.setOutput(
            0, self.colName["longTermDebt"], output, self.latestYear)
        self.setOutput(
            1, self.colName["longTermDebtn1"], output, self.lastYear)
