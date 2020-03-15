import quandl
import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()


def getStockPrice(company):
    quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")
    return quandl.get_table('SHARADAR/SEP', ticker=company)


def clearSpaceinTable(financialDFCombined):
    filterLeftSpaceDL = financialDFCombined.rename(index=lambda x: x.lstrip())
    transToFloatDL = filterLeftSpaceDL.apply(
        lambda x: x.iloc[0:].str.replace(',', '').astype(np.float))
    return transToFloatDL


def concatTable(financialDFDict):
    balanceDF = financialDFDict["balance"]
    cashDF = financialDFDict["cash"]
    incomeDF = financialDFDict["income"]
    return pd.concat([balanceDF, cashDF, incomeDF])


def filterEmptyDataFrame(data):
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
