import quandl
import os
import io
import time
from pathlib import Path
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
load_dotenv()

quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")
alphaVantageAPIKey = os.getenv("ALPHA_API_KEY")


def cleanDataWorker(dir):
    rawDFDict = readReport(dir)
    DFDict = filterEmptyDataSource(rawDFDict)
    CombinedDF = concatTable(DFDict)
    return formatedTable(CombinedDF)


def requestRetrySession(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def isColumnExist(company):
    return company in readSeriesFromFile().index


def readSeriesFromFile():
    return pd.read_csv('price.csv', index_col=0)


def getSeriesInDF(company):
    return readSeriesFromFile().loc[company]


def saveDFtoFile(df, company):
    # with pd.ExcelWriter('price.csv', mode='a') as writer:
    df.to_csv('price.csv', mode='a')
    return df.loc[company]


def fetchUrlWithLog(url, function):
    t0 = time.time()
    try:
        response = function().get(url)
    except Exception as x:
        print('Request failed :(', x.__class__.__name__)
    else:
        print('Request eventually worked', response.status_code)
    finally:
        t1 = time.time()
        print('Took', t1 - t0, 'seconds')
        csv = response.content
        return pd.read_csv(io.StringIO(csv.decode('utf-8')))


def getStockPrice(company):
    if Path('price.csv').is_file() and isColumnExist(company):
        # if file exist read from file
        return getSeriesInDF(company)
    else:
        # if file not exist call api and save in file
        url = ''.join(['https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=',
                       company, '&apikey=', alphaVantageAPIKey, '&datatype=csv'])
        df = fetchUrlWithLog(url, requestRetrySession)
        time.sleep(20)
        priceDF = df.T.loc[['timestamp', 'close']].rename(
            {'timestamp': 'timestamp', 'close': company}, axis='index')
        return saveDFtoFile(priceDF, company)


def getTreasuriesYield():
    return quandl.get("ML/AAAEY").sort_index(ascending=False)


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
