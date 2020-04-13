import gspread
import json
import pandas as pd
import numpy as np
import re
import Config.pathConfig as pathConfig
from pathlib import Path
# from worker import readSeriesFromFile
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
    # print(result)
    return result


def upload2Sheet(df, sheetTabName, company, idNum):
    sheetName = "Stock"
    ws = openSheet(sheetName, sheetTabName)
    ws.format(getFormatedOfCell(sheetTabName, idNum)["range"],
              getFormatedOfCell(sheetTabName, idNum)["formated"])
    ws.batch_update(getUploadData(df, sheetTabName, company, idNum))


def readCompanySheet(sheetTabName, data):
    df = pd.DataFrame(data[1:], columns=data[0])
    return df.set_index('Name')


def getName(bidArr):
    result = []
    i = 1
    for ele in bidArr:
        result.append(ele+'-'+str(i))
        i = i + 1
    return result


def readMyStockSheet(sheetTabName, data):
    bidArr = [ele for ele in data[4] if re.match("Bid/BidDate-*", ele)]
    columnList = []
    columnList.extend(['Company', 'Own Shares'])
    columnList.extend(getName(bidArr))
    df = pd.DataFrame(data[6:, 1:], columns=columnList)
    return df.set_index('Company')


def readDataFromGoogleSheet(sheetName, sheetTabName):
    ws = openSheet(sheetName, sheetTabName)
    return ws.get_all_values()


def readSheetFromCSV(csvName):
    return pd.read_csv(csvName, index_col=0)


def getCompany(fileName, company):
    df = readSheetFromCSV(fileName)
    if company in df.axes[0].values:
        return df.loc[company]
    else:
        return pd.DataFrame()


def saveAndGetCompany(df, fileName, company):
    df.to_csv(fileName)
    return getCompany(fileName, company)


def getCompanyAndIndustryInfo(sheetTabName, company):
    fileName = pathConfig.cache+'company.csv'
    sheetName = "Stock"
    data = readDataFromGoogleSheet(sheetName, sheetTabName)

    if Path(fileName).is_file():
        return getCompany(fileName, company)
    else:
        df = readCompanySheet(data)
        return saveAndGetCompany(df, fileName, company)


def getMyStock(sheetTabName, company):
    fileName = pathConfig.cache+'myStock.csv'
    sheetName = "Stock"
    data = readDataFromGoogleSheet(sheetName, sheetTabName)

    if Path(fileName).is_file():
        return getCompany(fileName, company)
    else:
        df = readMyStockSheet(sheetTabName, np.array(data))
        return saveAndGetCompany(df, fileName, company)
