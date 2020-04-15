import os
# import pathlib as plib
# import pandas as pd
# import numpy as np
# import time
# from CreateTables.ScoreTableStrategy import createAnalyzeTable  # ,  # AnalyzeTable
# from CreateTables.BuyDecisionTableStrategy import createBuyDecisionTable
# from CreateTables.SellDecisionTableStrategy import createSellDecisionTable
# from API.GoogleSheet import getCompanyAndIndustryInfo, getMyStock
# from API.AlphaVantage import getStockPrice
# from API.YahooFinance import getRevenueEstimate, getDividendRecord, getMyDividendRecord
# from API.Quandl import getTreasuriesYield
from Output.upload2Sheet import upload2Sheet
from mainFactory import createInputFactory, createInputPipelineFactory, createTablesFactory, createAnalyzeTablesFactory


def mainProcess(entry, idNum):
    company = entry.name
    fileIterator = os.scandir(entry.path)

    # Done
    # New
    print('Step1: Create Input Factory', company)
    inputFactory = createInputFactory(**dict(
        fileIterator=fileIterator,
        company=company
    ))
    if (not inputFactory.isInputExist()):
        return
    rawDataDict = inputFactory.loadTemplate1()
    # rawDataDict: {'CombinedDF': DF, 'PriceDF': DF, ...}
    # OLD
    # fileList = transIterator2FileList(fileIterator)
    # if (len(fileList) == 0):
    #     return
    # rawDFDict = readReport(fileList)
    # DFDict = filterEmptyDataSource(rawDFDict)
    # 把Company Info 加入pipeLine
    # companyInfoDF = getCompanyAndIndustryInfo('Company', company)
    # DONE
    # New
    print('Step2: Create Input Pipeline Factory', company)
    inputPipelineFactory = createInputPipelineFactory()
    standardDF = inputPipelineFactory.handle(rawDataDict['combinedDF'])

    print('Step2-1: Dump RawData Dict', company)
    companyInfoDF = rawDataDict['companyInfoDF']
    priceDF = rawDataDict['priceDF']
    revenueEstimateDF = rawDataDict['revenueEstimateDF']
    treasuriesYieldDF = rawDataDict['treasuriesYieldDF']
    dividendRecordDF = rawDataDict['dividendRecordDF']
    myStockDF = rawDataDict['myStockDF']
    myDividendRecorDF = rawDataDict['myDividendRecorDF']

    # Old
    # standardDF = cleanDataWorker(DFDict)
    # print('old', standardDF)

    # Done
    # Old
    # print('Step3: Create API Factory', company)
    # # priceDF = getStockPrice(company)
    # # revenueEstimateDF = getRevenueEstimate(company)
    # # treasuriesYieldDF = getTreasuriesYield()
    # # dividendRecordDF = getDividendRecord(company)

    # Done
    # NEW
    print('Step3: Create Level 1 Tables Factory', company)
    tablesFactory = createTablesFactory(
        **dict(
            combinedDF=standardDF,
            priceDF=priceDF,
            companyInfoDF=companyInfoDF,
            treasuriesYieldDF=treasuriesYieldDF,
            revenueEstimateDF=revenueEstimateDF,
            company=company
        )
    )
    parsTable = tablesFactory.createParsTable()
    priceTable = tablesFactory.createPriceTable()
    # OLD
    # parsTable = createParsTable(
    #     standardDF, [priceDF, companyInfoDF], company)
    # priceTable = createPriceTable(
    #     standardDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company)

    # Done
    print('Step4: Create Level 2 Tables Factory', company)
    # New
    analyzeTablesFactory = createAnalyzeTablesFactory()
    scoreTable = analyzeTablesFactory.createScoreTable(
        **dict(
            parsTable=parsTable,
            company=company
        )
    )
    buyDecisionTable = analyzeTablesFactory.createBuyDecisionTable(
        **dict(
            scoreTable=scoreTable,
            priceTable=priceTable,
            company=company
        )
    )
    # print('new scoreTable', scoreTable)
    # print('new buyDecisionTable', buyDecisionTable)
    # OLD
    # scoreTable = createAnalyzeTable(parsTable, company)
    # buyDecisionTable = createBuyDecisionTable(priceTable, scoreTable, company)

    print('Step5: Create Output Factory', company)
    # upload2Sheet(parsTable, 'Pars', company, idNum)
    # upload2Sheet(priceTable, 'Price', company, idNum)
    # upload2Sheet(analyzedTable, 'Analysis', company, idNum)
    # upload2Sheet(buyDecisionTable, 'BuyDecision', company, idNum)
    # print('Finish Uploading to Google Sheet at:', company)

    print('Step6: Create MyStock Factory', company)
    if company not in myStockDF.axes[0].values:
        return

    # Done
    # New
    sellDecisionTable = analyzeTablesFactory.createSellDecisionTable(
        **dict(
            scoreTable=scoreTable,
            priceTable=priceTable,
            company=company,
            myStockDF=myStockDF,
            myDividendRecorDF=myDividendRecorDF
        )
    )
    # print('new sellDecisionTable', sellDecisionTable)
    # Old
    # myDividendRecorDF = getMyDividendRecord(myStockDF, company)
    # sellDecisionTable = createSellDecisionTable(
    #     priceTable, scoreTable, company, myStockDF, myDividendRecorDF)
    # print('old', sellDecisionTable)
    # print('Start to upload to Google Sheet at:', company)
    # upload2Sheet(sellDecisionTable, 'SellDecision', company, idNum)


def scanFolderTree(folder):
    i = 7
    for entry in os.scandir(folder):
        if entry.is_dir(follow_symlinks=False):
            mainProcess(entry, i)
            i = i+1


def main(path):
    scanFolderTree(path)


if __name__ == '__main__':
    path = os.path.expanduser("~/FinancialData")
    main(path)
