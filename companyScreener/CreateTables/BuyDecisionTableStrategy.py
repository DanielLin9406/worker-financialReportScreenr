import pandas as pd
import Config.config as config
from .Context import Context


def createBuyDecisionTable(priceTable, analyzedTable, company):
    result = pd.DataFrame()
    stockPriceName = config.BuyDecisionTable["stockPrice"]
    finalScoreName = config.BuyDecisionTable['finalScore']
    investmentName = config.BuyDecisionTable["investmentType"]
    discountPremiumName = config.BuyDecisionTable["DiscountPremiumOfFCFE"]
    result.at[company, stockPriceName] = priceTable.get(
        stockPriceName).loc[company]
    result.at[company, finalScoreName] = analyzedTable.get(
        finalScoreName).loc[company]
    result.at[company, investmentName] = analyzedTable.get(
        investmentName).loc[company]
    result.at[company, discountPremiumName] = priceTable.get(
        discountPremiumName).loc[company]
    return result


class BuyDecisionStrategy:
    def __init__(self, priceTable, scoreTable, company):
        self._resultDF = pd.DataFrame()
        self._priceTable = priceTable
        self._scoreTable = scoreTable
        self._company = company

    def setResultDF(self, company):
        stockPriceName = config.BuyDecisionTable["stockPrice"]
        finalScoreName = config.BuyDecisionTable['finalScore']
        investmentName = config.BuyDecisionTable["investmentType"]
        discountPremiumName = config.BuyDecisionTable["DiscountPremiumOfFCFE"]
        priceTable = self._priceTable
        scoreTable = self._scoreTable

        self._resultDF.at[company, stockPriceName] = priceTable.get(
            stockPriceName).loc[company]
        self._resultDF.at[company, finalScoreName] = scoreTable.get(
            finalScoreName).loc[company]
        self._resultDF.at[company, investmentName] = scoreTable.get(
            investmentName).loc[company]
        self._resultDF.at[company, discountPremiumName] = priceTable.get(
            discountPremiumName).loc[company]

    @property
    def doAlgorithm(self):
        return self._resultDF

    @doAlgorithm.setter
    def doAlgorithm(self, kwargs):
        company = kwargs.get('company')
        self.setResultDF(company)


def BuyDecisionTable(**kwargs):
    scoreTable = kwargs.get('scoreTable')
    priceTable = kwargs.get('priceTable')
    company = kwargs.get('company')
    context = Context(**dict(
        company=company,
    ))
    context.strategy = BuyDecisionStrategy(priceTable, scoreTable, company)
    buydecisionDF = context.doSummarizedAlgorithm()
    return buydecisionDF
