

class Context:
    def __init__(self, **kwargs):
        self._strategy = None
        self._listName = kwargs.get('listName')
        self._company = kwargs.get('company')
        self._parsTable = kwargs.get('parsTable')

    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def doScoreAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            listName=self._listName,
            company=self._company,
            parsTable=self._parsTable
        )
        return self._strategy.doAlgorithm

    def doSummarizedAlgorithm(self):
        self._strategy.doAlgorithm = dict(
            company=self._company,
        )
        return self._strategy.doAlgorithm
