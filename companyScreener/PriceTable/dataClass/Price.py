import pandas as pd
import numpy as np
import config
from ParsTable.dataClass.Super import Super


class Price(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        super().__init__(thisYear)
        self.colName = config.PriceName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.treasuriesYieldDF = args[1][1]
        self.revenueEstimateDF = args[1][2]
        self.company = args[2]

    def getTreasuriesYield(self):
        return pd.Series(self.treasuriesYieldDF.iloc[0][0]/100, index=[self.latestYear], dtype="float")

    def getDepreciation(self):
        return self.getParsSeries("Depreciation, Amortization and Depletion, Non-Cash Adjustment")

    def getNetBorrowings(self):
        return self.getParsSeries("Issuance of/Repayments for Long Term Debt, Net")

    def getNetCashFromOperation(self):
        return self.getParsSeries("Net Cash Flow from Continuing Operating Activities, Indirect")

    def getShortTermDebtIssuance(self):
        return self.getParsSeries("Issuance of/Repayments for Short Term Debt, Net")

    def getTaxRate(self):
        return pd.Series(config.FCFF["taxRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getCostOfCapital(self):
        return pd.Series(config.FCFF["costOfCapital"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getCostofEquity(self):
        return pd.Series(config.FCFE["costOfEquity"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getInfiniteGrowthRateFCFF(self):
        return pd.Series(config.FCFF["infiniteGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getDiscountRate(self):
        return pd.Series(config.DDM2["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getTerminalYieldGrowth(self):
        return pd.Series(config.DDM2["terminalYieldGrowth"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getYieldGrowthRate(self):
        return pd.Series(config.DDM2["yieldGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthPeriod(self):
        return pd.Series(config.DDM2["highGrowthPeriod"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getMarginOfSafety(self):
        return pd.Series(config.marginOfSafety,  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getRetentionRate(self):
        return self.divide(self.getNetIncome()-self.getTotalDividend(), self.getNetIncome())

    def getGrowthRatebyPRATModel(self):
        MeanRetentionRate = self.getRetentionRate().drop(index='TTM').mean()
        MeanNetIncomeMargin = self.getNetIncomeMargin().drop(index='TTM').mean()
        MeanAssetTurnoverRatio = self.getAssetTurnoverRatio().drop(
            index='TTM').dropna().mean()
        MeanFinancialLeverage = self.getFinancialLeverage().drop(index='TTM').dropna().mean()
        output = MeanRetentionRate*MeanNetIncomeMargin * \
            MeanAssetTurnoverRatio*MeanFinancialLeverage
        return pd.Series([output], index=[str(int(self.latestYear)+1)])

    def getGrowthRateForecast(self, initialGrowthRate, terminalGrowthRate):
        g1 = initialGrowthRate
        g5 = terminalGrowthRate
        g2 = g1 + self.divide((g5-g1)*(2-1), 5-1)
        g3 = g1 + self.divide((g5-g1)*(3-1), 5-1)
        g4 = g1 + self.divide((g5-g1)*(4-1), 5-1)
        return pd.DataFrame({'0': [1+float(g1), 1+float(g1), 1+float(g1), 1+float(g1), 1+float(g1)],
                             '1': [1, 1+float(g2), 1+float(g2), 1+float(g2), 1+float(g2)],
                             '2': [1, 1, 1+float(g3), 1+float(g3), 1+float(g3)],
                             '3': [1, 1, 1, 1+float(g4), 1+float(g4)],
                             '4': [1, 1, 1, 1, 1+float(g5)]},
                            index=[str(int(self.latestYear)+1), str(int(self.latestYear)+2), str(int(self.latestYear)+3), str(int(self.latestYear)+4), str(int(self.latestYear)+5)]).sort_index(ascending=False)

    def getDividendAfterNYears(self):
        return self.getDividend()*np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod())

    def setStockPrice(self):
        output = self.getPrice()
        self.setOutput(
            7, self.colName["stockPrice"], output, self.latestYear)

    def setTreasuriesYield(self):
        output = self.getTreasuriesYield()
        self.setOutput(
            6, self.colName["treasuriesYield"], output, self.latestYear)

    def setDividendAfterNYears(self):
        output = self.getDividendAfterNYears()
        self.setOutput(
            5, self.colName["dividendAfterNYears"], output, self.latestYear)

    def setMarginOfSafety(self):
        output = self.getMarginOfSafety()
        self.setOutput(
            4, self.colName["marginOfSafety"], output, self.latestYear)

    def setDiscountRate(self):
        output = self.getDiscountRate()
        self.setOutput(
            3, self.colName["discountRate"], output, self.latestYear)

    def setTerminalYieldGrowth(self):
        output = self.getTerminalYieldGrowth()
        self.setOutput(
            2, self.colName["terminalYieldGrowth"], output, self.latestYear)

    def setYieldGrowthRate(self):
        output = self.getYieldGrowthRate()
        self.setOutput(
            1, self.colName["yieldGrowthRate"], output, self.latestYear)

    def setHighGrowthPeriod(self):
        output = self.getHighGrowthPeriod()
        self.setOutput(
            0, self.colName["highGrowthPeriod"], output, self.latestYear)
