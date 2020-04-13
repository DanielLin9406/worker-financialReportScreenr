
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Context(metaclass=Singleton):
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    @property
    def listName(self):
        return self._listName

    @listName.setter
    def listName(self, listName):
        self._listName = listName

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, company):
        self._company = company

    @property
    def parsTable(self):
        return self._parsTable

    @parsTable.setter
    def parsTable(self, parsTable):
        self._parsTable = parsTable

    @property
    def priceTable(self):
        return self._priceTable

    @priceTable.setter
    def priceTable(self, priceTable):
        self._priceTable = priceTable

    @property
    def scoreTable(self):
        return self._scoreTable

    @scoreTable.setter
    def scoreTable(self, scoreTable):
        self._scoreTable = scoreTable

    @property
    def myStockDF(self):
        return self._myStockDF

    @myStockDF.setter
    def myStockDF(self, myStockDF):
        self._myStockDF = myStockDF

    @property
    def myDividendRecorDF(self):
        return self._myDividendRecorDF

    @myDividendRecorDF.setter
    def myDividendRecorDF(self, myDividendRecorDF):
        self._myDividendRecorDF = myDividendRecorDF

    @property
    def summarizedScoreList(self):
        return self._summarizedScoreList

    @summarizedScoreList.setter
    def summarizedScoreList(self, summarizedScoreList):
        self._summarizedScoreList = summarizedScoreList

    @property
    def countScoreDFList(self):
        return self._countScoreDFList

    @countScoreDFList.setter
    def countScoreDFList(self, countScoreDFList):
        self._countScoreDFList = countScoreDFList

    def doScoreAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            listName=self._listName,
            company=self._company,
            parsTable=self._parsTable,
        )
        return self._strategy.doAlgorithm

    def doCountScoreAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            listName=self._listName,
            company=self._company,
            countScoreDFList=self._countScoreDFList
        )
        return self._strategy.doAlgorithm

    def doSummarizedAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            company=self._company,
            summarizedScoreList=self._summarizedScoreList
        )
        return self._strategy.doAlgorithm

    def doBuyDecisionAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            company=self._company,
            priceTable=self._priceTable,
            scoreTable=self._scoreTable
        )
        return self._strategy.doAlgorithm

    def doSellDecisionAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            company=self._company,
            priceTable=self._priceTable,
            scoreTable=self._scoreTable,
            myStockDF=self._myStockDF,
            myDividendRecorDF=self._myDividendRecorDF
        )
        return self._strategy.doAlgorithm
