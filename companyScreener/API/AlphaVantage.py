import io
import os
import time
import pandas as pd
import Config.pathConfig as pathConfig
from pathlib import Path
from dotenv import load_dotenv
from Worker.worker import isColumnExist, getSeriesInDF, fetchUrlWithLog, requestRetrySession, saveDFtoFile
load_dotenv()

alphaVantageAPIKey = os.getenv("ALPHA_API_KEY")


def getStockPrice(company, fileName=pathConfig.cache+'stockPrice.csv'):
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
