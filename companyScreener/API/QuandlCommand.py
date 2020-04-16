import os
import quandl
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv
from API.APICommand import APICommand
from Worker.worker import fetchUrlWithLog
import Config.pathConfig as pathConfig
load_dotenv()
quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")


class FetchTreasuriesYieldCommand(APICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName = ''.join(['treasuriesYield'])
        self._parNameCollection = self._parName
        self._fileName = pathConfig.cache+'treasuriesYield.csv'
        self._url = 'ML/AAAEY'
        self._urlName = 'Yahoo Finance QuoteSummary API'

    def fetchDataViaAPI(self, url, urlName):
        return quandl.get(url).sort_index(ascending=False)

    def APICallback(self, content):
        try:
            treasuriesYieldDF = content.iloc[:2].T.loc[['BAMLC0A1CAAAEY']].rename(
                {'BAMLC0A1CAAAEY': self._parName}, axis='index')
        except Exception as x:
            print('JSON Parse failed when getting dividend :(',
                  x.__class__.__name__)
            return pd.DataFrame()
        else:
            return treasuriesYieldDF
