import pandas as pd
from dataClass.DividendClass import Dividend
from dataClass.ProfitClass import Profit
from dataClass.GrowthClass import Growth
from dataClass.SafetyClass import Safety


def createDividendDF(combinedDF, priceDF, company):
    dividendInstance = Dividend(combinedDF, priceDF, company)
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


def createProfitDF(combinedDF, priceDF, company):
    profitInstance = Profit(combinedDF, priceDF, company)
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


def createGrowthDF(combinedDF, priceDF, company):
    growthInstance = Growth(combinedDF, priceDF, company)
    growthInstance.setROTA()
    growthInstance.setGrossMargin()
    growthInstance.setAssetTurnoverRatio()
    growthInstance.setReinvestmentRate()
    growthInstance.setOperatingIncome()
    return growthInstance.getOutput()


def createSafetyDF(combinedDF, priceDF, company):
    safetyInstance = Safety(combinedDF, priceDF, company)
    safetyInstance.setDebtEquityRatio()
    safetyInstance.setCurrentRatio()
    safetyInstance.setQuickRatio()
    safetyInstance.setDebtCapitalRatio()
    safetyInstance.setDebtAssetsRatio()
    safetyInstance.setDividendsFCFRatio()
    safetyInstance.setSharesCapital()
    return safetyInstance.getOutput()


def createParasTable(combinedDF, priceDF, company):
    return pd.concat([
        createDividendDF(combinedDF, priceDF, company),
        createProfitDF(combinedDF, priceDF, company),
        createGrowthDF(combinedDF, priceDF, company),
        createSafetyDF(combinedDF, priceDF, company)], axis=1)
