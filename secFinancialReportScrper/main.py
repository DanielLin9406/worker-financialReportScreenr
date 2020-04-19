from mainFactory import createInputFactory
from API.APICommand import CommandInvoker
from API.SECCommand import FetchCompany2CIKMappingCommand, FetchEDGARIndexFileNameCommand
from API.GoogleSheetCommand import FetchCompanyAndIndustryInfoCommand


def mainProcess(company):
    inputFactory = createInputFactory(
        **dict(
            company=company,
        )
    )
    reportUrls = inputFactory.loadTemplate1()


def getEDGARIndexFiles():
    invoker = CommandInvoker()
    invoker.setCommand(FetchEDGARIndexFileNameCommand())
    return invoker.getDataFromAPI()


def getCompanyInfoList():
    invoker = CommandInvoker()
    invoker.setCommand(FetchCompanyAndIndustryInfoCommand())
    return invoker.getDataFromAPI()


def main():
    EDGARIndexDF = getEDGARIndexFiles()
    mainProcess('msft')
    # for company in getCompanyInfoList():
    # mainProcess(company)


if __name__ == '__main__':
    main()
