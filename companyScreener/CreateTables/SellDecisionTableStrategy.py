import re
import datetime
import numpy as np
import pandas as pd
import Config.config as config
from .Context import Context


# def getNow():
#     return datetime.datetime.now()


# def getColumnNameArr(myStockDF):
#     return [ele for ele in myStockDF.columns.values if re.match("Bid/BidDate-*", ele)]


# def getBidDate(myStockDF):
#     bidDateCellArr = [myStockDF.get(bid).iloc[1]
#                       for bid in getColumnNameArr(myStockDF)]
#     return [ele.split("-") for ele in bidDateCellArr]


# def getRawBid(myStockDF):
#     return [float(myStockDF.get(bid).iloc[0][1:]) for bid in getColumnNameArr(myStockDF)]


# def getDurationInYear(now, bidDate):
#     duration = now - bidDate
#     durationInSecond = duration.total_seconds()
#     years = divmod(durationInSecond, 31536000)[0]
#     return years


# def getHPR(stockPrice, myStockDF, returnOfDividendArr):
#     bidArr = getRawBid(myStockDF)
#     currentPrice = stockPrice
#     returnOfDividend = np.sum(returnOfDividendArr)
#     returnOfInvestment = currentPrice + returnOfDividend
#     return np.divide(returnOfInvestment - bidArr[0], bidArr[0])


# def getAverageRR(stockPrice, myStockDF, returnOfDividendArr):
#     bidArr = getRawBid(myStockDF)
#     bidDate = getBidDate(myStockDF)
#     years = getDurationInYear(getNow(), datetime.datetime(
#         int(bidDate[0][0]), int(bidDate[0][1]), int(bidDate[0][2])))
#     returnOfInvestment = stockPrice + np.sum(returnOfDividendArr)
#     return np.divide((returnOfInvestment-bidArr[0])*years, bidArr[0])


# def getAnnualizedRR(stockPrice, myStockDF, returnOfDividendArr):
#     bidArr = getRawBid(myStockDF)
#     bidDateArr = getBidDate(myStockDF)
#     years = getDurationInYear(getNow(), datetime.datetime(
#         int(bidDateArr[0][0]), int(bidDateArr[0][1]), int(bidDateArr[0][2])))
#     returnOfInvestment = stockPrice + np.sum(returnOfDividendArr)
#     return np.power(np.divide(returnOfInvestment, bidArr[0]), years) - 1


# def getIRR(stockPrice, myStockDF, returnOfDividendArr):
#     data = []
#     bidArr = getRawBid(myStockDF)
#     data.extend([-i for i in bidArr])
#     data.extend(returnOfDividendArr)
#     data.append(stockPrice)
#     return np.irr(data)


# def getDividendRecord(myDividendRecorDF, company):
#     if myDividendRecorDF.empty:
#         return []
#     else:
#         return myDividendRecorDF.T.get(company+'-amount').tolist()


# def createSellDecisionTable(priceTable, analyzedTable, company, myStockDF, myDividendRecorDF):

#     result = pd.DataFrame()
#     investmentName = config.SellDecisionTable["investmentType"]
#     finalScoreName = config.SellDecisionTable['finalScore']
#     lastYearInvestmentName = config.SellDecisionTable["lastYearInvestmentType"]
#     lastYearFinalScoreName = config.SellDecisionTable['lastYearFinalScore']
#     dividend = config.SellDecisionTable['dividend']
#     stockPriceName = config.SellDecisionTable["stockPrice"]
#     discountPremiumName = config.SellDecisionTable["DiscountPremiumOfFCFE"]
#     # print('analyzedTable', analyzedTable)
#     returnOfDividendArr = getDividendRecord(myDividendRecorDF, company)
#     stockPrice = priceTable.get(stockPriceName).loc[company]
#     IRR = getIRR(stockPrice, myStockDF, returnOfDividendArr)
#     AnnualizedRR = getAnnualizedRR(stockPrice, myStockDF, returnOfDividendArr)
#     AverageRR = getAverageRR(stockPrice, myStockDF, returnOfDividendArr)
#     HPR = getHPR(stockPrice, myStockDF, returnOfDividendArr)

#     result.at[company, investmentName] = analyzedTable.get(
#         investmentName).loc[company]
#     result.at[company, finalScoreName] = analyzedTable.get(
#         finalScoreName).loc[company]
#     result.at[company, lastYearInvestmentName] = analyzedTable.get(
#         investmentName).loc[company]
#     result.at[company, lastYearFinalScoreName] = analyzedTable.get(
#         finalScoreName).loc[company]
#     result.at[company, dividend] = np.sum(returnOfDividendArr)
#     result.at[company, stockPriceName] = stockPrice
#     result.at[company, discountPremiumName] = priceTable.get(
#         discountPremiumName).loc[company]
#     result.at[company, 'IRR'] = IRR
#     result.at[company, 'AnnualizedRR'] = AnnualizedRR
#     result.at[company, 'AverageRR'] = AverageRR
#     result.at[company, 'HPR'] = HPR
#     return result

def getNow():
    return datetime.datetime.now()


def getColumnNameArr(myStockDF):
    return [ele for ele in myStockDF.columns.values if re.match("Bid/BidDate-*", ele)]


def getBidDate(myStockDF):
    bidDateCellArr = [myStockDF.get(bid).iloc[1]
                      for bid in getColumnNameArr(myStockDF)]
    return [ele.split("-") for ele in bidDateCellArr]


def getRawBid(myStockDF):
    return [float(myStockDF.get(bid).iloc[0][1:]) for bid in getColumnNameArr(myStockDF)]


def getDurationInYear(now, bidDate):
    duration = now - bidDate
    durationInSecond = duration.total_seconds()
    years = divmod(durationInSecond, 31536000)[0]
    return years


class SellDecisionStrategy:
    def __init__(self):
        self._resultDF = pd.DataFrame()
        self._stockPrice = None
        self._ror = dict(
            _IRR=None,
            _annualizedRR=None,
            _averageRR=None,
            _HPR=None
        )
        self._name = dict(
            _investment=None,
            _finalScore=None,
            _lastYearInvestment=None,
            _lastYearFinalScore=None,
            _dividend=None,
            _stockPrice=None,
            _discountPremium=None
        )

    def setPars(self, kwargs):
        self._priceTable = kwargs.get('priceTable')
        self._scoreTable = kwargs.get('scoreTable')
        self._company = kwargs.get('company')
        self._myStockDF = kwargs.get('myStockDF')
        self._myDividendRecorDF = kwargs.get('myDividendRecorDF')
        self.setConfigName()
        self.setStockPrice(
            self._priceTable, self._name['_stockPrice'], self._company)
        self.setDividendArr(self._myDividendRecorDF, self._company)
        self.setIRR()
        self.setAnnualizedRR()
        self.setAverageRR()
        self.setHPR()

    def setConfigName(self):
        self._name['_investment'] = config.SellDecisionTable["investmentType"]
        self._name['_finalScore'] = config.SellDecisionTable['finalScore']
        self._name['_lastYearInvestment'] = config.SellDecisionTable["lastYearInvestmentType"]
        self._name['_lastYearFinalScore'] = config.SellDecisionTable['lastYearFinalScore']
        self._name['_dividend'] = config.SellDecisionTable['dividend']
        self._name['_stockPrice'] = config.SellDecisionTable["stockPrice"]
        self._name['_discountPremium'] = config.SellDecisionTable["DiscountPremiumOfFCFE"]

    def getDividendArr(self):
        return self._dividendRecord

    def setDividendArr(self, myDividendRecorDF, company):
        if myDividendRecorDF.empty:
            self._dividendRecord = []
        else:
            self._dividendRecord = myDividendRecorDF.T.get(
                company+'-amount').tolist()

    def getStockPrice(self):
        return self._stockPrice

    def setStockPrice(self, priceTable, stockPriceName, company):
        self._stockPrice = priceTable.get(stockPriceName).loc[company]

    def getIRR(self):
        return self._ror['_IRR']

    def setIRR(self):
        data = []
        myStockDF = self._myStockDF
        stockPrice = self._stockPrice
        returnOfDividendArr = self._dividendRecord

        bidArr = getRawBid(myStockDF)
        data.extend([-i for i in bidArr])
        data.extend(returnOfDividendArr)
        data.append(stockPrice)
        self._ror['_IRR'] = np.irr(data)

    def getAnnualizedRR(self):
        return self._ror['_annualizedRR']

    def setAnnualizedRR(self):
        data = []
        myStockDF = self._myStockDF
        stockPrice = self._stockPrice
        returnOfDividendArr = self._dividendRecord
        bidArr = getRawBid(myStockDF)
        bidDateArr = getBidDate(myStockDF)
        years = getDurationInYear(getNow(), datetime.datetime(
            int(bidDateArr[0][0]), int(bidDateArr[0][1]), int(bidDateArr[0][2])))
        returnOfInvestment = stockPrice + np.sum(returnOfDividendArr)
        self._ror['_annualizedRR'] = np.power(
            np.divide(returnOfInvestment, bidArr[0]), years) - 1

    def getAverageRR(self):
        return self._ror['_averageRR']

    def setAverageRR(self):
        myStockDF = self._myStockDF
        stockPrice = self._stockPrice
        returnOfDividendArr = self._dividendRecord
        bidArr = getRawBid(myStockDF)
        bidDate = getBidDate(myStockDF)
        years = getDurationInYear(getNow(), datetime.datetime(
            int(bidDate[0][0]), int(bidDate[0][1]), int(bidDate[0][2])))
        returnOfInvestment = stockPrice + np.sum(returnOfDividendArr)
        self._ror['_averageRR'] = np.divide(
            (returnOfInvestment-bidArr[0])*years, bidArr[0])

    def getHPR(self):
        return self._ror['_HPR']

    def setHPR(self):
        myStockDF = self._myStockDF
        stockPrice = self._stockPrice
        returnOfDividendArr = self._dividendRecord
        bidArr = getRawBid(myStockDF)
        currentPrice = stockPrice
        returnOfDividend = np.sum(returnOfDividendArr)
        returnOfInvestment = currentPrice + returnOfDividend
        self._ror['_HPR'] = np.divide(
            returnOfInvestment - bidArr[0], bidArr[0])

    def getValueFromTable(self, table, name):
        company = self._company
        return table.get(name).loc[company]

    def setResultDF(self):
        company = self._company
        scoreTable = self._scoreTable
        priceTable = self._priceTable
        investmentName = self._name['_investment']
        finalScoreName = self._name['_finalScore']
        lastYearInvestmentName = self._name['_lastYearInvestment']
        lastYearFinalScoreName = self._name['_lastYearFinalScore']
        dividend = self._name['_dividend']
        stockPriceName = self._name['_stockPrice']
        discountPremiumName = self._name['_discountPremium']

        self._resultDF.at[company, investmentName] = self.getValueFromTable(
            scoreTable, investmentName)
        self._resultDF.at[company, finalScoreName] = self.getValueFromTable(
            scoreTable, finalScoreName)
        self._resultDF.at[company, lastYearInvestmentName] = self.getValueFromTable(
            scoreTable, investmentName)
        self._resultDF.at[company, lastYearFinalScoreName] = self.getValueFromTable(
            scoreTable, finalScoreName)

        self._resultDF.at[company, dividend] = np.sum(self.getDividendArr())
        self._resultDF.at[company, stockPriceName] = self.getStockPrice()
        self._resultDF.at[company, discountPremiumName] = self.getValueFromTable(
            priceTable, discountPremiumName)

        self._resultDF.at[company, 'IRR'] = self.getIRR()
        self._resultDF.at[company, 'AnnualizedRR'] = self.getAnnualizedRR()
        self._resultDF.at[company, 'AverageRR'] = self.getAverageRR()
        self._resultDF.at[company, 'HPR'] = self.getHPR()

    @property
    def doAlgorithm(self):
        return self._resultDF

    @doAlgorithm.setter
    def doAlgorithm(self, kwargs):
        self.setPars(kwargs)
        self.setResultDF()


def SellDecisionTable(**kwargs):
    """
    @param: DataFrame
    @return: DataFrame
    """
    context = kwargs.get('context')
    context.company = kwargs.get('company')
    context.priceTable = kwargs.get('priceTable')
    context.scoreTable = kwargs.get('scoreTable')
    context.myStockDF = kwargs.get('myStockDF')
    context.myDividendRecorDF = kwargs.get('myDividendRecorDF')
    context.strategy = SellDecisionStrategy()
    return context.doSellDecisionAlgorithm()
