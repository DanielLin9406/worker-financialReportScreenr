import pandas as pd
from .Builder import Builder, Director
from .builderProduct.Price import Price
from .builderProduct.Value import Value
from .builderProduct.DDM import DDM
from .builderProduct.DDM2 import DDM2
from .builderProduct.DDMH import DDMH
from .builderProduct.DCF import DCF
from .builderProduct.FCFF import FCFF
from .builderProduct.FCFE import FCFE
from .builderProduct.EBT import EBT
from .builderProduct.Graham import Graham
from .builderProduct.AvgPrice import AvgPrice


class PriceBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Price(**kwargs)

    def constructPars(self):
        self._cell.setStockPrice()


class DDMBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = DDM(**kwargs)

    def constructPars(self):
        self._cell.setHighGrowthRate()
        self._cell.setPerpetualGrowthRate()
        self._cell.setDiscountRate()
        self._cell.setStockPriceDDM()


class DDM2Builder(Builder):
    def __init__(self, **kwargs):
        self._cell = DDM2(**kwargs)

    def constructPars(self):
        self._cell.setHighGrowthPeriod()
        self._cell.setHighGrowthRate()
        self._cell.setPerpetualGrowthRate()
        self._cell.setDiscountRate()
        self._cell.setDividendAfterNYears()
        self._cell.setStockPrice()


class DDMHBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = DDMH(**kwargs)

    def constructPars(self):
        self._cell.setHighGrowthPeriod()
        self._cell.setHighGrowthRate()
        self._cell.setPerpetualGrowthRate()
        self._cell.setDiscountRate()
        self._cell.setDividendAfterNYears()
        self._cell.setStockPrice()


class FCFEBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = FCFE(**kwargs)

    def constructPars(self):
        self._cell.setHighGrowthRate()
        self._cell.setPerpetualGrowthRate()
        self._cell.setDiscountRate()
        self._cell.setStockPrice()


class DCFBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = DCF(**kwargs)

    def constructPars(self):
        self._cell.setRevenueEstimate()
        self._cell.setAvgGrowthRate()
        self._cell.setPerpetualGrowthRate()
        self._cell.setDiscountRate()
        self._cell.setAvgNetIncomeMargin()
        self._cell.setAvgFCFNetIncomeRatio()
        self._cell.setStockPrice()


class GrahamBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Graham(**kwargs)

    def constructPars(self):
        self._cell.setGrowthRate()
        self._cell.setTreasuriesYield()
        self._cell.setStockPrice()


class EBTBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = EBT(**kwargs)

    def constructPars(self):
        self._cell.setStockPrice()


class AvgPriceBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = AvgPrice(**kwargs)

    def constructPars(self):
        self._cell.setAVGPriceofValueInvesement()
        self._cell.setAVGPriceofGrowthInvesement()
        self._cell.setDiscountPremiumOfDDM()
        self._cell.setDiscountPremiumOfDDM2()
        self._cell.setDiscountPremiumOfDDMH()
        self._cell.setDiscountPremiumOfFCFE()
        self._cell.setDiscountPremiumOfDCF()
        self._cell.setDiscountPremiumOfGraham()
        self._cell.setDiscountPremiumOfEBT()


class ValueBuilder(Builder):
    def __init__(self, **kwargs):
        self._cell = Value(**kwargs)

    def constructPars(self):
        self._cell.setPRRatio()
        self._cell.setPSRatio()
        self._cell.setPERatio()
        self._cell.setPEGRatio()
        self._cell.setPBRatio()


def PriceTable(**kwargs):
    result = []
    instanceDict = dict(
        valueInvesement=dict(),
        growthInvesement=dict(),
    )
    director = Director()

    director.builder = PriceBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    director.builder = DDMBuilder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'DDM': director.builder})
    result.append(director.getOutput())

    director.builder = DDM2Builder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'DDM2': director.builder})
    result.append(director.getOutput())

    director.builder = DDMHBuilder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'DDMH': director.builder})
    result.append(director.getOutput())

    director.builder = FCFEBuilder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'FCFE': director.builder})
    instanceDict['growthInvesement'].update({'FCFE': director.builder})
    result.append(director.getOutput())

    director.builder = DCFBuilder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'DCF': director.builder})
    instanceDict['growthInvesement'].update({'DCF': director.builder})
    result.append(director.getOutput())

    director.builder = GrahamBuilder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'Graham': director.builder})
    result.append(director.getOutput())

    director.builder = EBTBuilder(**kwargs)
    director.constructPars()
    instanceDict['valueInvesement'].update({'EBT': director.builder})
    instanceDict['growthInvesement'].update({'EBT': director.builder})
    result.append(director.getOutput())

    director.builder = AvgPriceBuilder(**kwargs, **instanceDict)
    director.constructPars()
    result.append(director.getOutput())

    director.builder = ValueBuilder(**kwargs)
    director.constructPars()
    result.append(director.getOutput())

    return pd.concat(result, axis=1)


# def createPriceDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company):
#     priceInstance = Price(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     priceInstance.setStockPrice()
#     return priceInstance.getOutput()


# def createDDMDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     ddmInstance = DDM(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     ddmInstance.setHighGrowthRate()
#     ddmInstance.setPerpetualGrowthRate()
#     ddmInstance.setDiscountRate()
#     ddmInstance.setStockPriceDDM()
#     instanceDict['valueInvesement'].update({'DDM': ddmInstance})
#     return ddmInstance.getOutput()


# def createDDM2DF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     ddm2Instance = DDM2(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     ddm2Instance.setHighGrowthPeriod()
#     ddm2Instance.setHighGrowthRate()
#     ddm2Instance.setPerpetualGrowthRate()
#     ddm2Instance.setDiscountRate()
#     ddm2Instance.setDividendAfterNYears()
#     ddm2Instance.setStockPrice()
#     instanceDict['valueInvesement'].update({'DDM2': ddm2Instance})
#     return ddm2Instance.getOutput()


# def createDDMHDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     ddmHInstance = DDMH(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     ddmHInstance.setHighGrowthPeriod()
#     ddmHInstance.setHighGrowthRate()
#     ddmHInstance.setPerpetualGrowthRate()
#     ddmHInstance.setDiscountRate()
#     ddmHInstance.setDividendAfterNYears()
#     ddmHInstance.setStockPrice()
#     instanceDict['valueInvesement'].update({'DDMH': ddmHInstance})
#     return ddmHInstance.getOutput()


# # def createFCFFDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company):
# #     fcffHInstance = FCFF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company)
# #     # fcffHInstance.setStockPriceFCFF()


# def createFCFEDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     fcfeInstance = FCFE(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     fcfeInstance.setHighGrowthRate()
#     fcfeInstance.setPerpetualGrowthRate()
#     fcfeInstance.setDiscountRate()
#     fcfeInstance.setStockPrice()
#     instanceDict['valueInvesement'].update({'FCFE': fcfeInstance})
#     instanceDict['growthInvesement'].update({'FCFE': fcfeInstance})
#     return fcfeInstance.getOutput()


# def createDCFDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     dcfInstance = DCF(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     dcfInstance.setRevenueEstimate()
#     dcfInstance.setAvgGrowthRate()
#     dcfInstance.setPerpetualGrowthRate()
#     dcfInstance.setDiscountRate()
#     dcfInstance.setAvgNetIncomeMargin()
#     dcfInstance.setAvgFCFNetIncomeRatio()
#     dcfInstance.setStockPrice()
#     instanceDict['valueInvesement'].update({'DCF': dcfInstance})
#     instanceDict['growthInvesement'].update({'DCF': dcfInstance})
#     return dcfInstance.getOutput()


# def createGrahamDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     grahamInstance = Graham(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     grahamInstance.setGrowthRate()
#     grahamInstance.setTreasuriesYield()
#     grahamInstance.setStockPrice()
#     instanceDict['valueInvesement'].update({'Graham': grahamInstance})
#     return grahamInstance.getOutput()


# def createEBTDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     ebtInstance = EBT(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     ebtInstance.setStockPrice()
#     instanceDict['valueInvesement'].update({'EBT': ebtInstance})
#     instanceDict['growthInvesement'].update({'EBT': ebtInstance})
#     return ebtInstance.getOutput()


# def createAvgPriceDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company, instanceDict):
#     avgPriceInstance = AvgPrice(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ), **dict(
#         valueInvesement=instanceDict['valueInvesement'],
#         growthInvesement=instanceDict['growthInvesement'],
#     ))
#     avgPriceInstance.setAVGPriceofValueInvesement()
#     avgPriceInstance.setAVGPriceofGrowthInvesement()
#     avgPriceInstance.setDiscountPremiumOfDDM()
#     avgPriceInstance.setDiscountPremiumOfDDM2()
#     avgPriceInstance.setDiscountPremiumOfDDMH()
#     avgPriceInstance.setDiscountPremiumOfFCFE()
#     avgPriceInstance.setDiscountPremiumOfDCF()
#     avgPriceInstance.setDiscountPremiumOfGraham()
#     avgPriceInstance.setDiscountPremiumOfEBT()
#     return avgPriceInstance.getOutput()


# def createValueDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company):
#     valueInstance = Value(**dict(
#         reportsDF=reportsDF,
#         priceDF=priceDF,
#         treasuriesYieldDF=treasuriesYieldDF,
#         revenueEstimateDF=revenueEstimateDF,
#         company=company
#     ))
#     valueInstance.setPRRatio()
#     valueInstance.setPSRatio()
#     valueInstance.setPERatio()
#     valueInstance.setPEGRatio()
#     valueInstance.setPBRatio()
#     return valueInstance.getOutput()


# def createPriceTable(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company):
#     instanceDict = dict(
#         valueInvesement=dict(),
#         growthInvesement=dict(),
#     )

#     return pd.concat([createPriceDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF, company),
#                       createDDMDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                   company, instanceDict),
#                       createDDM2DF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                    company, instanceDict),
#                       createDDMHDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                    company, instanceDict),
#                       createFCFEDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                    company, instanceDict),
#                       createDCFDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                   company, instanceDict),
#                       createGrahamDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                      company, instanceDict),
#                       createEBTDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                   company, instanceDict),
#                       createAvgPriceDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                        company, instanceDict),
#                       createValueDF(reportsDF, priceDF, treasuriesYieldDF, revenueEstimateDF,
#                                     company), ], axis=1)
