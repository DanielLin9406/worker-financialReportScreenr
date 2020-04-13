import pandas as pd
import numpy as np
import Config.config as config
from .Super import Super
from .AvgPrice import AvgPrice


class Price(Super):
    def __init__(self, **kwargs):
        thisYear = kwargs.get('combinedDF').columns[0]
        super().__init__(thisYear)
        self.colName = config.PriceName
        self.combinedDF = kwargs.get('combinedDF')
        self.priceDF = kwargs.get('priceDF')
        self.treasuriesYieldDF = kwargs.get('treasuriesYieldDF')
        self.revenueEstimateDF = kwargs.get('revenueEstimateDF')
        self.company = kwargs.get('company')

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

    def getMarginOfSafety(self):
        return pd.Series(config.marginOfSafety,  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getRetentionRate(self):
        return self.divide(self.getNetIncome()-self.getTotalDividend(), self.getNetIncome())

    def getPerpetualGrowthRatebyGordonGrowthModel(self):
        currentPrice = self.getPrice().get(self.latestYear)
        R = self.getDiscountRate().get(self.latestYear)
        D0 = self.getDividend().get(self.latestYear)
        output = self.divide(currentPrice*R-D0, currentPrice+D0)
        return pd.Series([output], index=[str(int(self.latestYear)+5)])

    def getPerpetualGrowthRatebySingleStageModel(self):
        equityMarketValue = self.getPrice().get(self.latestYear) * \
            self.getShares().get(self.latestYear)
        R = self.getDiscountRate().get(self.latestYear)
        FCFE0 = self.getFCFE().get(self.latestYear)
        output = self.divide(equityMarketValue*R-FCFE0,
                             equityMarketValue+FCFE0)
        return pd.Series([output], index=[str(int(self.latestYear)+5)])

    def getGrowthRateByPRATModel(self):
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
        return self.getDividend()*np.power(1+self.getHighGrowthRate(), self.getHighGrowthPeriod())

    def setDividendAfterNYears(self):
        output = self.getDividendAfterNYears()
        self.setOutput(
            0, self.colName["dividendAfterNYears"], output, self.latestYear)

    def setDiscountRate(self):
        output = self.getDiscountRate()
        self.setOutput(
            0, self.colName["discountRate"], output, self.latestYear)

    def setMarginOfSafety(self):
        output = self.getMarginOfSafety()
        self.setOutput(
            0, self.colName["marginOfSafety"], output, self.latestYear)

    def setTreasuriesYield(self):
        output = self.getTreasuriesYield()
        self.setOutput(
            0, self.colName["treasuriesYield"], output, self.latestYear)

    def setDividend(self):
        output = self.getDividend()
        self.setOutput(0, self.colName["dividend"], output, self.latestYear)

    def setStockPrice(self):
        output = self.getPrice()
        self.setOutput(
            0, self.colName["stockPrice"], output, self.latestYear)
