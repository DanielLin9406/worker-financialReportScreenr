import Config.pathConfig as pathConfig
import re
import gspread
import pandas as pd
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         'https://www.googleapis.com/auth/drive.file',
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


class GoogleAPICommand:
    def openSheet(self):
        return client.open(self._sheetName).worksheet(self._sheetTabName)

    def getDataFromGoogleSheet(self):
        ws = openSheet(self._sheetName, self._sheetTabName)
        return ws.get_all_values()


class FetchCompanyAndIndustryInfoCommand(APICommand, GoogleAPICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName = ''.join([self._company])
        self._fileName = pathConfig.cache+'company.csv'
        self._sheetName = "Stock"
        self._sheetTabName = 'Company'

    def getCompanySheet(self, data):
        df = pd.DataFrame(data[1:], columns=data[0])
        return df.set_index('Name')

    def fetchDataViaAPI(self, url, urlName):
        return self.getDataFromGoogleSheet(self.sheetName, self.sheetTabName)

    def APICallback(self, content):
        return getCompanySheet(content)


class FetchMyStockCommand(APICommand, GoogleAPICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName = ''.join([self._company])
        self._fileName = pathConfig.cache+'myStock.csv'
        self._sheetName = "Stock"
        self._sheetTabName = 'MyStock'

    def getName(self, bidArr):
        result = []
        i = 1
        for ele in bidArr:
            result.append(ele+'-'+str(i))
            i = i + 1
        return result

    def getMyStockSheet(self, sheetTabName, data):
        bidArr = [ele for ele in data[4] if re.match("Bid/BidDate-*", ele)]
        columnList = []
        columnList.extend(['Company', 'Own Shares'])
        columnList.extend(getName(bidArr))
        df = pd.DataFrame(data[6:, 1:], columns=columnList)
        return df.set_index('Company')

    def fetchDataViaAPI(self, url, urlName):
        return self.getDataFromGoogleSheet(self.sheetName, self.sheetTabName)

    def APICallback(self, content):
        df = getMyStockSheet(self.sheetTabName, np.array(content))
        return df
