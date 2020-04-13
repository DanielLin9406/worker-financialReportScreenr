from abc import ABC, abstractmethod, abstractproperty
from .ParsTableBuilder import ParsTable
from .PriceTableBuilder import PriceTable
from .ScoreTableStrategy import ScoreTable
from .BuyDecisionTableStrategy import BuyDecisionTable
from .SellDecisionTableStrategy import SellDecisionTable


class TablesFactory:
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def createParsTable(self):
        return ParsTable(**self.kwargs)

    def createPriceTable(self):
        return PriceTable(**self.kwargs)


class AnalyzeTablesFactory:
    def createScoreTable(self, **kwargs):
        return ScoreTable(**kwargs)

    def createBuyDecisionTable(self, **kwargs):
        return BuyDecisionTable(**kwargs)

    def createSellDecisionTable(self, **kwargs):
        return SellDecisionTable(**kwargs)
