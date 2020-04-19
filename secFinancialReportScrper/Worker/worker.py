import io
import time
import pandas as pd
import requests
import copy
from pathlib import Path
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


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
        return response


def isCacheExist(key, fileName):
    if (key):
        return Path(fileName).is_file() and isColumnExist(key, fileName)
    else:
        return Path(fileName).is_file()


def isColumnExist(key, fileName):
    key = copy.deepcopy(key)
    fileIndexList = readFile(fileName).index
    if (type(key) == list):
        while(len(key) > 0):
            return key.pop() in fileIndexList
        return False
    else:
        return key in fileIndexList


def readFile(fileName):
    try:
        df = pd.read_csv(fileName, index_col=0,
                         error_bad_lines=False, warn_bad_lines=False)
        df.index = df.index.map(str)
        return df
    except Exception as x:
        print('Read CSV failed :(', x.__class__.__name__)
        return pd.DataFrame()


def getDF(key, fileName):
    df = readFile(fileName)
    if type(key) == list:
        if all(ele in df.index for ele in key):
            return df.loc[key]
        else:
            return df
    else:
        if (key in df.index):
            return df.loc[key]
        else:
            return df


def saveDFtoFile(df, key, fileName):
    df.to_csv(fileName, mode='a')
    if (key):
        return df.loc[key]
    else:
        return df


def readAPIContent(content):
    return io.StringIO(content.decode('utf-8'))
