import pandas as pd
from ParsTable.dataClass.Dividend import Dividend
from ParsTable.dataClass.Profit import Profit
from ParsTable.dataClass.Growth import Growth
from ParsTable.dataClass.Safety import Safety
from ParsTable.dataClass.Industry import Industry


def createIndustryInfo(combinedDF, parsDFList, company):
    industryInstance = Industry(combinedDF, parsDFList, company)
    industryInstance.setSector()
    industryInstance.setIndustry()
    industryInstance.setMarketCapitalization()
    return industryInstance.getOutput()


def createDividendDF(combinedDF, parsDFList, company):
    dividendInstance = Dividend(
        combinedDF, parsDFList, company)
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


def createProfitDF(combinedDF, parsDFList, company):
    profitInstance = Profit(combinedDF, parsDFList, company)
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


def createGrowthDF(combinedDF, parsDFList, company):
    growthInstance = Growth(combinedDF, parsDFList, company)
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


def createSafetyDF(combinedDF, parsDFList, company):
    safetyInstance = Safety(combinedDF, parsDFList, company)
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


def createParsTable(combinedDF, parsDFList, company):
    return pd.concat([
        createIndustryInfo(combinedDF, parsDFList, company),
        createDividendDF(combinedDF, parsDFList, company),
        createProfitDF(combinedDF, parsDFList, company),
        createGrowthDF(combinedDF, parsDFList, company),
        createSafetyDF(combinedDF, parsDFList, company)], axis=1)
