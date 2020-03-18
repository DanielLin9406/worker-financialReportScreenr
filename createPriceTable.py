import pandas as pd
from dataClass.PriceData import Price
from dataClass.ValueData import Value


def createPriceDF(combinedDF, priceDFList, company):
    priceInstance = Price(combinedDF, priceDFList, company)
    priceInstance.setHighGrowthPeriod()
    priceInstance.setYieldGrowthRate()
    priceInstance.setTerminalYieldGrowth()
    priceInstance.setDiscountRate()
    priceInstance.setMarginOfSafety()
    priceInstance.setDividendAfterNYears()
    priceInstance.setStockPriceDDM2()
    priceInstance.setStockPriceDDMH()
    priceInstance.setStockPriceFCFE()
    priceInstance.setStockPriceFCFF()
    priceInstance.setBenjaminGrahamPrice()
    priceInstance.setEBTPriceRatio()
    return priceInstance.getOutput()


def createValueDF(combinedDF, priceDFList, company):
    valueInstance = Value(combinedDF, priceDFList, company)
    valueInstance.setPRRatio()
    valueInstance.setPSRatio()
    valueInstance.setPERatio()
    valueInstance.setPEGRatio()
    valueInstance.setPBRatio()
    return valueInstance.getOutput()


def createPriceTable(combinedDF, priceDFList, company):
    return pd.concat([createPriceDF(combinedDF, priceDFList, company), createValueDF(combinedDF, priceDFList, company)], axis=1)
