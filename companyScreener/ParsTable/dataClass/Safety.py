import pandas as pd
import config
from ParsTable.dataClass.Super import Super


class Safety(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.SafetyName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getDebt(self):
        return self.getParsSeries("Debt")

    def getLongTermDebt(self):
        def alterNative():
            return self.getDebt()-self.getShortTermDebt()
        return self.getParsSeries("Long Term Debt", alterNative)

    def getShortTermDebt(self):
        return self.getParsSeries(['Financial Liabilities, Current',
                                   'Other Loans, Current Debt'])

    def getTotalAssests(self):
        return self.getParsSeries("Total Assets")

    def getOtherCurrentAssets(self):
        return self.getParsSeries("Other Current Assets")

    def getInventory(self):
        return self.getParsSeries("Inventories")

    def getCashAndEquivalents(self):
        return self.getParsSeries("Cash, Cash Equivalents and Short Term Investments")

    def getMarketableSecurities(self):
        return self.getParsSeries("Available-for-Sale Securities, Current")

    def getAccountsReceivable(self):
        return self.getParsSeries("Trade and Other Receivables, Current")

    def getCurrentRatio(self):
        return self.divide(self.getCurrentAssets(), self.getCurrentLiabilities())

    def getQuickRatio(self):
        if (self.getInventory().sum() == 0):
            return self.divide(self.getCashAndEquivalents()+self.getMarketableSecurities()+self.getAccountsReceivable(), self.getCurrentLiabilities())
        else:
            return self.divide(self.getCurrentAssets()-self.getOtherCurrentAssets()-self.getInventory(), self.getCurrentLiabilities())

    def getDebtEquityRatio(self):
        return self.divide(self.getShortTermDebt()+self.getLongTermDebt(), self.getStockholdersEquity())

    def getDebtCapitalRatio(self):
        return self.divide(self.getShortTermDebt()+self.getLongTermDebt(), self.getShortTermDebt()+self.getLongTermDebt()+self.getStockholdersEquity())

    def getDebtAssetsRatio(self):
        return self.divide(self.getShortTermDebt()+self.getLongTermDebt(), self.getTotalAssests())

    def getTotalDividendsFCFRatio(self):
        return self.divide(self.getTotalDividend(), self.getFreeCashFlow())

    def getYearPercentageOfPositiveFreeCashFlow(self):
        output = self.divide(
            self.sum(self.getFreeCashFlow().dropna().gt(0)), len(self.getFreeCashFlow().dropna()))
        return pd.Series([output], index=[self.latestYear])

    def getSharesCapital(self):
        return self.getShares()

    def setSharesCapital(self):
        output = self.getSharesCapital()
        self.setOutput(
            0, self.colName["shareCapital"], output, self.latestYear)
        self.setOutput(
            0, self.colName["shareCapitaln1"], output, self.lastYear)

    def setTotalDividendsFCFRatio(self):
        output = self.getTotalDividendsFCFRatio()
        self.setOutput(
            0, self.colName["totalDividendsFCFRatio"], output, self.latestYear)

    def setDebtAssetsRatio(self):
        output = self.getDebtAssetsRatio()
        self.setOutput(
            0, self.colName["debtAssetRatio"], output, self.latestYear)

    def setDebtCapitalRatio(self):
        output = self.getDebtCapitalRatio()
        self.setOutput(
            0, self.colName["debtCapitalRatio"], output, self.latestYear)

    def setDebtEquityRatio(self):
        output = self.getDebtEquityRatio()
        self.setOutput(
            0, self.colName["debtEquityRatio"], output, self.latestYear)

    def setQuickRatio(self):
        output = self.getQuickRatio()
        self.setOutput(0, self.colName["quickRatio"], output, self.latestYear)
        self.setOutput(
            9, self.colName["quickRation1"], output, self.lastYear)

    def setCurrentRatio(self):
        output = self.getCurrentRatio()
        self.setOutput(
            0, self.colName["currentRatio"], output, self.latestYear)
        self.setOutput(
            0, self.colName["currentRation1"], output, self.lastYear)

    def setYearPercentageOfPositiveFreeCashFlow(self):
        output = self.getYearPercentageOfPositiveFreeCashFlow()
        self.setOutput(
            0, self.colName["yearPercentageOfPositiveFreeCashFlow"], output, self.latestYear)

    def setFreeCashFlow(self):
        output = self.getFreeCashFlow()
        self.setOutput(
            0, self.colName["freeCashFlow"], output, self.latestYear)

    def setLongTermDebt(self):
        output = self.getLongTermDebt()
        self.setOutput(
            0, self.colName["longTermDebt"], output, self.latestYear)
        self.setOutput(
            0, self.colName["longTermDebtn1"], output, self.lastYear)

    def setTotalLiabilities(self):
        output = self.getTotalLiabilities()
        self.setOutput(
            0, self.colName["totalLiabilities"], output, self.latestYear)
        self.setOutput(
            0, self.colName["totalLiabilitiesn1"], output, self.lastYear)

    def setTotalAssests(self):
        output = self.getTotalAssests()
        self.setOutput(
            0, self.colName["totalAssets"], output, self.latestYear)
        self.setOutput(
            0, self.colName["totalAssetsn1"], output, self.lastYear)
