import gspread
import pandas as pd
import numpy as np
import re
import Config.pathConfig as pathConfig
from pathlib import Path
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         'https://www.googleapis.com/auth/drive.file',
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


def openSheet(stock, sheetTabName):
    return client.open(stock).worksheet(sheetTabName)


class OutPutToGoogleSheet:
    def __init__(self, **kwargs):
        self._ws = None
        self._sheetName = "Stock"
        self._df = kwargs.get('df')
        self._sheetTabName = kwargs.get('sheetTabName')
        self._idNum = kwargs.get('idNum')
        self._company = kwargs.get('company')
        self.buildConnection()

    def buildConnection(self):
        self._ws = openSheet(self._sheetName, self._sheetTabName)

    def getRangeOfList(self):
        sheetTabName = self._sheetTabName
        idNum = self._idNum
        if 'Pars' in sheetTabName:
            return ''.join(['C', str(idNum), ':BV', str(idNum)])
        elif 'Analysis' in sheetTabName:
            return ''.join(['C', str(idNum), ':BL', str(idNum)])
        elif 'Price' in sheetTabName:
            return ''.join(['C', str(idNum), ':BO', str(idNum)])
        elif 'BuyDecision' in sheetTabName:
            return ''.join(['C', str(idNum), ':G', str(idNum)])
        elif 'SellDecision' in sheetTabName:
            return ''.join(['C', str(idNum), ':O', str(idNum)])

    def getValueListFromDF(self):
        df = self._df
        sheetTabName = self._sheetTabName
        idNum = self._idNum
        if 'Pars' in sheetTabName:
            return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
        elif 'Price' in sheetTabName:
            return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
        elif 'Analysis' in sheetTabName:
            return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
        elif 'BuyDecision' in sheetTabName:
            return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
        elif 'SellDecision' in sheetTabName:
            return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()

    def getFormatedSetting(self):
        return {
            "horizontalAlignment": "CENTER"
        }

    def getRangeSetting(self):
        return self.getRangeOfList()

    def setCellFormat(self):
        self._ws.format(self.getRangeSetting(), self.getFormatedSetting())

    def getUploadData(self):
        return [
            {
                'range': ''.join(['B', str(self._idNum)]),
                'values': [[self._company]]
            }, {
                'range': self.getRangeSetting(),
                'values': self.getValueListFromDF()
            }
        ]

    def uploadData(self):
        self._ws.batch_update(self.getUploadData())


# def openSheet(stock, sheetTabName):
#     return client.open(stock).worksheet(sheetTabName)


# def getValueListFromDF(df, sheetTabName, company):
#     if 'Pars' in sheetTabName:
#         return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
#     elif 'Price' in sheetTabName:
#         return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
#     elif 'Analysis' in sheetTabName:
#         return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
#     elif 'BuyDecision' in sheetTabName:
#         return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
#     elif 'SellDecision' in sheetTabName:
#         return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()


# def getRangeOfList(sheetTabName, idNum):
#     if 'Pars' in sheetTabName:
#         return ''.join(['C', str(idNum), ':BV', str(idNum)])
#     elif 'Analysis' in sheetTabName:
#         return ''.join(['C', str(idNum), ':BL', str(idNum)])
#     elif 'Price' in sheetTabName:
#         return ''.join(['C', str(idNum), ':BO', str(idNum)])
#     elif 'BuyDecision' in sheetTabName:
#         return ''.join(['C', str(idNum), ':G', str(idNum)])
#     elif 'SellDecision' in sheetTabName:
#         return ''.join(['C', str(idNum), ':O', str(idNum)])


# def getFormatedOfCell(sheetTabName, idNum):
#     if 'Pars' in sheetTabName:
#         data = {
#             "range": getRangeOfList(sheetTabName, idNum),
#             "formated": {
#                 "horizontalAlignment": "CENTER"
#             }
#         }
#         return data
#     elif 'Analysis' in sheetTabName:
#         data = {
#             "range": getRangeOfList(sheetTabName, idNum),
#             "formated": {
#                 "horizontalAlignment": "CENTER"
#             }
#         }
#         return data
#     elif 'Price' in sheetTabName:
#         data = {
#             "range": getRangeOfList(sheetTabName, idNum),
#             "formated": {
#                 "horizontalAlignment": "CENTER"
#             }
#         }
#         return data
#     elif 'BuyDecision' in sheetTabName:
#         data = {
#             "range": getRangeOfList(sheetTabName, idNum),
#             "formated": {
#                 "horizontalAlignment": "CENTER"
#             }
#         }
#         return data
#     elif 'SellDecision' in sheetTabName:
#         data = {
#             "range": getRangeOfList(sheetTabName, idNum),
#             "formated": {
#                 "horizontalAlignment": "CENTER"
#             }
#         }
#         return data


# def getUploadData(df, sheetTabName, company, idNum):
#     sheetRange = getRangeOfList(sheetTabName, idNum)
#     dataList = getValueListFromDF(df, sheetTabName, company)
#     result = [
#         {
#             'range': ''.join(['B', str(idNum)]),
#             'values': [[company]]
#         }, {
#             'range': sheetRange,
#             'values': dataList
#         }]
#     return result


# def upload2Sheet(df, sheetTabName, company, idNum):
#     sheetName = "Stock"
#     ws = openSheet(sheetName, sheetTabName)
#     ws.format(getFormatedOfCell(sheetTabName, idNum)["range"],
#               getFormatedOfCell(sheetTabName, idNum)["formated"])
#     print('new', OutPutToGoogleSheet(
#         **dict(
#           df=df,
#           sheetTabName=sheetTabName,
#           company=company,
#           idNum=idNum
#           )).getUploadData())
#     print('old', getUploadData(df, sheetTabName, company, idNum))
#     ws.batch_update(getUploadData(df, sheetTabName, company, idNum))
