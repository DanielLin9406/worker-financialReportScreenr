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
# from Output.upload2Sheet import upload2Sheet
from mainFactory import createInputFactory, createInputPipelineFactory, createTablesFactory, createAnalyzeTablesFactory, createOutputFactory


# def mainProcess(entry, idNum):
def mainProcess(company, localFileDict, idNum):
    # company = entry.name
    # fileIterator = os.scandir(entry.path)

    # Done
    # New
    print('Step1: Create Input Factory', company)
    inputFactory = createInputFactory(**dict(
        # fileIterator=fileIterator,
        localFileDict=localFileDict,
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
    # # companyInfoDF = getCompanyAndIndustryInfo('Company', company)
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
    # New
    outputFactory = createOutputFactory(
        **dict(
            idNum=idNum,
            company=company,
            tables=dict(
                Pars=priceTable,
                Price=priceTable,
                Analysis=scoreTable,
                BuyDecision=buyDecisionTable
            )
        )
    )
    outputFactory.uploadData()
    # OLD
    # upload2Sheet(parsTable, 'Pars', company, idNum)
    # upload2Sheet(priceTable, 'Price', company, idNum)
    # upload2Sheet(scoreTable, 'Analysis', company, idNum)
    # upload2Sheet(buyDecisionTable, 'BuyDecision', company, idNum)

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


# def scanFolderTree(folder):
#     i = 7
#     for entry in os.scandir(folder):
#         if entry.is_dir(follow_symlinks=False):
#             mainProcess(entry, i)
#             i = i+1

# def main(path):
#     path = os.path.expanduser("~/FinancialData")
#     scanFolderTree(path)

def getLocalFileDict():
    filePath = os.path.expanduser("~/FinancialData")
    return {file.name: dict(fileIterator=os.scandir(file.path)) for file in os.scandir(
        filePath) if not file.name.startswith('.')}


def main(companyList=['V']):
    i = 7
    localFileDict = getLocalFileDict()
    for company in companyList:
        mainProcess(company, localFileDict, i)
        i = i+1


if __name__ == '__main__':
    main()
