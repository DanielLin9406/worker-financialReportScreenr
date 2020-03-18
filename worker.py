import quandl
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")


def getStockPrice(company):
    return quandl.get_table('SHARADAR/SEP', ticker=company)


def getTreasuriesYield():
    return quandl.get("USTREASURY/REALYIELD").sort_index(ascending=False).iloc[0]


def formatedTable(financialDFCombined):
    filterLeftSpaceDL = financialDFCombined.rename(index=lambda x: x.lstrip())
    transToFloatDL = filterLeftSpaceDL.apply(
        lambda x: x.iloc[0:].str.replace(',', '').astype(np.float))
    return transToFloatDL


def concatTable(financialDFDict):
    balanceDF = financialDFDict["balance"]
    cashDF = financialDFDict["cash"]
    incomeDF = financialDFDict["income"]
    return pd.concat([balanceDF, cashDF, incomeDF])


def filterEmptyDataSource(data):
    List = data["List"]
    if len(List) == 0:
        return
    return data["Dict"]


def readReport(dir):
    Dict = {}
    List = []
    for file in dir:
        currentTableName = file.name.split(' ')[0].lower()
        List.append(currentTableName)
        Dict[currentTableName] = pd.read_excel(
            file, index_col=0)
    return {"Dict": Dict, "List": List}
