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


def getValueListFromDF(df, sheetName, company):
    if 'Pars' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
    elif 'Price' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
    elif 'Analysis' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
    elif 'BuyDecision' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
    elif 'SellDecision' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()


def getRangeOfList(sheetName, idNum):
    if 'Pars' in sheetName:
        return ''.join(['C', str(idNum), ':BV', str(idNum)])
    elif 'Analysis' in sheetName:
        return ''.join(['C', str(idNum), ':BL', str(idNum)])
    elif 'Price' in sheetName:
        return ''.join(['C', str(idNum), ':BO', str(idNum)])
    elif 'BuyDecision' in sheetName:
        return ''.join(['C', str(idNum), ':G', str(idNum)])
    elif 'SellDecision' in sheetName:
        return ''.join(['C', str(idNum), ':O', str(idNum)])


def getFormatedOfCell(sheetName, idNum):
    if 'Pars' in sheetName:
        data = {
            "range": "".join(["E", str(idNum), ":BV", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data
    elif 'Analysis' in sheetName:
        data = {
            "range": "".join(["C", str(idNum), ":BL", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data
    elif 'Price' in sheetName:
        data = {
            "range": "".join(["C", str(idNum), ":BO", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data
    elif 'BuyDecision' in sheetName:
        data = {
            "range": "".join(["C", str(idNum), ":G", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data
    elif 'SellDecision' in sheetName:
        data = {
            "range": "".join(["C", str(idNum), ":O", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data


def getUploadData(df, sheetTabName, company, idNum):
    sheetRange = getRangeOfList(sheetTabName, idNum)
    dataList = getValueListFromDF(df, sheetTabName, company)
    result = [
        {
            'range': ''.join(['B', str(idNum)]),
            'values': [[company]]
        }, {
            'range': sheetRange,
            'values': dataList
        }]
    return result


def upload2Sheet(df, sheetTabName, company, idNum):
    sheetName = "Stock"
    ws = openSheet(sheetName, sheetTabName)
    ws.format(getFormatedOfCell(sheetTabName, idNum)["range"],
              getFormatedOfCell(sheetTabName, idNum)["formated"])
    ws.batch_update(getUploadData(df, sheetTabName, company, idNum))
