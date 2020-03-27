import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class DCF(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getDiscountRate(self):
        return pd.Series(config.DCF["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def perpetualGrowthRate(self):
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
            {'1 Year': str(int(self.latestYear)+1), '2 Year': str(int(self.latestYear)+2)}, axis='index')

    def getGrowthRate(self):
        output = self.renameRevenueEstimateDF().get(
            ''.join([self.company, '-growth'])).dropna().mean()
        return pd.Series([output, output, output, output], index=[str(int(self.latestYear)+1), str(int(self.latestYear)+2), str(int(self.latestYear)+3), str(int(self.latestYear)+4)])

    def getGrowthRateForecastDCF(self):
        g = self.getGrowthRate().get(str(int(self.latestYear)+1))
        return pd.DataFrame({
            'g1': [1, 1, 1, 1+float(g)],
            'g2': [1, 1, 1+float(g), 1+float(g)]},
            index=[str(int(self.latestYear)+1), str(int(self.latestYear)+2), str(int(self.latestYear)+3), str(int(self.latestYear)+4)])

    def getRevenueForcast(self):
        revenueForcastFromExperts = self.renameRevenueEstimateDF().get(
            ''.join([self.company, '-low']))
        revenueForcastFromModel = pd.Series([revenueForcastFromExperts.get(str(int(self.latestYear)+2)), revenueForcastFromExperts.get(
            str(int(self.latestYear)+2))], index=[str(int(self.latestYear)+3), str(int(self.latestYear)+4)])
        return revenueForcastFromExperts.append(
            revenueForcastFromModel)*self.getGrowthRateForecastDCF().apply(np.prod, axis=1)

    def getNetIncomeForcast(self):
        return self.getRevenueForcast()*self.getAvgNetIncomeMargin().get(str(int(self.latestYear)+1))

    def getFreeCashFlowForcast(self):
        return self.getNetIncomeForcast().sort_index(ascending=False)*self.getAvgFCFNetIncomeRatio().get(str(int(self.latestYear)+1))

    def getFreeCashFlowTerminalForecast(self):
        return self.divide(self.getFreeCashFlowForcast().iloc[0]*(1+self.perpetualGrowthRate().get(self.latestYear)), self.getDiscountRate().get(self.latestYear)-self.perpetualGrowthRate().get(self.latestYear))

    def getNPVofTerminalValueFreeCashFlow(self):
        return np.npv(self.getDiscountRate().get(self.latestYear),
                      [0, 0, 0, self.getFreeCashFlowTerminalForecast()])

    def getNPVofExplicitPeriodFreeCashFlow(self):
        return np.npv(self.getDiscountRate().get(self.latestYear), self.getFreeCashFlowForcast().tolist())

    def getEquityValueDCF(self):
        return self.getNPVofExplicitPeriodFreeCashFlow()+self.getNPVofTerminalValueFreeCashFlow()

    def getStockPriceDCF(self):
        return self.divide(self.getEquityValueDCF(), self.getShares())

    def setStockPriceDCF(self):
        output = self.getStockPriceDCF()
        self.setOutput(
            0, self.colName["CPriceDCF"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RPriceDCF"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EPriceDCF"], output, self.latestYear)
