from abc import ABC, abstractmethod, abstractproperty
from Input.ReadLocalFile import ReadLocalFile
from API.GoogleSheet import getCompanyAndIndustryInfo, getMyStock
from API.Quandl import getTreasuriesYield
from API.AlphaVantage import getStockPrice
from API.YahooFinance import getRevenueEstimate, getDividendRecord, getMyDividendRecord
from API.APIMediator import APIMediator, FetchYahooAPINotify, FetchAlphavantageNotify, FetchQuandlNotify, FetchGoogleSheetNotify


class ReadDataType:
    def readCSVOperation(self):
        self.readSQLOperation()
        print("Read CSV")

    def readSQLOperation(self):
        print("Read SQL")

    def readNoSQLOperation(self):
        print("Read NoSQL")


class DataFetcherCollection(ReadDataType):
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self._localFileInstance = self._kwargs.get('localFileInstance')
        self._notifyYahooAPI = FetchYahooAPINotify()
        self._notifyAlphavantage = FetchAlphavantageNotify()
        self._notifyQuandl = FetchQuandlNotify()
        self._notifyGoogleSheet = FetchGoogleSheetNotify()
        self._company = self._kwargs.get('company')

    def loadTemplate1(self):
        """
        @param: DataFrame
        @return: {
          combinedDF: DataFrame,
          yahoo: DataFrame
          ...
        }
        """
        return dict(
            combinedDF=self.readCombinedDF(),
            companyInfoDF=self.readCompanyInfo(),
            priceDF=self.readStockPrice(),
            revenueEstimateDF=self.readRevenueEstimate(),
            treasuriesYieldDF=self.readTreasuriesYield(),
            dividendRecordDF=self.readDividendRecord(),
            myStockDF=self.readMyStock(),
            myDividendRecorDF=self.readMyDividendRecord(),
        )

    def loadTemplate2(self):
        self.readMongoOperation()
        self.readGoogle()
        self.readQuandl()

    def readCombinedDF(self):
        return self._localFileInstance.getData()

    def readStockPrice(self):
        # notifyAlphavantage.getStockPrice()
        return getStockPrice(self._company)

    def readMyDividendRecord(self):
        myStockDF = self.readMyStock()
        # notifyYahooAPI.getMyDividendRecord()
        return getMyDividendRecord(myStockDF, self._company)

    def readDividendRecord(self):
        # notifyYahooAPI.getDividendRecord()
        return getDividendRecord(self._company)

    def readTreasuriesYield(self):
        # notifyQuandl.getTreasuriesYield()
        return getTreasuriesYield()

    def readRevenueEstimate(self):
        # notifyYahooAPI.getRevenueEstimate()
        return getRevenueEstimate(self._company)

    def readMyStock(self):
        # notifyGoogleSheet.getMyStock()
        return getMyStock(self._company)

    def readCompanyInfo(self):
        # notifyGoogleSheet.getCompanyInfo()
        return getCompanyAndIndustryInfo(self._company)


class InputTemplate1(DataFetcherCollection):
    def __init__(self, **kwargs):
        self.localFileInstance = ReadLocalFile(**kwargs)
        self.APIMediatorInstance = APIMediator(**kwargs)
        super().__init__(**kwargs, **dict(
            localFileInstance=self.localFileInstance,
        ))

    def isInputExist(self):
        instance = self.localFileInstance
        return instance.isInputExist()
