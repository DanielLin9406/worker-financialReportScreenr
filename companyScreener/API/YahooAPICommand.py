import json
import pandas as pd
import Config.pathConfig as pathConfig
from API.APICommand import APICommand
from Worker.dataFrameWorker import getUnixTimeStamp, getBidDate


class FetchRevenueEstimateCommand(APICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName1 = ''.join([self._company, '-low'])
        self._parName2 = ''.join([self._company, '-growth'])
        self._parNameCollection = [self._parName1, self._parName2]
        self._fileName = pathConfig.cache+'revenueEstimate.csv'
        self._url = f'https://query1.finance.yahoo.com/v10/finance/quoteSummary/{self._company}?modules=earningsTrend'
        self._urlName = 'Yahoo Finance QuoteSummary API'

    def APICallback(self, content):
        try:
            trendDict = json.loads(
                content)["quoteSummary"]["result"][0]["earningsTrend"]["trend"]
            forcast1Year = trendDict[2]["revenueEstimate"]
            forcast2Year = trendDict[3]["revenueEstimate"]
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            forcast1YearDF = pd.DataFrame(
                forcast1Year).loc['raw'].rename('1 Year')
            forcast2YearDF = pd.DataFrame(
                forcast2Year).loc['raw'].rename('2 Year')
            DF = pd.concat([forcast1YearDF, forcast2YearDF], axis=1)
            return DF.loc[['low', 'growth']].rename(
                {'low': self._parName1, 'growth': self._parName2}, axis='index')


class FetchDividendRecordCommand(APICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName1 = ''.join([self._company, '-amount'])
        self._parName2 = ''.join([self._company, '-date'])
        self._parNameCollection = [self._parName1, self._parName2]
        self._firstBidUnixTimestamp = getUnixTimeStamp([[2014, 1, 3]])
        self._fileName = pathConfig.cache+'dividendRecord.csv'
        self._url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self._company}?period1={self._firstBidUnixTimestamp}&period2=9999999999&interval=1d&includePrePost=false&events=div%2Csplit'
        self._urlName = 'Yahoo Finance Chart API'

    def APICallback(self, content):
        try:
            dividendDict = json.loads(
                content)["chart"]["result"][0]["events"]["dividends"]
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            return pd.DataFrame(dividendDict).rename(
                {'amount': self._parName1, 'date': self._parName2}, axis='index')


class FetchMyDividendRecordCommand(APICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._myStockDF = kwargs.get('myStockDF')
        self._parName1 = ''.join([self._company, '-amount'])
        self._parName2 = ''.join([self._company, '-date'])
        self._parNameCollection = [self._parName1, self._parName2]
        self._firstBidTime = getBidDate(self._myStockDF)
        self._firstBidUnixTimestamp = getUnixTimeStamp([[2014, 1, 3]])
        self._fileName = pathConfig.cache+'myDividendRecord.csv'
        self._url = f'https://query1.finance.yahoo.com/v8/finance/chart/{self._company}?period1={self._firstBidUnixTimestamp}&period2=9999999999&interval=1d&includePrePost=false&events=div%2Csplit'
        self._urlName = 'Yahoo Finance Chart API'

    def APICallback(self, content):
        try:
            dividendDict = json.loads(
                content)["chart"]["result"][0]["events"]["dividends"]
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            return pd.DataFrame(dividendDict).rename(
                {'amount': self._parName1, 'date': self._parName2}, axis='index')
