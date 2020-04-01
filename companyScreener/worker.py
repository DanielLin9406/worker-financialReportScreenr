import os
import io
import time
import quandl
import pandas as pd
import numpy as np
import json
import requests

from pathlib import Path
from dotenv import load_dotenv
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


def isColumnExist(company, fileName):
    if (type(company) == list):
        while(len(company) > 0):
            return company.pop() in readSeriesFromFile(fileName).index
        return False
    else:
        return company in readSeriesFromFile(fileName).index


def readSeriesFromFile(fileName):
    try:
        return pd.read_csv(fileName, index_col=0)
    except Exception as x:
        print('Read CSV failed :(', x.__class__.__name__)
        return pd.DataFrame()


def getSeriesInDF(company, fileName):
    return readSeriesFromFile(fileName).loc[company]


def saveDFtoFile(df, company, fileName):
    df.to_csv(fileName, mode='a')
    return df.loc[company]


def fetchUrlWithLog(url, function, urlName):
    t0 = time.time()
    try:
        response = function().get(url)
    except Exception as x:
        print('Request failed :(', x.__class__.__name__)
    else:
        print('Request eventually worked', response.status_code)
    finally:
        t1 = time.time()
        print('Took', t1 - t0, 'seconds to fetch from', urlName)
        return response.content


def getStockPrice(company, fileName='price.csv'):
    if Path(fileName).is_file() and isColumnExist(company, fileName):
        # if file exist read from file
        return getSeriesInDF(company, fileName)
    else:
        # if file not exist call api and save in file
        url = ''.join(['https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=',
                       company, '&apikey=', alphaVantageAPIKey, '&datatype=csv'])
        urlName = 'Alphavantage'
        content = fetchUrlWithLog(url, requestRetrySession, urlName)
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        time.sleep(20)
        priceDF = df.T.loc[['timestamp', 'close']].rename(
            {'timestamp': 'timestamp', 'close': company}, axis='index')
        return saveDFtoFile(priceDF, company, fileName)


def getRevenueEstimate(company, fileName='revenueEstimate.csv'):
    parName1 = ''.join([company, '-low'])
    parName2 = ''.join([company, '-growth'])
    if Path(fileName).is_file() and isColumnExist([parName1, parName2], fileName):
        return getSeriesInDF([parName1, parName2], fileName)
    else:
        url = ''.join(['https://query1.finance.yahoo.com/v10/finance/quoteSummary/',
                       company, '?modules=earningsTrend'])
        urlName = 'Yahoo Finance API'
        content = fetchUrlWithLog(url, requestRetrySession, urlName)
        forcast1Quarter = None
        forcast1Year = None
        try:
            trendDict = json.loads(
                content)["quoteSummary"]["result"][0]["earningsTrend"]["trend"]
            forcast1Year = trendDict[2]["revenueEstimate"]
            forcast2Year = trendDict[3]["revenueEstimate"]
        except Exception as x:
            print('JSON Parse failed :(', x.__class__.__name__)
            return pd.DataFrame()
        else:
            forcast1YearDF = pd.DataFrame(
                forcast1Year).loc['raw'].rename('1 Year')
            forcast2YearDF = pd.DataFrame(
                forcast2Year).loc['raw'].rename('2 Year')
            DF = pd.concat([forcast1YearDF, forcast2YearDF], axis=1)
            NewDF = DF.loc[['low', 'growth']].rename(
                {'low': parName1, 'growth': parName2}, axis='index')
            return saveDFtoFile(NewDF, [parName1, parName2], fileName)


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
