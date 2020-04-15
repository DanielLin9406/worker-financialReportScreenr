import io
import json
import os
import time
import pandas as pd
import Config.pathConfig as pathConfig
from dotenv import load_dotenv
from API.APICommand import APICommand
load_dotenv()
alphaVantageAPIKey = os.getenv("ALPHA_API_KEY")


class FetchStockPriceCommand(APICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName1 = ''.join([self._company, '-amount'])
        self._parName2 = ''.join([self._company, '-date'])
        self._parNameCollection = [self._parName1, self._parName2]
        self._fileName = pathConfig.cache+'stockPrice.csv'
        self._url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={self._company}&apikey={alphaVantageAPIKey}&datatype=csv'
        self._urlName = 'Alphavantage'

    def APICallback(self, content):
        try:
            df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            time.sleep(20)
            return df.T.loc[['timestamp', 'close']].rename(
                {'close': self._parName1, 'timestamp': self._parName2}, axis='index')
