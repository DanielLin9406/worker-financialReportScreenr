import pandas as pd
import numpy as np
import Config.config as config
from .Price import Price


class DCF(Price):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def getDiscountRate(self):
        return pd.Series(config.DCF["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getPerpetualGrowthRate(self):
        return pd.Series(config.DCF["perpetualGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getFCFNetIncomeRatio(self):
        return self.divide(self.getFreeCashFlow(), self.getNetIncome())

    def getAvgNetIncomeMargin(self):
        output = self.getNetIncomeMargin().drop('TTM').dropna().mean()
        return pd.Series([output], index=[str(int(self.latestYear)+1)])

    def getAvgFCFNetIncomeRatio(self):
        output = self.getFCFNetIncomeRatio().drop('TTM').dropna().mean()
        return pd.Series([output], index=[str(int(self.latestYear)+1)])

    def renameRevenueEstimateDF(self):
        return self.revenueEstimateDF.T.rename(
            {'1 Year': str(int(self.latestYear)+1), '2 Year': str(int(self.latestYear)+2)}, axis='index').astype(float)

    def getGrowthRate(self):
        output = self.renameRevenueEstimateDF().get(
            ''.join([self.company, '-growth'])).dropna().mean()
        return pd.Series([output, output, output, output], index=[str(int(self.latestYear)+1), str(int(self.latestYear)+2), str(int(self.latestYear)+3), str(int(self.latestYear)+4)])

    def getGrowthRateForecast(self):
        g = self.getGrowthRate().get(str(int(self.latestYear)+1))
        return pd.DataFrame({
            'g1': [1, 1, 1, 1+float(g)],
            'g2': [1, 1, 1+float(g), 1+float(g)]},
            index=[str(int(self.latestYear)+1), str(int(self.latestYear)+2), str(int(self.latestYear)+3), str(int(self.latestYear)+4)])

    def getRevenueEstimate(self):
        return self.renameRevenueEstimateDF().get(''.join([self.company, '-low']))

    def getRevenueForcast(self):
        revenueForcastFromModel = pd.Series([self.getRevenueEstimate().get(str(int(self.latestYear)+2)), self.getRevenueEstimate().get(
            str(int(self.latestYear)+2))], index=[str(int(self.latestYear)+3), str(int(self.latestYear)+4)])
        return self.getRevenueEstimate().append(
            revenueForcastFromModel)*self.getGrowthRateForecast().apply(np.prod, axis=1)

    def getNetIncomeForcast(self):
        return self.getRevenueForcast()*self.getAvgNetIncomeMargin().get(str(int(self.latestYear)+1))

    def getFreeCashFlowForcast(self):
        return self.getNetIncomeForcast().sort_index(ascending=False)*self.getAvgFCFNetIncomeRatio().get(str(int(self.latestYear)+1))

    def getFreeCashFlowTerminalForecast(self):
        return self.divide(self.getFreeCashFlowForcast().iloc[0]*(1+self.getPerpetualGrowthRate().get(self.latestYear)), self.getDiscountRate().get(self.latestYear)-self.getPerpetualGrowthRate().get(self.latestYear))

    def getNPVofTerminalValueFreeCashFlow(self):
        return np.npv(self.getDiscountRate().get(self.latestYear),
                      [0, 0, 0, self.getFreeCashFlowTerminalForecast()])

    def getNPVofExplicitPeriodFreeCashFlow(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), self.getFreeCashFlowForcast().tolist())

    def getEquityValue(self):
        return self.getNPVofExplicitPeriodFreeCashFlow()+self.getNPVofTerminalValueFreeCashFlow()

    def getStockPrice(self):
        return self.divide(self.getEquityValue(), self.getShares())

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CPriceDCF"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RPriceDCF"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EPriceDCF"], output, self.latestYear)

    def setAvgFCFNetIncomeRatio(self):
        output = self.getAvgFCFNetIncomeRatio()
        self.setOutput(
            0, self.colName["avgFCFNetIncomeRatio"], output, str(int(self.latestYear)+1))

    def setAvgNetIncomeMargin(self):
        output = self.getAvgNetIncomeMargin()
        self.setOutput(
            0, self.colName["avgNetIncomeMargin"], output, str(int(self.latestYear)+1))

    def setDiscountRate(self):
        output = self.getDiscountRate()
        self.setOutput(
            0, self.colName["discountRate"], output, self.latestYear)

    def setPerpetualGrowthRate(self):
        output = self.getPerpetualGrowthRate()
        self.setOutput(
            0, self.colName["perpetualGrowthRate"], output, self.latestYear)

    def setAvgGrowthRate(self):
        output = self.getGrowthRate()
        self.setOutput(
            0, self.colName["avgGrowthRate"], output, str(int(self.latestYear)+1))

    def setRevenueEstimate(self):
        output = self.getRevenueEstimate()
        self.setOutput(
            0, self.colName["revenueEstimateDCFHalfYear"], output, str(int(self.latestYear)+1))
        self.setOutput(
            0, self.colName["revenueEstimateDCFOneYear"], output, str(int(self.latestYear)+2))
