import pandas as pd
from dataClass.DividendData import Dividend
from dataClass.ProfitData import Profit
from dataClass.GrowthData import Growth
from dataClass.SafetyData import Safety


def createDividendDF(combinedDF, priceDFList, company):
    dividendInstance = Dividend(combinedDF, priceDFList, company)
    dividendInstance.setDividend()
    dividendInstance.setTotalDivideds()
    dividendInstance.setAvgDividendin5years()
    dividendInstance.setMaxDividendin5Years()
    dividendInstance.setMinDividendin5Years()
    dividendInstance.setIsDividendGrowthin3Years()
    dividendInstance.setDividendGrowthin3Years()
    dividendInstance.setDividendGrowthin5Years()
    dividendInstance.setDividendYield()
    dividendInstance.setPayoutRatio()
    return dividendInstance.getOutput()


def createProfitDF(combinedDF, priceDFList, company):
    profitInstance = Profit(combinedDF, priceDFList, company)
    profitInstance.setROE()
    profitInstance.setAvgROEin5years()
    profitInstance.setMaxROEin5Years()
    profitInstance.setMinROEin5Years()
    profitInstance.setROA()
    profitInstance.setGrossMargin()
    profitInstance.setOperatingMarin()
    profitInstance.setOperatingCashFlow()
    profitInstance.setFreeCashFlow()
    return profitInstance.getOutput()


def createGrowthDF(combinedDF, priceDFList, company):
    growthInstance = Growth(combinedDF, priceDFList, company)
    growthInstance.setROTA()
    growthInstance.setGrossMargin()
    growthInstance.setAssetTurnoverRatio()
    growthInstance.setReinvestmentRate()
    growthInstance.setOperatingIncomeGrowth()
    growthInstance.setRevenueGrowth()
    return growthInstance.getOutput()


def createSafetyDF(combinedDF, priceDFList, company):
    safetyInstance = Safety(combinedDF, priceDFList, company)
    safetyInstance.setDebtEquityRatio()
    safetyInstance.setCurrentRatio()
    safetyInstance.setQuickRatio()
    safetyInstance.setDebtCapitalRatio()
    safetyInstance.setDebtAssetsRatio()
    safetyInstance.setDividendsFCFRatio()
    safetyInstance.setSharesCapital()
    return safetyInstance.getOutput()


def createParasTable(combinedDF, priceDFList, company):
    return pd.concat([
        createDividendDF(combinedDF, priceDFList, company),
        createProfitDF(combinedDF, priceDFList, company),
        createGrowthDF(combinedDF, priceDFList, company),
        createSafetyDF(combinedDF, priceDFList, company)], axis=1)
