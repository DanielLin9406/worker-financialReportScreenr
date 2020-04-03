import config
import re
import pandas as pd
import numpy as np
import datetime


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


def getHPR(stockPrice, myStockDF, returnOfDividendArr):
    bidArr = getRawBid(myStockDF)
    currentPrice = stockPrice
    returnOfDividend = np.sum(returnOfDividendArr)
    returnOfInvestment = currentPrice + returnOfDividend
    return np.divide(returnOfInvestment - bidArr[0], bidArr[0])


def getAverageRR(stockPrice, myStockDF, returnOfDividendArr):
    bidArr = getRawBid(myStockDF)
    bidDate = getBidDate(myStockDF)
    years = getDurationInYear(getNow(), datetime.datetime(
        int(bidDate[0][0]), int(bidDate[0][1]), int(bidDate[0][2])))
    returnOfInvestment = stockPrice + np.sum(returnOfDividendArr)
    return np.divide((returnOfInvestment-bidArr[0])*years, bidArr[0])


def getAnnualizedRR(stockPrice, myStockDF, returnOfDividendArr):
    bidArr = getRawBid(myStockDF)
    bidDateArr = getBidDate(myStockDF)
    years = getDurationInYear(getNow(), datetime.datetime(
        int(bidDateArr[0][0]), int(bidDateArr[0][1]), int(bidDateArr[0][2])))
    returnOfInvestment = stockPrice + np.sum(returnOfDividendArr)
    return np.power(np.divide(returnOfInvestment, bidArr[0]), years) - 1


def getIRR(stockPrice, myStockDF, returnOfDividendArr):
    data = []
    bidArr = getRawBid(myStockDF)
    data.extend([-i for i in bidArr])
    data.extend(returnOfDividendArr)
    data.append(stockPrice)
    return np.irr(data)


def getDividendRecord(myDividendRecorDF, company):
    if myDividendRecorDF.empty:
        return []
    else:
        return myDividendRecorDF.T.get(company+'-amount').tolist()


def createSellDecisionTable(priceTable, analyzedTable, company, myStockDF, myDividendRecorDF):
    result = pd.DataFrame()
    investmentName = config.SellDecisionTable["investmentType"]
    finalScoreName = config.SellDecisionTable['finalScore']
    lastYearInvestmentName = config.SellDecisionTable["lastYearInvestmentType"]
    lastYearFinalScoreName = config.SellDecisionTable['lastYearFinalScore']
    dividend = config.SellDecisionTable['dividend']
    stockPriceName = config.SellDecisionTable["stockPrice"]
    discountPremiumName = config.SellDecisionTable["DiscountPremiumOfFCFE"]

    returnOfDividendArr = getDividendRecord(myDividendRecorDF, company)
    stockPrice = priceTable.get(stockPriceName).loc[company]
    IRR = getIRR(stockPrice, myStockDF, returnOfDividendArr)
    AnnualizedRR = getAnnualizedRR(stockPrice, myStockDF, returnOfDividendArr)
    AverageRR = getAverageRR(stockPrice, myStockDF, returnOfDividendArr)
    HPR = getHPR(stockPrice, myStockDF, returnOfDividendArr)

    result.at[company, investmentName] = analyzedTable.get(
        investmentName).loc[company]
    result.at[company, finalScoreName] = analyzedTable.get(
        finalScoreName).loc[company]
    result.at[company, lastYearInvestmentName] = analyzedTable.get(
        investmentName).loc[company]
    result.at[company, lastYearFinalScoreName] = analyzedTable.get(
        finalScoreName).loc[company]
    result.at[company, dividend] = np.sum(returnOfDividendArr)
    result.at[company, stockPriceName] = stockPrice
    result.at[company, discountPremiumName] = priceTable.get(
        discountPremiumName).loc[company]
    result.at[company, 'IRR'] = IRR
    result.at[company, 'AnnualizedRR'] = AnnualizedRR
    result.at[company, 'AverageRR'] = AverageRR
    result.at[company, 'HPR'] = HPR
    return result
