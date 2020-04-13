import os
import pathlib as plib
import pandas as pd
import numpy as np
import time
from abc import ABC, abstractmethod, abstractproperty
# from CreateTables.ScoreTableStrategy import createAnalyzeTable  # ,  # AnalyzeTable
# from CreateTables.BuyDecisionTableStrategy import createBuyDecisionTable
# from CreateTables.SellDecisionTableStrategy import createSellDecisionTable
from API.GoogleSheetAPI import upload2Sheet, getCompanyAndIndustryInfo, getMyStock
from API.AlphaVantage import getStockPrice
from API.YahooFinance import getRevenueEstimate, getDividendRecord, getMyDividendRecord
from API.Quandl import getTreasuriesYield
from CreateTables.TableAbstractFactory import TablesFactory, AnalyzeTablesFactory
from Input.InputTemplate import InputTemplateFromFile
from InputPipeline.PipelineHandler import initHandler, concatTableHandler, leftSpaceStripHandler, transStrToFloatHandler


# def readReport(fileList):
#     Dict = {}
#     List = []
#     for file in fileList:
#         tabName = file.name.split(' ')[0].lower()
#         List.append(tabName)
#         Dict[tabName] = pd.read_excel(
#             file, index_col=0)
#     return {"Dict": Dict, "List": List}


# def filterEmptyDataSource(data):
#     List = data["List"]
#     if len(List) == 0:
#         return
#     return data["Dict"]


# def concatTable(financialDFDict):
#     balanceDF = financialDFDict["balance"]
#     cashDF = financialDFDict["cash"]
#     incomeDF = financialDFDict["income"]
#     return pd.concat([balanceDF, cashDF, incomeDF])


# def formatedTable(financialDFCombined):
#     filterLeftSpaceDL = financialDFCombined.rename(index=lambda x: x.lstrip())
#     transToFloatDL = filterLeftSpaceDL.apply(
#         lambda x: x.iloc[0:].str.replace(',', '').astype(np.float))
#     return transToFloatDL


# def cleanDataWorker(DFDict):
#     CombinedDF = concatTable(DFDict)
#     return formatedTable(CombinedDF)


# def transIterator2FileList(fileIterator):
#     return [ele for ele in fileIterator]


# class AbstractAPIFactory(ABC):


# class AbstractOutputFactory(ABC):

# class AbstractMyStockFactory(ABC):


def createInputFactory(**kwargs):
    factory = InputTemplateFromFile(**kwargs)
    return factory


def createInputPipelineFactory():
    factory = initHandler()
    concatTable = concatTableHandler()
    leftSpaceStrip = leftSpaceStripHandler()
    transStrToFloat = transStrToFloatHandler()
    factory.setNext(concatTable).setNext(
        leftSpaceStrip).setNext(transStrToFloat)
    return factory


def createTablesFactory(**kwargs):
    factory = TablesFactory(**kwargs)
    return factory


def createAnalyzeTablesFactory():
    factory = AnalyzeTablesFactory()
    return factory


def mainProcess(entry, idNum):
    company = entry.name
    fileIterator = os.scandir(entry.path)

    # Done
    # New
    print('Step1: Create Input Factory', company)
    inputFactory = createInputFactory(**dict(
        fileIterator=fileIterator
    ))
    if (not inputFactory.isInputExist()):
        return
    rawData = inputFactory.getData()
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
    standardDF = inputPipelineFactory.handle(rawData)
    # Old
    # standardDF = cleanDataWorker(DFDict)
    # print('old', standardDF)

    # TODO
    print('Step3: Create API Factory', company)
    priceDF = getStockPrice(company)
    revenueEstimateDF = getRevenueEstimate(company)
    treasuriesYieldDF = getTreasuriesYield()
    companyInfoDF = getCompanyAndIndustryInfo('Company', company)
    dividendRecordDF = getDividendRecord(company)

    # Done
    # NEW
    print('Step4: Create Level 1 Tables Factory', company)
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
    print('Step5: Create Level 2 Tables Factory', company)
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
    print('new scoreTable', scoreTable)
    print('new buyDecisionTable', buyDecisionTable)
    # OLD
    # scoreTable = createAnalyzeTable(parsTable, company)
    # buyDecisionTable = createBuyDecisionTable(priceTable, scoreTable, company)

    print('Step6: Create Output Factory', company)
    # upload2Sheet(parsTable, 'Pars', company, idNum)
    # upload2Sheet(priceTable, 'Price', company, idNum)
    # upload2Sheet(analyzedTable, 'Analysis', company, idNum)
    # upload2Sheet(buyDecisionTable, 'BuyDecision', company, idNum)
    # print('Finish Uploading to Google Sheet at:', company)

    print('Step7: Create MyStock Factory', company)
    myStockDF = getMyStock('MyStock', company)
    if company not in myStockDF.axes[0].values:
        return

    # Done
    # New
    myDividendRecorDF = getMyDividendRecord(myStockDF, company)
    sellDecisionTable = analyzeTablesFactory.createSellDecisionTable(
        **dict(
            scoreTable=scoreTable,
            priceTable=priceTable,
            company=company,
            myStockDF=myStockDF,
            myDividendRecorDF=myDividendRecorDF
        )
    )
    print('new sellDecisionTable', sellDecisionTable)
    # Old
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
