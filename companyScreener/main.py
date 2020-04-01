import os
import pathlib as plib
import pandas as pd
import time
from ParsTable.CreateParsTable import createParsTable
from PriceTable.CreatePriceTable import createPriceTable
from CriteriaTable.CreateCriteriaTable import analyzeData
from GoogleSheetAPI.GoogleSheetAPI import upload2Sheet, createCompanyAndIndustryInfo
from worker import getStockPrice, getTreasuriesYield, cleanDataWorker, getRevenueEstimate


def mainProcess(dir, company, idNum):
    print('Start to Process data of', company)
    formatedCombinedDF = cleanDataWorker(dir)
    priceDF = getStockPrice(company)
    revenueEstimateDF = getRevenueEstimate(company)
    treasuriesYieldDF = getTreasuriesYield()

    parasTable = createParsTable(
        formatedCombinedDF, [priceDF], company)
    priceTable = createPriceTable(
        formatedCombinedDF, [priceDF, treasuriesYieldDF, revenueEstimateDF], company)
    analyzedTable = analyzeData(parasTable, company)
    print('Get Stock Name from Google Sheet at:', company)
    companyTable = createCompanyAndIndustryInfo('Company', company)
    newparasTable = pd.concat([companyTable, parasTable], axis=1)
    print('Finish Getting Stock Name from Google Sheet at:', company)

    # print('Start to upload to Google Sheet at:', company)
    # upload2Sheet(newparasTable, 'Pars', company, idNum)
    upload2Sheet(priceTable, 'Price', company, idNum)
    # upload2Sheet(analyzedTable, 'Analysis', company, idNum)
    # print('Finish Uploading to Google Sheet at:', company)


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
