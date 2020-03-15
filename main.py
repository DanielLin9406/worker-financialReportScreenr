from worker import filterEmptyDataFrame, readReport, concatTable, clearSpaceinTable, getStockPrice
from valueInvestment import createValueInvestment
import pathlib as plib
import os


def mainProcess(dir, company):
    data = readReport(dir)
    financialDFDict = filterEmptyDataFrame(data)
    financialDFCombined = concatTable(financialDFDict)
    financialDFCombinedFormated = clearSpaceinTable(financialDFCombined)
    priceDF = getStockPrice(company)
    valueInvestmentTable = createValueInvestment(
        financialDFCombinedFormated, priceDF, company)
    print(valueInvestmentTable)


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
