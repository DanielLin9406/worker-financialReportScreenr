from abc import ABC, abstractmethod, abstractproperty
from .ParsTableBuilder import ParsTable
from .PriceTableBuilder import PriceTable
from .Context import Context
from .ScoreTableStrategy import ScoreTable
from .BuyDecisionTableStrategy import BuyDecisionTable
from .SellDecisionTableStrategy import SellDecisionTable

context = Context()


class TablesFactory:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def createParsTable(self):
        return ParsTable(**self.kwargs)

    def createPriceTable(self):
        return PriceTable(**self.kwargs)


class AnalyzeTablesFactory:
    def __init__(self):
        self._context = context

    def createScoreTable(self, **kwargs):
        return ScoreTable(**kwargs, **dict(context=self._context))

    def createBuyDecisionTable(self, **kwargs):
        return BuyDecisionTable(**kwargs, **dict(context=self._context))

    def createSellDecisionTable(self, **kwargs):
        return SellDecisionTable(**kwargs, **dict(context=self._context))
