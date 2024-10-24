import io
import time
import pandas as pd
import re
import numpy as np
from bs4 import BeautifulSoup
import Config.pathConfig as pathConfig
from Worker.worker import readAPIContent
from API.APICommand import APICommand


class SECAPICommand:
    def getUrl(self):
        return ''.join(self._urlList)

    def parseXML(self, content):
        return BeautifulSoup(content, 'lxml')

    def parseHTML(self, content):
        return BeautifulSoup(content, 'html')

    def turnContent2Text(self, content):
        return readAPIContent(content).getvalue()


class FetchCompany2CIKMappingCommand(APICommand, SECAPICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self.initFetchUrlPars()
        self.initCachePars()
        self.initReturnDataPars()

    def initFetchUrlPars(self):
        self._baseUrl = r"https://www.sec.gov/include/ticker.txt"
        self._urlName = 'CIK Ticker Fetcher'
        self._urlList = [self._baseUrl]
        self._url = self.getUrl()

    def initCachePars(self):
        self._fileName = pathConfig.cache+'CIKTicker.csv'
        self._readCSVseparator = '\t'

    def initReturnDataPars(self):
        self._parName = ''.join(
            [self._company if self._company is not None else 'fullData'])
        self._parNameCollection = self._parName

    def APICallback(self, response):
        content = response.content
        text = self.turnContent2Text(content)
        return pd.read_csv(io.StringIO(
            text), sep=self._readCSVseparator, index_col=0, names=['Company Code', 'CIK'])


class FetchEDGARIndexFileNameCommand(APICommand, SECAPICommand):
    def __init__(self, **kwargs) -> None:
        self._cik = kwargs.get('cik')
        self.initFetchUrlPars()
        self.initCachePars()
        self.initCallbackPars()
        self.initReturnDataPars()

    def initFetchUrlPars(self):
        self._baseUrl = r"https://www.sec.gov/Archives/edgar/daily-index"
        self._urlName = 'SEC Scraper'
        self._season = '/2019/QTR3'
        self._fileType = "/master"
        self._date = '.20190801.idx'
        self._urlList = [self._baseUrl,
                         self._season, self._fileType, self._date]
        self._url = self.getUrl()

    def initCachePars(self):
        self._fileName = pathConfig.cache+'EDGARIndex.csv'
        self._readCSVseparator = '|'

    def initCallbackPars(self):
        self._formType = '10-K'
        self._txtSeparator = 'ftp://ftp.sec.gov/edgar/'

    def initReturnDataPars(self):
        self._parName = ''.join(
            [self._cik if self._cik is not None else 'fullData'])
        self._parNameCollection = self._parName

    def purefyText(self, text):
        separator = self._txtSeparator
        return text[text.find(separator) + len(separator)+1:]

    def APICallback(self, response):
        content = response.content
        text = self.turnContent2Text(content)
        purefyedText = self.purefyText(text)
        df = pd.read_csv(io.StringIO(purefyedText),
                         sep=self._readCSVseparator, index_col=0).dropna()
        return df[df['Form Type'] == self._formType]


class FetchReportUrlCommand(APICommand, SECAPICommand):
    def __init__(self, **kwargs) -> None:
        self._company = kwargs.get('company')
        self._EDGARIndexFileName = kwargs.get('EDGARIndexFileName')
        self.initFetchUrlPars()
        self.initCachePars()
        self.initReturnDataPars()

    def initFetchUrlPars(self):
        self._baseUrl = r"https://www.sec.gov/Archives/"
        self._urlName = 'Fetch Filling Summary'
        self._fileUrl = self._EDGARIndexFileName.replace(
            '-', '').replace('.txt', '')
        self._fileType = '/FilingSummary.xml'
        self._urlList = [self._baseUrl, self._fileUrl, self._fileType]
        self._url = self.getUrl()
        print(self._url)

    def initCachePars(self):
        self._fileName = pathConfig.cache+'ReportUrls.csv'

    def initReturnDataPars(self):
        self._parName = ''.join(
            [self._company if self._company is not None else 'fullData'])
        self._parNameCollection = self._parName

    def dumpUsefulReport(self, soup):
        reports = soup.find('myreports').find_all('report')[:-1]
        df = pd.DataFrame()
        for report in reports:
            df.at[self._company,
                  report.shortname.text] = f"{self._baseUrl}{self._fileUrl}/{report.htmlfilename.text}"
        return df

    def APICallback(self, response):
        content = response.content
        soup = self.parseXML(content)
        df = self.dumpUsefulReport(soup)
        return df


class FetchFinancialStatementsCommand(APICommand, SECAPICommand):
    def __init__(self, **kwargs) -> None:
        self._sheetUrl = kwargs.get('sheetUrl')
        self._sheetName = kwargs.get('sheetName')
        self._company = kwargs.get('company')
        self.initFetchUrlPars()
        self.initCachePars()
        self.initReturnDataPars()

    def initFetchUrlPars(self):
        self._urlName = f'{self._sheetUrl}'
        self._url = self._sheetUrl

    def initCachePars(self):
        self._fileName = pathConfig.cache + \
            f'{self._company}-{self._sheetName}.csv'

    def initReturnDataPars(self):
        self._thisYear = '2019'
        self._parName = ''.join(['fullData'])
        self._parNameCollection = self._parName

    def dumpUsefulReport(self, soup):
        statementData = {}
        statementData['headers'] = []
        statementData['sections'] = []
        statementData['data'] = []
        for index, row in enumerate(soup.table.find_all('tr', class_=lambda x: x and not 'outerFootnote' in x)):
            # first let's get all the elements
            cols = row.find_all('td')

            # if it's a regular row and not a section or a table header
            if (len(row.find_all('th')) == 0 and len(row.find_all('strong')) == 0 and len(row.find_all('table')) == 0):
                regRow = [ele.text.strip() for ele in cols]
                statementData['data'].append(regRow)

            # if it's a regular row and a section but not a table header
            elif (len(row.find_all('th')) == 0 and len(row.find_all('strong')) != 0):
                secRow = cols[0].text.strip()
                statementData['sections'].append(secRow)
            # finally if it's not any of those it must be a header
            elif (len(row.find_all('th')) != 0):
                headRow = [ele.text.strip() for ele in row.find_all('th')]
                statementData['sections'].append(headRow)
            else:
                print('Encountered an error.')
        return statementData

    def APICallback(self, response):
        content = response.content
        soup = self.parseXML(content)
        result = self.dumpUsefulReport(soup)
        array = np.array(result['data'])
        df = pd.DataFrame(array[:, 0:2], columns=[
                          'name', self._company+'-'+self._thisYear])
        df = df.set_index('name')
        return df.T


# class FetchFullReportCommand(APICommand, SECAPICommand):
#     def __init__(self, **kwargs) -> None:
#         self._EDGARIndexFileName = kwargs.get('EDGARIndexFileName')
#         self.initFetchUrlPars()
#         self.initCachePars()
#         self.initReturnDataPars()

#     def initFetchUrlPars(self):
#         self._baseUrl = r"https://www.sec.gov/Archives/"
#         self._urlName = 'Full Report'
#         self._fileUrl = self._EDGARIndexFileName
#         self._urlList = [self._baseUrl, self._fileUrl]
#         self._url = self.getUrl()

#     def initCachePars(self):
#         self._fileName = pathConfig.cache+'FullReport.csv'
#         self._readCSVseparator = ','

#     def initReturnDataPars(self):
#         self._parName = ''.join(['fullData'])
#         self._parNameCollection = self._parName

#     def APICallback(self, response):
#         content = response.content
#         print(content)
