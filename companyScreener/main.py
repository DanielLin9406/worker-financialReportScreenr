from worker import filterEmptyDataSource, readReport, concatTable, formatedTable, getStockPrice, getTreasuriesYield
from ParsTable.CreateParsTable import createParsTable
from PriceTable.CreatePriceTable import createPriceTable
from CriteriaTable.CreateCriteriaTable import analyzeData
import pathlib as plib
import pandas as pd
import os


def cleanDataWorker(dir):
    rawDFDict = readReport(dir)
    DFDict = filterEmptyDataSource(rawDFDict)
    CombinedDF = concatTable(DFDict)
    return formatedTable(CombinedDF)


def mainProcess(dir, company):
    formatedCombinedDF = cleanDataWorker(dir)
    priceDF = getStockPrice(company)
    treasuriesYieldDF = getTreasuriesYield()

    parasTable = createParsTable(
        formatedCombinedDF, [priceDF], company)
    priceTable = createPriceTable(
        formatedCombinedDF, [priceDF, treasuriesYieldDF], company)
    analyzedTable = analyzeData(parasTable, company)
    print(pd.concat([parasTable, priceTable, analyzedTable], axis=1))


def main(path):
    for dirpath, dirs, files in os.walk(path):
        if len(dirs) > 0:
            for company in dirs:
                companyFoldrStr = os.path.expanduser(
                    "~/FinancialData/"+company)
                if (len(list(plib.Path(companyFoldrStr).glob("*.xls")))):
                    companyFoldrPath = plib.Path(companyFoldrStr).glob("*.xls")
                    mainProcess(companyFoldrPath, company)


if __name__ == '__main__':
    path = os.path.expanduser("~/FinancialData")
    main(path)
