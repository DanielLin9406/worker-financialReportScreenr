import io
import os
import time
import datetime
import json
import pandas as pd
import Config.pathConfig as pathConfig
from pathlib import Path
from dotenv import load_dotenv
from CreateTables.SellDecisionTableStrategy import getBidDate
from Worker.worker import isColumnExist, getDF, fetchUrlWithLog, requestRetrySession, saveDFtoFile
load_dotenv()


def getUnixTimeStamp(firstBidTime):
    year = int(firstBidTime[0][0])
    month = int(firstBidTime[0][1])
    day = int(firstBidTime[0][2])
    d = datetime.date(year, month, day)
    return str(int(time.mktime(d.timetuple())))

# TODO
# Output Format


def getRevenueEstimate(company, fileName=pathConfig.cache+'revenueEstimate.csv'):
    parName1 = ''.join([company, '-low'])
    parName2 = ''.join([company, '-growth'])
    if Path(fileName).is_file() and isColumnExist([parName1, parName2], fileName):
        return getDF([parName1, parName2], fileName)
    else:
        url = ''.join(['https://query1.finance.yahoo.com/v10/finance/quoteSummary/',
                       company, '?modules=earningsTrend'])
        urlName = 'Yahoo Finance QuoteSummary API'
        content = fetchUrlWithLog(url, requestRetrySession, urlName)
        forcast1Quarter = None
        forcast1Year = None
        try:
            trendDict = json.loads(
                content)["quoteSummary"]["result"][0]["earningsTrend"]["trend"]
            forcast1Year = trendDict[2]["revenueEstimate"]
            forcast2Year = trendDict[3]["revenueEstimate"]
        except Exception as x:
            print('JSON Parse failed when getting estimate revenue :(',
                  x.__class__.__name__)
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

# TODO
# Output Format


def getDividendRecord(company, fileName=pathConfig.cache+'dividendRecord.csv'):
    parName1 = ''.join([company, '-amount'])
    parName2 = ''.join([company, '-date'])
    firstBidUnixTimestamp = getUnixTimeStamp([[2014, 1, 3]])
    if Path(fileName).is_file() and isColumnExist([parName1, parName2], fileName):
        return getDF([parName1, parName2], fileName)
    else:
        url = ''.join(['https://query1.finance.yahoo.com/v8/finance/chart/',
                       company, '?period1=', firstBidUnixTimestamp, '&period2=9999999999&interval=1d&includePrePost=false&events=div%2Csplit'])
        urlName = 'Yahoo Finance Chart API'
        content = fetchUrlWithLog(url, requestRetrySession, urlName)
        try:
            dividendDict = json.loads(
                content)["chart"]["result"][0]["events"]["dividends"]
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            DF = pd.DataFrame(dividendDict).rename(
                {'amount': parName1, 'date': parName2}, axis='index')
            print(DF)
            return saveDFtoFile(DF, [parName1, parName2], fileName)

# TODO
# Output Format


def getMyDividendRecord(myStockDF, company, fileName=pathConfig.cache+'myDividendRecord.csv'):
    parName1 = ''.join([company, '-amount'])
    parName2 = ''.join([company, '-date'])
    firstBidTime = getBidDate(myStockDF)
    firstBidUnixTimestamp = getUnixTimeStamp(firstBidTime)
    if Path(fileName).is_file() and isColumnExist([parName1, parName2], fileName):
        return getDF([parName1, parName2], fileName)
    else:
        url = ''.join(['https://query1.finance.yahoo.com/v8/finance/chart/',
                       company, '?period1=', firstBidUnixTimestamp, '&period2=9999999999&interval=1d&includePrePost=false&events=div%2Csplit'])
        urlName = 'Yahoo Finance Chart API'
        content = fetchUrlWithLog(url, requestRetrySession, urlName)
        try:
            dividendDict = json.loads(
                content)["chart"]["result"][0]["events"]["dividends"]
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            DF = pd.DataFrame(dividendDict).rename(
                {'amount': parName1, 'date': parName2}, axis='index')
            return saveDFtoFile(DF, [parName1, parName2], fileName)
