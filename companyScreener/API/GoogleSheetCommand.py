from oauth2client.service_account import ServiceAccountCredentials
import re
import gspread
import pandas as pd
import numpy as np
import Config.pathConfig as pathConfig
from API.APICommand import APICommand

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
        ws = self.openSheet()
        return ws.get_all_values()


class FetchCompanyAndIndustryInfoCommand(APICommand, GoogleAPICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName = ''.join([self._company])
        self._parNameCollection = self._parName
        self._fileName = pathConfig.cache+'company.csv'
        self._sheetName = "Stock"
        self._sheetTabName = 'Company'
        self._url = self._sheetName
        self._urlName = self._sheetTabName

    def getCompanySheet(self, data):
        df = pd.DataFrame(data[1:], columns=data[0])
        return df.set_index('Name')

    def fetchDataViaAPI(self, url, urlName):
        return self.getDataFromGoogleSheet()

    def APICallback(self, content):
        return self.getCompanySheet(content)


class FetchMyStockCommand(APICommand, GoogleAPICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._parName = ''.join([self._company])
        self._parNameCollection = self._parName
        self._fileName = pathConfig.cache+'myStock.csv'
        self._sheetName = "Stock"
        self._sheetTabName = 'MyStock'
        self._url = self._sheetName
        self._urlName = self._sheetTabName

    def getName(self, bidArr):
        result = []
        i = 1
        for ele in bidArr:
            result.append(ele+'-'+str(i))
            i = i + 1
        return result

    def getMyStock(self, data):
        bidArr = [ele for ele in data[4] if re.match("Bid/BidDate-*", ele)]
        columnList = []
        columnList.extend(['Company', 'Own Shares'])
        columnList.extend(self.getName(bidArr))
        df = pd.DataFrame(data[6:, 1:], columns=columnList)
        return df.set_index('Company')

    def fetchDataViaAPI(self, url, urlName):
        return self.getDataFromGoogleSheet()

    def APICallback(self, content):
        df = self.getMyStock(np.array(content))
        return df
