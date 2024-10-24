from abc import ABC, abstractmethod, abstractproperty
from API.SECCommand import FetchEDGARIndexFileNameCommand, FetchCompany2CIKMappingCommand, FetchReportUrlCommand, FetchFinancialStatementsCommand
from API.APICommand import CommandInvoker


class AbstructAPIMediator(ABC):
    def notify(self, sender: object, event: str) -> None:
        pass


class APIMediator(AbstructAPIMediator):
    def __init__(self, **kwargs):
        self._queryCondition = dict()
        self._company = kwargs.get('company')
        self._apiNotify = kwargs.get('apiNotifyInstance')
        self._apiNotify.mediator = self

    def notify(self, sender: object, event: str) -> None:
        data = dict(company=self._company)
        invoker = CommandInvoker()
        if event == 'Company2CIKMapping':
            invoker.setCommand(FetchCompany2CIKMappingCommand(**data))
        elif event == 'EDGARIndexFileName':
            invoker.setCommand(
                FetchEDGARIndexFileNameCommand(**data, **self._queryCondition))
        elif event == 'ReportUrls':
            invoker.setCommand(
                FetchReportUrlCommand(**data, **self._queryCondition))
        elif event == 'FinancialStatements':
            invoker.setCommand(
                FetchFinancialStatementsCommand(**data, **self._queryCondition))
        # elif event == 'FullReport':
        #     invoker.setCommand(
        #         FetchFullReportCommand(**data, **self._queryCondition))
        return invoker.getDataFromAPI()

    @property
    def data(self):
        return self._queryCondition

    @data.setter
    def data(self, value):
        self._queryCondition = value


class APINotifyBase:
    def __init__(self, mediator: AbstructAPIMediator = None) -> None:
        self._mediator = mediator

    @property
    def mediator(self) -> AbstructAPIMediator:
        return self._mediator

    @mediator.setter
    def mediator(self, mediator: AbstructAPIMediator) -> None:
        self._mediator = mediator


class APINotify(APINotifyBase):
    def getCompany2CIKMapping(self):
        return self.mediator.notify(self, "Company2CIKMapping")

    def getEDGARIndexFileName(self):
        return self.mediator.notify(self, "EDGARIndexFileName")

    def getReportUrls(self):
        return self.mediator.notify(self, "ReportUrls")

    def getFinancialStatements(self):
        return self.mediator.notify(self, "FinancialStatements")

    # def getFullReport(self):
    #     return self.mediator.notify(self, "FullReport")
