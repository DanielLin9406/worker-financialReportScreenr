import pandas as pd
from ParsTable.dataClass.Dividend import Dividend
from ParsTable.dataClass.Profit import Profit
from ParsTable.dataClass.Growth import Growth
from ParsTable.dataClass.Safety import Safety
from ParsTable.dataClass.Industry import Industry


def createIndustryInfo(combinedDF, priceDFList, company):
    industryInstance = Industry(combinedDF, priceDFList, company)
    industryInstance.setMarketCapitalization()
    return industryInstance.getOutput()


def createDividendDF(combinedDF, priceDFList, company):
    dividendInstance = Dividend(
        combinedDF, priceDFList, company)
    dividendInstance.setDividend()
    dividendInstance.setDividendGrowth()
    dividendInstance.setTotalDivideds()
    dividendInstance.setAvgDividendin5years()
    dividendInstance.setMaxDividendin5Years()
    dividendInstance.setMinDividendin5Years()
    dividendInstance.setDividendGrowthin3Years()
    dividendInstance.setDividendGrowthin5Years()
    dividendInstance.setDividendYield()
    dividendInstance.setPayoutRatio()
    return dividendInstance.getOutput()


def createProfitDF(combinedDF, priceDFList, company):
    profitInstance = Profit(combinedDF, priceDFList, company)
    profitInstance.setROE()
    profitInstance.setAvgROEin4years()
    profitInstance.setMaxROEin4Years()
    profitInstance.setMinROEin4Years()
    profitInstance.setYearPercentageOfHighROE()
    profitInstance.setROA()
    profitInstance.setROS()
    # profitInstance.setGrossMargin()
    profitInstance.setOperatingMarin()
    profitInstance.setOperatingCashFlow()
    profitInstance.setNetIncome()
    profitInstance.setFreeCashFlow()
    profitInstance.setYearPercentageOfPositiveFreeCashFlow()
    profitInstance.setEPS()
    return profitInstance.getOutput()


def createGrowthDF(combinedDF, priceDFList, company):
    growthInstance = Growth(combinedDF, priceDFList, company)
    growthInstance.setROTA()
    growthInstance.setGrossMargin()
    growthInstance.setAssetTurnoverRatio()
    growthInstance.setReinvestmentRate()
    growthInstance.setResearch()
    growthInstance.setOperatingIncomeGrowth()
    growthInstance.setOperatingIncomeAccelerateGrowth()
    growthInstance.setYearPercentageOfOperatingIncomeGrowth()
    growthInstance.setRevenueGrowth()
    growthInstance.setYearPercentageOfRevenueGrowth()
    growthInstance.setEPSGrowth()
    growthInstance.setEPSGrowth3YearAvg()
    return growthInstance.getOutput()


def createSafetyDF(combinedDF, priceDFList, company):
    safetyInstance = Safety(combinedDF, priceDFList, company)
    safetyInstance.setTotalAssests()
    safetyInstance.setTotalLiabilities()
    safetyInstance.setLongTermDebt()
    safetyInstance.setCurrentRatio()
    safetyInstance.setQuickRatio()
    safetyInstance.setDebtEquityRatio()
    safetyInstance.setDebtCapitalRatio()
    safetyInstance.setDebtAssetsRatio()
    safetyInstance.setTotalDividendsFCFRatio()
    safetyInstance.setSharesCapital()
    return safetyInstance.getOutput()


def createParsTable(combinedDF, priceDFList, company):
    createIndustryInfo(combinedDF, priceDFList, company)
    return pd.concat([
        createIndustryInfo(combinedDF, priceDFList, company),
        createDividendDF(combinedDF, priceDFList, company),
        createProfitDF(combinedDF, priceDFList, company),
        createGrowthDF(combinedDF, priceDFList, company),
        createSafetyDF(combinedDF, priceDFList, company)], axis=1)
