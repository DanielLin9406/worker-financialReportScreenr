from Worker.logger import dumpArgs
import os
import quandl
from pathlib import Path
import Config.pathConfig as pathConfig
from Worker.worker import isColumnExist, getDF, fetchUrlWithLog, requestRetrySession, saveDFtoFile
from dotenv import load_dotenv
load_dotenv()
quandl.ApiConfig.api_key = os.getenv("QUANDL_API_KEY")


def getTreasuriesYield(fileName=pathConfig.cache+'treasuriesYield.csv'):
    parName = ''.join(['treasuriesYield'])
    if Path(fileName).is_file() and isColumnExist(parName, fileName):
        # if file exist read from file
        return getDF(parName, fileName)
    else:
        # if file not exist call api and save in file
        df = quandl.get("ML/AAAEY").sort_index(ascending=False)
        treasuriesYieldDF = df.iloc[:2].T.loc[['BAMLC0A1CAAAEY']].rename(
            {'BAMLC0A1CAAAEY': parName}, axis='index')
        return saveDFtoFile(treasuriesYieldDF, parName, fileName)
