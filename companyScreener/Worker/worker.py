from Worker.logger import dumpArgs
import time
import io
import copy
import pandas as pd
import datetime
import numpy as np
import json
import requests
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


def isCacheExist(key, fileName):
    return Path(fileName).is_file() and isColumnExist(key, fileName)


def isColumnExist(key, fileName):
    key = copy.deepcopy(key)
    if (type(key) == list):
        while(len(key) > 0):
            return key.pop() in readFile(fileName).index
        return False
    else:
        return key in readFile(fileName).index


def readAPIContent(content):
    return pd.read_csv(io.StringIO(content.decode('utf-8')))


def readJSONContent(content):
    return json.loads(content)


def readFile(fileName):
    try:
        return pd.read_csv(fileName, index_col=0, error_bad_lines=False, warn_bad_lines=False,)
    except Exception as x:
        print('Read CSV failed :(', x.__class__.__name__)
        return pd.DataFrame()


def getDF(key, fileName):
    df = readFile(fileName)
    if type(key) == list:
        if all(ele in df.axes[0].values for ele in key):
            # print(fileName, df.loc[key])
            return df.loc[key]
        else:
            return pd.DataFrame()
    else:
        if (key in df.axes[0].values):
            return df.loc[key]
        else:
            return pd.DataFrame()


def saveDFtoFile(df, key, fileName):
    df.to_csv(fileName, mode='a')
    return df.loc[key]


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
