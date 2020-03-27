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
    priceInstance.setHighGrowthPeriod()
    priceInstance.setYieldGrowthRate()
    priceInstance.setTerminalYieldGrowth()
    priceInstance.setDiscountRate()
    priceInstance.setMarginOfSafety()
    priceInstance.setDividendAfterNYears()
    priceInstance.setTreasuriesYield()
    priceInstance.setStockPrice()
    return priceInstance.getOutput()


def createDDMDF(combinedDF, priceDFList, company):
    ddmInstance = DDM(combinedDF, priceDFList, company)
    ddmInstance.setStockPriceDDM()
    return ddmInstance.getOutput()


def createDDM2DF(combinedDF, priceDFList, company):
    ddm2Instance = DDM2(combinedDF, priceDFList, company)
    ddm2Instance.setStockPriceDDM2()
    return ddm2Instance.getOutput()


def createDDMHDF(combinedDF, priceDFList, company):
    ddmHInstance = DDMH(combinedDF, priceDFList, company)
    ddmHInstance.setStockPriceDDMH()
    return ddmHInstance.getOutput()


def createFCFFDF(combinedDF, priceDFList, company):
    fcffHInstance = FCFF(combinedDF, priceDFList, company)
    # fcffHInstance.setStockPriceFCFF()


def createFCFEDF(combinedDF, priceDFList, company):
    fcfeInstance = FCFE(combinedDF, priceDFList, company)
    fcfeInstance.setStockPriceFCFE()
    return fcfeInstance.getOutput()


def createDCFDF(combinedDF, priceDFList, company):
    dcfInstance = DCF(combinedDF, priceDFList, company)
    dcfInstance.setStockPriceDCF()
    return dcfInstance.getOutput()


def createEBTDF(combinedDF, priceDFList, company):
    ebtInstance = EBT(combinedDF, priceDFList, company)
    ebtInstance.setEBTPriceRatio()
    return ebtInstance.getOutput()


def createGrahamDF(combinedDF, priceDFList, company):
    grahamInstance = Graham(combinedDF, priceDFList, company)
    grahamInstance.setBenjaminGrahamPrice()
    return grahamInstance.getOutput()


def createAvgPriceDF(combinedDF, priceDFList, company):
    avgPriceInstance = AvgPrice(combinedDF, priceDFList, company)
    avgPriceInstance.setAVGPriceofValueInvesement()
    avgPriceInstance.setAVGPriceofGrowthInvesement()
    return avgPriceInstance.getOutput()


def createValueDF(combinedDF, priceDFList, company):
    valueInstance = Value(combinedDF, priceDFList, company)
    valueInstance.setPRRatio()
    valueInstance.setPSRatio()
    valueInstance.setPERatio()
    valueInstance.setPEGRatio()
    valueInstance.setPBRatio()
    return valueInstance.getOutput()


def createPriceTable(combinedDF, priceDFList, company):
    return pd.concat([createPriceDF(combinedDF, priceDFList, company),
                      createDDMDF(combinedDF, priceDFList, company),
                      createDDM2DF(combinedDF, priceDFList, company),
                      createDDMHDF(combinedDF, priceDFList, company),
                      createFCFEDF(combinedDF, priceDFList, company),
                      createDCFDF(combinedDF, priceDFList, company),
                      createGrahamDF(combinedDF, priceDFList, company),
                      createEBTDF(combinedDF, priceDFList, company),
                      createAvgPriceDF(combinedDF, priceDFList, company),
                      createValueDF(combinedDF, priceDFList, company)], axis=1)
