from worker import filterEmptyDataSource, readReport, concatTable, formatedTable, getStockPrice, getTreasuriesYield
from createParasTable import createParasTable
from createPriceTable import createPriceTable
from analyzeData import analyzeData
import pathlib as plib
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

    parasTable = createParasTable(
        formatedCombinedDF, [priceDF], company)
    priceTable = createPriceTable(
        formatedCombinedDF, [priceDF, treasuriesYieldDF], company)
    # analyzeData(parasTable)


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
