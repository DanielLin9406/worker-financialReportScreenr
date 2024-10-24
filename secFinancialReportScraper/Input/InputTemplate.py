from API.APIMediator import APIMediator, APINotify


class DataFetcherCollection:
    def __init__(self, **kwargs):
        self._kwargs = kwargs
        self.initAPIMediator()

    def initAPIMediator(self):
        self._APINotifyInstance = APINotify()
        self._mediatorInstance = APIMediator(**self._kwargs, **dict(
            apiNotifyInstance=self._APINotifyInstance,
        ))

    def loadTemplate1(self):
        # 1. Fetch CIK
        self._cik = self.getCIK()

        # 2. Fetch EDGARIndexFileName
        self._mediatorInstance.data = dict(
            cik=self._cik
        )
        self._EDGARIndexFileName = self.getEDGARIndexFileName()

        # 3. Fetch reports urls
        self._mediatorInstance.data = dict(
            EDGARIndexFileName=self._EDGARIndexFileName
        )
        self._reportUrls = self.getReportUrls()

        # 4. Fetch all financial reports
        FinancialStatementsList = [
            'INCOME STATEMENTS',
            'COMPREHENSIVE INCOME STATEMENTS',
            'BALANCE SHEETS',
            'BALANCE SHEETS (Parenthetical)',
            'CASH FLOWS STATEMENTS',
            "STOCKHOLDERS' EQUITY STATEMENTS"
        ]
        financialReportDFdict = {}
        for sheetName in FinancialStatementsList:
            self._mediatorInstance.data = dict(
                sheetName=sheetName,
                sheetUrl=self._reportUrls.get(sheetName),
            )
            financialReportDFdict[sheetName.replace(
                ' ', '_')] = self.getFinancialStatements()

        return dict(
            cik=self._cik,
            EDGARIndexFileName=self._EDGARIndexFileName,
            reportUrlsDF=self._reportUrls,
            financialReportDFDict=financialReportDFdict
        )

    def getCIK(self):
        return str(self.readCompany2CIKMapping().get('CIK'))

    def getEDGARIndexFileName(self):
        return self.readEDGARIndexFiles().get('File Name')

    def getReportUrls(self):
        return self.readReportUrls()

    def getFinancialStatements(self):
        return self.readFinancialStatements()

    # def getSECReport(self):
    #     return self.readSECReport()

    def readCompany2CIKMapping(self):
        return self._APINotifyInstance.getCompany2CIKMapping()

    def readEDGARIndexFiles(self):
        return self._APINotifyInstance.getEDGARIndexFileName()

    def readReportUrls(self):
        return self._APINotifyInstance.getReportUrls()

    def readFinancialStatements(self):
        return self._APINotifyInstance.getFinancialStatements()

    # def readSECReport(self):
    #     return self._APINotifyInstance.getSECReport()


class InputTemplate(DataFetcherCollection):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
