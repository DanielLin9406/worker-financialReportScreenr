import time
import pandas as pd
import numpy as np
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


def isColumnExist(company, fileName):
    if (type(company) == list):
        while(len(company) > 0):
            return company.pop() in readSeriesFromFile(fileName).index
        return False
    else:
        return company in readSeriesFromFile(fileName).index


def readSeriesFromFile(fileName):
    try:
        return pd.read_csv(fileName, index_col=0, error_bad_lines=False, warn_bad_lines=False,)
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
