import gspread
import json
import pandas as pd
import numpy as np

from pathlib import Path
from worker import readSeriesFromFile
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
         "https://www.googleapis.com/auth/spreadsheets",
         'https://www.googleapis.com/auth/drive.file',
         "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)


def openSheet(stock, sheetTabName):
    return client.open(stock).worksheet(sheetTabName)


# def getTitleListFromDF(df, sheetName, company):
#     return df.columns.astype(str).values.tolist()


def getValueListFromDF(df, sheetName, company):
    if 'Pars' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
    elif 'Price' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()
    elif 'Analysis' in sheetName:
        return np.nan_to_num(df.astype(float, errors="ignore").values).tolist()


def getRangeOfList(sheetName, idNum):
    if 'Pars' in sheetName:
        return ''.join(['C', str(idNum), ':BV', str(idNum)])
    elif 'Analysis' in sheetName:
        return ''.join(['C', str(idNum), ':BL', str(idNum)])
    elif 'Price' in sheetName:
        return ''.join(['C', str(idNum), ':BO', str(idNum)])


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
    # print(result)
    return result


def upload2Sheet(df, sheetTabName, company, idNum):
    sheetName = "Stock"
    ws = openSheet(sheetName, sheetTabName)
    ws.format(getFormatedOfCell(sheetTabName, idNum)["range"],
              getFormatedOfCell(sheetTabName, idNum)["formated"])
    ws.batch_update(getUploadData(df, sheetTabName, company, idNum))


def readSheetFromGoogleSheet(sheetTabName):
    sheetName = "Stock"
    ws = openSheet(sheetName, sheetTabName)
    data = ws.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df.set_index('Name')


def readSheetFromCSV(csvName, company):
    return pd.read_csv(csvName, index_col=0)


def getCompany(csvName, company):
    df = readSheetFromCSV(csvName, company)
    return df.loc[company]


def saveAndGetCompany(df, fileName, company):
    df.to_csv(fileName)
    return df.loc[company]


def getCompanyAndIndustryInfo(sheetTabName, company):
    fileName = 'company.csv'
    if Path(fileName).is_file():
        return getCompany(fileName, company)
    else:
        df = readSheetFromGoogleSheet(sheetTabName)
        return saveAndGetCompany(df, fileName, company)


def createCompanyAndIndustryInfo(sheetTabName, company):
    series = getCompanyAndIndustryInfo(sheetTabName, company)
    df = pd.DataFrame()
    df.at[company, series.index[0]] = series.iloc[0]
    df.at[company, series.index[1]] = series.iloc[1]
    return df
