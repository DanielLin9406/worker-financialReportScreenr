import pandas as pd
import Config.config as config
from .Context import Context


# def createBuyDecisionTable(priceTable, analyzedTable, company):
#     result = pd.DataFrame()
#     stockPriceName = config.BuyDecisionTable["stockPrice"]
#     finalScoreName = config.BuyDecisionTable['finalScore']
#     investmentName = config.BuyDecisionTable["investmentType"]
#     discountPremiumName = config.BuyDecisionTable["DiscountPremiumOfFCFE"]
#     result.at[company, stockPriceName] = priceTable.get(
#         stockPriceName).loc[company]
#     result.at[company, finalScoreName] = analyzedTable.get(
#         finalScoreName).loc[company]
#     result.at[company, investmentName] = analyzedTable.get(
#         investmentName).loc[company]
#     result.at[company, discountPremiumName] = priceTable.get(
#         discountPremiumName).loc[company]
#     return result


class BuyDecisionStrategy:
    def __init__(self):
        self._resultDF = pd.DataFrame()

    def setResultDF(self):
        stockPriceName = config.BuyDecisionTable["stockPrice"]
        finalScoreName = config.BuyDecisionTable['finalScore']
        investmentName = config.BuyDecisionTable["investmentType"]
        discountPremiumName = config.BuyDecisionTable["DiscountPremiumOfFCFE"]
        priceTable = self._priceTable
        scoreTable = self._scoreTable
        company = self._company

        self._resultDF.at[company, stockPriceName] = priceTable.get(
            stockPriceName).loc[company]
        self._resultDF.at[company, finalScoreName] = scoreTable.get(
            finalScoreName).loc[company]
        self._resultDF.at[company, investmentName] = scoreTable.get(
            investmentName).loc[company]
        self._resultDF.at[company, discountPremiumName] = priceTable.get(
            discountPremiumName).loc[company]

    def setPars(self, kwargs):
        self._priceTable = kwargs.get('priceTable')
        self._scoreTable = kwargs.get('scoreTable')
        self._company = kwargs.get('company')

    @property
    def doAlgorithm(self):
        return self._resultDF

    @doAlgorithm.setter
    def doAlgorithm(self, kwargs):
        self.setPars(kwargs)
        self.setResultDF()


def BuyDecisionTable(**kwargs):
    """
    @param: DataFrame
    @return: DataFrame
    """
    context = kwargs.get('context')
    context.company = kwargs.get('company')
    context.scoreTable = kwargs.get('scoreTable')
    context.priceTable = kwargs.get('priceTable')
    context.strategy = BuyDecisionStrategy()
    return context.doBuyDecisionAlgorithm()
