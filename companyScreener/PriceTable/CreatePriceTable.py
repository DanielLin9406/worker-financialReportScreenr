import pandas as pd
from PriceTable.dataClass.Price import Price
from PriceTable.dataClass.Value import Value
from PriceTable.dataClass.DDM import DDM
from PriceTable.dataClass.DDM2 import DDM2
from PriceTable.dataClass.DDMH import DDMH
from PriceTable.dataClass.DCF import DCF
from PriceTable.dataClass.FCFF import FCFF
from PriceTable.dataClass.FCFE import FCFE
from PriceTable.dataClass.EBT import EBT
from PriceTable.dataClass.Graham import Graham
from PriceTable.dataClass.AvgPrice import AvgPrice


def createPriceDF(combinedDF, priceDFList, company):
    priceInstance = Price(combinedDF, priceDFList, company)
    priceInstance.setStockPrice()
    return priceInstance.getOutput()
    # priceInstance.setDividend()


def createDDMDF(combinedDF, priceDFList, company, instanceDict):
    ddmInstance = DDM(combinedDF, priceDFList, company)
    ddmInstance.setHighGrowthRate()
    ddmInstance.setPerpetualGrowthRate()
    ddmInstance.setDiscountRate()
    ddmInstance.setStockPriceDDM()
    instanceDict['valueInvesement'].append(ddmInstance)
    instanceDict['valueInvesement2'].update({'DDM': ddmInstance})
    return ddmInstance.getOutput()


def createDDM2DF(combinedDF, priceDFList, company, instanceDict):
    ddm2Instance = DDM2(combinedDF, priceDFList, company)
    ddm2Instance.setHighGrowthPeriod()
    ddm2Instance.setHighGrowthRate()
    ddm2Instance.setPerpetualGrowthRate()
    ddm2Instance.setDiscountRate()
    ddm2Instance.setDividendAfterNYears()
    ddm2Instance.setStockPrice()
    instanceDict['valueInvesement'].append(ddm2Instance)
    instanceDict['valueInvesement2'].update({'DDM2': ddm2Instance})
    return ddm2Instance.getOutput()


def createDDMHDF(combinedDF, priceDFList, company, instanceDict):
    ddmHInstance = DDMH(combinedDF, priceDFList, company)
    ddmHInstance.setHighGrowthPeriod()
    ddmHInstance.setHighGrowthRate()
    ddmHInstance.setPerpetualGrowthRate()
    ddmHInstance.setDiscountRate()
    ddmHInstance.setDividendAfterNYears()
    ddmHInstance.setStockPrice()
    instanceDict['valueInvesement'].append(ddmHInstance)
    instanceDict['valueInvesement2'].update({'DDMH': ddmHInstance})
    return ddmHInstance.getOutput()


# def createFCFFDF(combinedDF, priceDFList, company):
#     fcffHInstance = FCFF(combinedDF, priceDFList, company)
#     # fcffHInstance.setStockPriceFCFF()


def createFCFEDF(combinedDF, priceDFList, company, instanceDict):
    fcfeInstance = FCFE(combinedDF, priceDFList, company)
    fcfeInstance.setHighGrowthRate()
    fcfeInstance.setPerpetualGrowthRate()
    fcfeInstance.setDiscountRate()
    fcfeInstance.setStockPrice()
    instanceDict['valueInvesement'].append(fcfeInstance)
    instanceDict['growthInvesement'].append(fcfeInstance)
    instanceDict['valueInvesement2'].update({'FCFE': fcfeInstance})
    instanceDict['growthInvesement2'].update({'FCFE': fcfeInstance})
    return fcfeInstance.getOutput()


def createDCFDF(combinedDF, priceDFList, company, instanceDict):
    dcfInstance = DCF(combinedDF, priceDFList, company)
    dcfInstance.setRevenueEstimate()
    dcfInstance.setAvgGrowthRate()
    dcfInstance.setPerpetualGrowthRate()
    dcfInstance.setDiscountRate()
    dcfInstance.setAvgNetIncomeMargin()
    dcfInstance.setAvgFCFNetIncomeRatio()
    dcfInstance.setStockPrice()
    instanceDict['valueInvesement'].append(dcfInstance)
    instanceDict['growthInvesement'].append(dcfInstance)
    instanceDict['valueInvesement2'].update({'DCF': dcfInstance})
    instanceDict['growthInvesement2'].update({'DCF': dcfInstance})
    return dcfInstance.getOutput()


def createGrahamDF(combinedDF, priceDFList, company, instanceDict):
    grahamInstance = Graham(combinedDF, priceDFList, company)
    grahamInstance.setGrowthRate()
    grahamInstance.setTreasuriesYield()
    grahamInstance.setStockPrice()
    instanceDict['valueInvesement'].append(grahamInstance)
    instanceDict['valueInvesement2'].update({'Graham': grahamInstance})
    return grahamInstance.getOutput()


def createEBTDF(combinedDF, priceDFList, company, instanceDict):
    ebtInstance = EBT(combinedDF, priceDFList, company)
    ebtInstance.setStockPrice()
    instanceDict['valueInvesement'].append(ebtInstance)
    instanceDict['growthInvesement'].append(ebtInstance)
    instanceDict['valueInvesement2'].update({'EBT': ebtInstance})
    instanceDict['growthInvesement2'].update({'EBT': ebtInstance})
    return ebtInstance.getOutput()


def createAvgPriceDF(combinedDF, priceDFList, company, instanceDict):
    avgPriceInstance = AvgPrice(
        combinedDF, priceDFList, instanceDict, company)
    avgPriceInstance.setAVGPriceofValueInvesement()
    avgPriceInstance.setAVGPriceofGrowthInvesement()
    avgPriceInstance.setDiscountPremiumOfDDM()
    avgPriceInstance.setDiscountPremiumOfDDM2()
    avgPriceInstance.setDiscountPremiumOfDDMH()
    avgPriceInstance.setDiscountPremiumOfFCFE()
    avgPriceInstance.setDiscountPremiumOfDCF()
    avgPriceInstance.setDiscountPremiumOfGraham()
    avgPriceInstance.setDiscountPremiumOfEBT()
    return avgPriceInstance.getOutput()


def createValueDF(combinedDF, priceDFList, company, instanceDict):
    valueInstance = Value(combinedDF, priceDFList, company)
    valueInstance.setPRRatio()
    valueInstance.setPSRatio()
    valueInstance.setPERatio()
    valueInstance.setPEGRatio()
    valueInstance.setPBRatio()
    return valueInstance.getOutput()


def createPriceTable(combinedDF, priceDFList, company):
    instanceDict = dict(
        valueInvesement=[],
        growthInvesement=[],
        valueInvesement2=dict(),
        growthInvesement2=dict(),
    )

    return pd.concat([createPriceDF(combinedDF, priceDFList, company),
                      createDDMDF(combinedDF, priceDFList,
                                  company, instanceDict),
                      createDDM2DF(combinedDF, priceDFList,
                                   company, instanceDict),
                      createDDMHDF(combinedDF, priceDFList,
                                   company, instanceDict),
                      createFCFEDF(combinedDF, priceDFList,
                                   company, instanceDict),
                      createDCFDF(combinedDF, priceDFList,
                                  company, instanceDict),
                      createGrahamDF(combinedDF, priceDFList,
                                     company, instanceDict),
                      createEBTDF(combinedDF, priceDFList,
                                  company, instanceDict),
                      createAvgPriceDF(combinedDF, priceDFList,
                                       company, instanceDict),
                      createValueDF(combinedDF, priceDFList,
                                    company, instanceDict), ], axis=1)
