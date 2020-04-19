import os
from API.APICommand import CommandInvoker
from API.GoogleSheetCommand import FetchCompanyAndIndustryInfoCommand
from mainFactory import createInputFactory, createInputPipelineFactory, createTablesFactory, createAnalyzeTablesFactory, createOutputFactory


def mainProcess(company, localFileDict, idNum):
    inputFactory = createInputFactory(**dict(
        localFileDict=localFileDict,
        company=company
    ))
    print(f'Step0: Check Local File Of {company} Exist')
    if (not inputFactory.isMainDataExist()):
        return

    print(f'Step1: Load {company} Input Data')
    rawDataDict = inputFactory.loadTemplate1()

    print(f'Step2: Run {company} Data Pipeline')
    inputPipelineFactory = createInputPipelineFactory()
    reportsDF = inputPipelineFactory.handle(rawDataDict['reportsDF'])

    print(f'Step2-1: Dump {company} RawData Dict')
    companyInfoDF = rawDataDict['companyInfoDF']
    priceDF = rawDataDict['priceDF']
    revenueEstimateDF = rawDataDict['revenueEstimateDF']
    treasuriesYieldDF = rawDataDict['treasuriesYieldDF']
    dividendRecordDF = rawDataDict['dividendRecordDF']
    myStockDF = rawDataDict['myStockDF']
    myDividendRecorDF = rawDataDict['myDividendRecorDF']

    print(f'Step3: Create {company} Level 1 Tables')
    tablesFactory = createTablesFactory(
        **dict(
            reportsDF=reportsDF,
            priceDF=priceDF,
            companyInfoDF=companyInfoDF,
            treasuriesYieldDF=treasuriesYieldDF,
            revenueEstimateDF=revenueEstimateDF,
            company=company
        )
    )
    parsTable = tablesFactory.createParsTable()
    priceTable = tablesFactory.createPriceTable()

    print(f'Step4: Create {company} Level 2 Tables')
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
    print(f'Step5: Create {company} MyStock Table')
    if company in myStockDF.axes[0].values:
        sellDecisionTable = analyzeTablesFactory.createSellDecisionTable(
            **dict(
                scoreTable=scoreTable,
                priceTable=priceTable,
                company=company,
                myStockDF=myStockDF,
                myDividendRecorDF=myDividendRecorDF
            )
        )
    else:
        sellDecisionTable = None

    print(f'Step6: Upload {company} Data to Cloud')
    outputFactory = createOutputFactory(
        **dict(
            idNum=idNum,
            company=company,
            tables=dict(
                Pars=parsTable,
                Price=priceTable,
                Analysis=scoreTable,
                BuyDecision=buyDecisionTable,
                SellDecision=sellDecisionTable
            )
        )
    )
    outputFactory.uploadData()


def getLocalFileDict():
    companysPath = os.path.expanduser("~/FinancialData")
    return {
        companyFolder.name: dict(
            reportList=[ele for ele in os.scandir(companyFolder.path)],
            isReportExist=len(
                [ele for ele in os.scandir(companyFolder.path)]) > 0
        ) for companyFolder in os.scandir(companysPath) if not companyFolder.name.startswith('.')
    }


def getCompanyInfoList():
    invoker = CommandInvoker()
    invoker.setCommand(FetchCompanyAndIndustryInfoCommand())
    return invoker.getDataFromAPI()


def main():
    i = 7
    localFileDict = getLocalFileDict()
    for company in getCompanyInfoList():
        mainProcess(company, localFileDict, i)
        i = i+1


if __name__ == '__main__':
    main()
