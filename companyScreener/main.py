import os
import pathlib as plib
import pandas as pd
import time
from ParsTable.CreateParsTable import createParsTable
from PriceTable.CreatePriceTable import createPriceTable
from AnalyzeTable.CreateAnalyzeTable import createAnalyzeTable
from BuyDecisionTable.CreateBuyDecisionTable import createBuyDecisionTable
from SellDecisionTable.CreateSellDecisionTable import createSellDecisionTable
from API.GoogleSheetAPI import upload2Sheet, getCompanyAndIndustryInfo, getMyStock
from API.AlphaVantage import getStockPrice
from API.YahooFinance import getRevenueEstimate, getDividendRecord
from API.Quandl import getTreasuriesYield
from worker import cleanDataWorker


def mainProcess(dir, company, idNum):
    print('Start to Process data of', company)
    formatedCombinedDF = cleanDataWorker(dir)
    priceDF = getStockPrice(company)
    revenueEstimateDF = getRevenueEstimate(company)
    treasuriesYieldDF = getTreasuriesYield()
    companyInfoDF = getCompanyAndIndustryInfo('Company', company)
    myStockDF = getMyStock('MyStock', company)

    parasTable = createParsTable(
        formatedCombinedDF, [priceDF, companyInfoDF], company)
    priceTable = createPriceTable(
        formatedCombinedDF, [priceDF, treasuriesYieldDF, revenueEstimateDF], company)
    analyzedTable = createAnalyzeTable(parasTable, company)
    buyDecisionTable = createBuyDecisionTable(
        priceTable, analyzedTable, company)
    # print('Start to upload to Google Sheet at:', company)
    # upload2Sheet(parasTable, 'Pars', company, idNum)
    # upload2Sheet(priceTable, 'Price', company, idNum)
    # upload2Sheet(analyzedTable, 'Analysis', company, idNum)
    # upload2Sheet(buyDecisionTable, 'BuyDecision', company, idNum)
    # print('Finish Uploading to Google Sheet at:', company)

    if company in myStockDF.axes[0].values:
        myDividendRecorDF = getDividendRecord(myStockDF, company)
        sellDecisionTable = createSellDecisionTable(
            priceTable, analyzedTable, company, myStockDF, myDividendRecorDF)
        print('Start to upload to Google Sheet at:', company)
        upload2Sheet(sellDecisionTable, 'SellDecision', company, idNum)


def main(path):
    for dirpath, dirs, files in os.walk(path):
        if len(dirs) > 0:
            i = 7
            for company in dirs:
                companyFoldrStr = os.path.expanduser(
                    "~/FinancialData/"+company)
                if (len(list(plib.Path(companyFoldrStr).glob("*.xls")))):
                    companyFoldrPath = plib.Path(companyFoldrStr).glob("*.xls")
                    mainProcess(companyFoldrPath, company, i)
                    i = i+1


if __name__ == '__main__':
    path = os.path.expanduser("~/FinancialData")
    main(path)
