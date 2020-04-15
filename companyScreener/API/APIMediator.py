from pathlib import Path
from APICommand import CommandInvoker
from YahooAPICommand import FetchRevenueEstimateCommand, FetchDividendRecordCommand, FetchMyDividendRecordCommand
from QuandlCommand import FetchTreasuriesYieldCommand
from AlphaVantageCommand import FetchStockPriceCommand
from API.GoogleSheetCommand import FetchCompanyAndIndustryInfoCommand, FetchMyStockCommand


class AbstructAPIMediator(ABC):
    def notify(self, sender: object, event: str) -> None:
        pass


class APIMediator(AbstructAPIMediator):
    def __init__(self, **kwargs):
        self._company = kwargs.get('company')

    def notify(self, sender: object, event: str) -> None:
        data = dict(company=self._company)
        invoker = CommandInvoker()
        if event == 'revenueEstimate':
            invoker.setCommand(FetchRevenueEstimateCommand(**data))
        elif event == 'dividendRecord':
            invoker.setCommand(FetchDividendRecordCommand(**data))
        elif event == 'myDividendRecord':
            invoker.setCommand(FetchMyDividendRecordCommand(**data))
        elif event == 'treasuriesYield':
            invoker.setCommand(FetchTreasuriesYieldCommand(**data))
        elif event == 'stockPrice':
            invoker.setCommand(FetchStockPriceCommand(**data))
        elif event == 'companyInfo':
            invoker.setCommand(FetchCompanyAndIndustryInfoCommand(**data))
        elif event == 'myStock':
            invoker.setCommand(FetchMyStockCommand(**data))

        return invoker.getDataFromAPI()


class APINotifyBase:
    def __init__(self, mediator: Mediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> Mediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: Mediator) -> None:
        self._mediator = mediator


class FetchYahooAPINotify(APINotifyBase):
    def getRevenueEstimate(self) -> None:
        return self.mediator.notify(self, "revenueEstimate")

    def getDividendRecord(self) -> None:
        return self.mediator.notify(self, "dividendRecord")

    def getMyDividendRecord(self) -> None:
        return self.mediator.notify(self, "myDividendRecord")


class FetchQuandlNotify(APINotifyBase):
    def getTreasuriesYield(self) -> None:
        return self.mediator.notify(self, "treasuriesYield")


class FetchAlphavantageNotify(APINotifyBase):
    def getStockPrice(self) -> None:
        return self.mediator.notify(self, "stockPrice")


class FetchGoogleSheetNotify(APINotifyBase):
    def getMyStock(self) -> None:
        return self.mediator.notify(self, "myStock")

    def getCompanyInfo(self) -> None:
        return self.mediator.notify(self, "companyInfo")


# notifyYahooAPI = FetchYahooAPINotify()
# notifyAlphavantage = FetchAlphavantageNotify()
# notifyQuandl = FetchQuandlNotify()
# notifyGoogleSheet = FetchGoogleSheetNotify()

# notifyYahooAPI.getRevenueEstimate()
# notifyYahooAPI.getDividendRecord()
# notifyYahooAPI.getMyDividendRecord()
# notifyAlphavantage.getStockPrice()
# notifyQuandl.getTreasuriesYield()
# notifyGoogleSheet.getMyStock()
# notifyGoogleSheet.getCompanyInfo()
