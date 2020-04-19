from abc import ABC, abstractmethod, abstractproperty
from Input.ReadLocalFile import ReadLocalFile
from API.APIMediator import APIMediator, APINotify


class DataFetcherCollection:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    def initReadLocalFile(self):
        self._localFileInstance = ReadLocalFile(**self._kwargs)

    def initAPIMediator(self):
        self._APINotifyInstance = APINotify()
        APIMediator(**self._kwargs, **dict(
            apiNotifyInstance=self._APINotifyInstance,
        ))

    def loadTemplate1(self):
        return dict(
            reportsDF=self.readLocalFileDF(),
            companyInfoDF=self.readCompanyInfo(),
            priceDF=self.readStockPrice(),
            revenueEstimateDF=self.readRevenueEstimate(),
            treasuriesYieldDF=self.readTreasuriesYield(),
            dividendRecordDF=self.readDividendRecord(),
            myStockDF=self.readMyStock(),
            myDividendRecorDF=self.readMyDividendRecord(),
        )

    def loadTemplate2(self):
        return dict(
            companyInfoDF=self.readCompanyInfo(),
        )

    def readLocalFileDF(self):
        self._localFileInstance = ReadLocalFile(**self._kwargs)
        return self._localFileInstance.getData()

    def readStockPrice(self):
        # print('new', self._APINotifyInstance.getStockPrice())
        # print('old', getStockPrice(self._company))
        return self._APINotifyInstance.getStockPrice()

    def readMyDividendRecord(self):
        # myStockDF = self.readMyStock()
        # print('new', self._APINotifyInstance.getDividendRecord())
        # print('old', getDividendRecord(self._company))
        return self._APINotifyInstance.getDividendRecord()

    def readDividendRecord(self):
        # print('new', self._APINotifyInstance.getDividendRecord())
        # print('old', getDividendRecord(self._company))
        return self._APINotifyInstance.getDividendRecord()

    def readTreasuriesYield(self):
        # print('new', self._APINotifyInstance.getTreasuriesYield())
        # print('old', getTreasuriesYield(self._company))
        return self._APINotifyInstance.getTreasuriesYield()

    def readRevenueEstimate(self):
        # print('new', self._APINotifyInstance.getRevenueEstimate())
        # print('old', getRevenueEstimate(self._company))
        return self._APINotifyInstance.getRevenueEstimate()

    def readMyStock(self):
        # print('new', self._APINotifyInstance.getMyStock())
        # print('old', getMyStock(self._company))
        return self._APINotifyInstance.getMyStock()

    def readCompanyInfo(self):
        # print('new', self._APINotifyInstance.getCompanyInfo())
        # print('old', getCompanyAndIndustryInfo(self._company))
        return self._APINotifyInstance.getCompanyInfo()


class InputTemplate1(DataFetcherCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        super().initReadLocalFile()
        super().initAPIMediator()

    def setMainData(self):
        self._mainData = 'LocalFile'

    def isMainDataExist(self):
        return self._localFileInstance.isFileExist()


# class InputTemplate2(DataFetcherCollection):
#     def __init__(self, **kwargs):
#         self._kwargs = kwargs
#         self.initAPIMediator()
#         super().__init__(**kwargs, **dict(
#             apiNotifyInstance=self._APINotifyInstance
#         ))

#     def initAPIMediator(self):
#         self._APINotifyInstance = APINotify()
#         APIMediator(**self._kwargs, **dict(
#             apiNotifyInstance=self._APINotifyInstance,
#         ))
