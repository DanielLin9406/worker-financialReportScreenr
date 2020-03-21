import gspread
import json
import numpy as np
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         'https://www.googleapis.com/auth/drive.file',
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


def sheet(sheetName):
    return client.open("Stock").worksheet(sheetName)


def getTitleListFromDF(df, sheetName, company):
    # df.columns = [''] * len(df.columns)
    return df.columns.astype(str).values.tolist()


def getValueListFromDF(df, sheetName, company):
    return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()


def getRangeOfList(sheetName, idNum):
    if 'Pars' in sheetName:
        return ''.join(['F', str(idNum), ':', 'BF', str(idNum)])
    elif 'Analysis' in sheetName:
        return ''.join(['C', str(idNum), ':', 'AW', str(idNum)])
    elif 'Price' in sheetName:
        return ''.join(['C', str(idNum), ':', 'AW', str(idNum)])


def getFormatedOfCell(sheetName, idNum):
    if 'Pars' in sheetName:
        data = {
            "range": "".join(["F", str(idNum), ":BF", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER",
                "numberFormat": {
                    "type": "NUMBER",
                    "pattern": "#,#0.##"
                }
            }
        }
        return data
    elif 'Analysis' in sheetName:
        data = {
            "range": "".join(["C", str(idNum), ":AW", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data
    elif 'Price' in sheetName:
        data = {
            "range": "".join(["C", str(idNum), ":AM", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data
    else:
        data = {
            "range": "".join(["C", str(idNum), ":AW", str(idNum)]),
            "formated": {
                "horizontalAlignment": "CENTER"
            }
        }
        return data


def getUploadPars(df, sheetName, company, idNum):
    sheetRange = getRangeOfList(sheetName, idNum)
    dataList = getValueListFromDF(df, sheetName, company)
    result = [
        {
            'range': ''.join(['B', str(idNum)]),
            'values': [[company]]
        }, {
            'range': sheetRange,
            'values': dataList
        }]
    return result


def upload2Sheet(df, sheetName, company, idNum):
    cellSetting = getFormatedOfCell(sheetName, idNum)
    ws = sheet(sheetName)
    ws.format(cellSetting["range"], cellSetting["formated"])
    ws.batch_update(getUploadPars(df, sheetName, company, idNum))
