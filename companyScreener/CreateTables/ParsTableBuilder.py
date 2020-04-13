import pandas as pd
from .Builder import Builder, Director
from .builderProduct.Dividend import Dividend
from .builderProduct.Profit import Profit
from .builderProduct.Growth import Growth
from .builderProduct.Safety import Safety
from .builderProduct.Industry import Industry


class IndustryInfoBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Industry(**kwargs)

    def constructPars(self):
        self._cell.setSector()
        self._cell.setIndustry()
        self._cell.setMarketCapitalization()


class DividendBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Dividend(**kwargs)

    def constructPars(self):
        self._cell.setDividend()
        self._cell.setDividendGrowth()
        self._cell.setTotalDivideds()
        self._cell.setAvgDividendin5years()
        self._cell.setMaxDividendin5Years()
        self._cell.setMinDividendin5Years()
        self._cell.setDividendGrowthin3Years()
        self._cell.setDividendGrowthin5Years()
        self._cell.setDividendYield()
        self._cell.setPayoutRatio()


class ProfitBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Profit(**kwargs)

    def constructPars(self):
        self._cell.setROE()
        self._cell.setAvgROEin4years()
        self._cell.setMaxROEin4Years()
        self._cell.setMinROEin4Years()
        self._cell.setYearPercentageOfHighROE()
        self._cell.setROA()
        self._cell.setROS()
        self._cell.setOperatingMarin()
        self._cell.setOperatingCashFlow()
        self._cell.setNetIncome()
        self._cell.setEPS()


class GrowthBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Growth(**kwargs)

    def constructPars(self):
        self._cell.setROTA()
        self._cell.setGrossMargin()
        self._cell.setAssetTurnoverRatio()
        self._cell.setReinvestmentRate()
        self._cell.setResearch()
        self._cell.setOperatingIncomeGrowth()
        self._cell.setOperatingIncomeAccelerateGrowth()
        self._cell.setYearPercentageOfOperatingIncomeGrowth()
        self._cell.setRevenueGrowth()
        self._cell.setYearPercentageOfRevenueGrowth()
        self._cell.setEPSGrowth()
        self._cell.setEPSGrowth3YearAvg()


class SafetyBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Safety(**kwargs)

    def constructPars(self):
        self._cell.setTotalAssests()
        self._cell.setTotalLiabilities()
        self._cell.setLongTermDebt()
        self._cell.setFreeCashFlow()
        self._cell.setYearPercentageOfPositiveFreeCashFlow()
        self._cell.setCurrentRatio()
        self._cell.setQuickRatio()
        self._cell.setDebtEquityRatio()
        self._cell.setDebtCapitalRatio()
        self._cell.setDebtAssetsRatio()
        self._cell.setTotalDividendsFCFRatio()
        self._cell.setSharesCapital()


def ParsTable(**kwargs):
    result = []
    director = Director()

    director.builder = IndustryInfoBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    director.builder = DividendBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    director.builder = ProfitBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    director.builder = GrowthBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    director.builder = SafetyBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    return pd.concat(result, axis=1)

# def createIndustryInfo(combinedDF, parsDFList, company):
#     industryInstance = Industry(**dict(
#         combinedDF=combinedDF,
#         parsDFList=parsDFList,
#         company=company
#     ))
#     industryInstance.setSector()
#     industryInstance.setIndustry()
#     industryInstance.setMarketCapitalization()
#     return industryInstance.getOutput()


# def createDividendDF(combinedDF, parsDFList, company):
#     dividendInstance = Dividend(**dict(
#         combinedDF=combinedDF,
#         parsDFList=parsDFList,
#         company=company
#     ))
#     dividendInstance.setDividend()
#     dividendInstance.setDividendGrowth()
#     dividendInstance.setTotalDivideds()
#     dividendInstance.setAvgDividendin5years()
#     dividendInstance.setMaxDividendin5Years()
#     dividendInstance.setMinDividendin5Years()
#     dividendInstance.setDividendGrowthin3Years()
#     dividendInstance.setDividendGrowthin5Years()
#     dividendInstance.setDividendYield()
#     dividendInstance.setPayoutRatio()
#     return dividendInstance.getOutput()


# def createProfitDF(combinedDF, parsDFList, company):
#     profitInstance = Profit(**dict(
#         combinedDF=combinedDF,
#         parsDFList=parsDFList,
#         company=company
#     ))
#     profitInstance.setROE()
#     profitInstance.setAvgROEin4years()
#     profitInstance.setMaxROEin4Years()
#     profitInstance.setMinROEin4Years()
#     profitInstance.setYearPercentageOfHighROE()
#     profitInstance.setROA()
#     profitInstance.setROS()
#     profitInstance.setOperatingMarin()
#     profitInstance.setOperatingCashFlow()
#     profitInstance.setNetIncome()
#     profitInstance.setEPS()
#     return profitInstance.getOutput()


# def createGrowthDF(combinedDF, parsDFList, company):
#     growthInstance = Growth(**dict(
#         combinedDF=combinedDF,
#         parsDFList=parsDFList,
#         company=company
#     ))
#     growthInstance.setROTA()
#     growthInstance.setGrossMargin()
#     growthInstance.setAssetTurnoverRatio()
#     growthInstance.setReinvestmentRate()
#     growthInstance.setResearch()
#     growthInstance.setOperatingIncomeGrowth()
#     growthInstance.setOperatingIncomeAccelerateGrowth()
#     growthInstance.setYearPercentageOfOperatingIncomeGrowth()
#     growthInstance.setRevenueGrowth()
#     growthInstance.setYearPercentageOfRevenueGrowth()
#     growthInstance.setEPSGrowth()
#     growthInstance.setEPSGrowth3YearAvg()
#     return growthInstance.getOutput()


# def createSafetyDF(combinedDF, parsDFList, company):
#     safetyInstance = Safety(**dict(
#         combinedDF=combinedDF,
#         parsDFList=parsDFList,
#         company=company
#     ))
#     safetyInstance.setTotalAssests()
#     safetyInstance.setTotalLiabilities()
#     safetyInstance.setLongTermDebt()
#     safetyInstance.setFreeCashFlow()
#     safetyInstance.setYearPercentageOfPositiveFreeCashFlow()
#     safetyInstance.setCurrentRatio()
#     safetyInstance.setQuickRatio()
#     safetyInstance.setDebtEquityRatio()
#     safetyInstance.setDebtCapitalRatio()
#     safetyInstance.setDebtAssetsRatio()
#     safetyInstance.setTotalDividendsFCFRatio()
#     safetyInstance.setSharesCapital()
#     return safetyInstance.getOutput()


# def createParsTable(combinedDF, parsDFList, company):
#     return pd.concat([
#         createIndustryInfo(combinedDF, parsDFList, company),
#         createDividendDF(combinedDF, parsDFList, company),
#         createProfitDF(combinedDF, parsDFList, company),
#         createGrowthDF(combinedDF, parsDFList, company),
#         createSafetyDF(combinedDF, parsDFList, company)], axis=1)
