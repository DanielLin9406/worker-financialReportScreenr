import io
import os
import time
import pandas as pd
import Config.pathConfig as pathConfig
from pathlib import Path
from dotenv import load_dotenv
from Worker.worker import isColumnExist, getDF, fetchUrlWithLog, requestRetrySession, saveDFtoFile
load_dotenv()

alphaVantageAPIKey = os.getenv("ALPHA_API_KEY")

# TODO
# Output Format


def getStockPrice(company, fileName=pathConfig.cache+'stockPrice.csv'):
    parName1 = ''.join([company, '-amount'])
    parName2 = ''.join([company, '-date'])
    if Path(fileName).is_file() and isColumnExist([parName1, parName2], fileName):
        # if file exist read from file
        return getDF([parName1, parName2], fileName)
    else:
        # if file not exist call api and save in file
        url = ''.join(['https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=',
                       company, '&apikey=', alphaVantageAPIKey, '&datatype=csv'])
        urlName = 'Alphavantage'
        content = fetchUrlWithLog(url, requestRetrySession, urlName)
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        time.sleep(20)
        # DF = pd.DataFrame(dividendDict).rename(
        #     {'amount': parName1, 'date': parName2}, axis='index')
        # priceDF = df.T.loc[['timestamp', 'close']].rename(
        #     {'timestamp': 'timestamp', 'close': company}, axis='index')
        priceDF = df.T.loc[['timestamp', 'close']].rename(
            {'close': parName1, 'timestamp': parName2}, axis='index')
        return saveDFtoFile(priceDF, company, fileName)
