import pandas as pd
import numpy as np
import config
from dataClass.SuperData import Super


class Price(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.colName = config.PriceName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.treasuriesYieldDF = args[1][1]
        self.company = args[2]

    def getTreasuriesYield(self):
        return pd.Series(self.treasuriesYieldDF.loc["5 YR"], index=[self.latestYear], dtype="float")

    def getDepreciation(self):
        return self.combinedDF.loc["Depreciation, Amortization and Depletion, Non-Cash Adjustment"]

    def getNetBorrowings(self):
        return self.combinedDF.loc["Issuance of/Repayments for Debt, Net"]

    def getTaxRate(self):
        return pd.Series(config.FCFF["taxRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getMarginOfSafety(self):
        return pd.Series(config.marginOfSafety,  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getBenjaminGrahamPrice(self):
        EPS = self.getEPS().get(self.latestYear)
        EPSGrowth = self.getEPSGrowth().get(self.latestYear)
        treasuriesYield = self.getTreasuriesYield().get(self.latestYear)
        return pd.Series(np.divide(EPS*(2*EPSGrowth+8.5)*4.4, treasuriesYield), index=[self.latestYear])

    def getEBT(self):
        return np.divide(self.getPretaxIncome(), self.getShares())

    def getEBTPriceRatio(self):
        return np.divide(self.getEBT(), 0.1)

    def getCostOfCapital(self):
        return pd.Series(config.FCFF["costOfCapital"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getCostofEquity(self):
        return pd.Series(config.FCFE["costOfEquity"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getInfiniteGrowthRateFCFF(self):
        return pd.Series(config.FCFF["infiniteGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getInfiniteGrowthRateFCFE(self):
        return pd.Series(config.FCFE["infiniteGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getFCFF(self):
        return (self.getEBIT()*(1-self.getTaxRate())+self.getDepreciation()+self.getChangeInWorkingCapital()-self.getCapitalExpenditures()).dropna()

    def getFCFE(self):
        return (self.getNetIncome() + self.getDepreciation()+self.getChangeInWorkingCapital() -
                self.getCapitalExpenditures()+self.getNetBorrowings()).dropna()

    def getNPVofExplicitPeriodFCFF(self):
        return np.npv(self.getCostOfCapital().get(self.latestYear), self.getFCFF().tolist())

    def getNPVofExplicitPeriodFCFE(self):
        return np.npv(self.getCostofEquity().get(self.latestYear), self.getFCFE().tolist())

    def getNPVofTerminalValueFCFF(self):
        return np.divide(self.getFCFF().get(self.latestYear)*(1+self.getInfiniteGrowthRateFCFF().get(self.latestYear)), self.getCostOfCapital().get(self.latestYear)-self.getInfiniteGrowthRateFCFF().get(self.latestYear))

    def getNPVofTerminalValueFCFE(self):
        return np.divide(self.getFCFE().get(self.latestYear)*(1+self.getInfiniteGrowthRateFCFE().get(self.latestYear)), self.getCostofEquity().get(self.latestYear)-self.getInfiniteGrowthRateFCFE().get(self.latestYear))

    def getEnterpriceValueFCFF(self):
        return self.getNPVofTerminalValueFCFF()+self.getNPVofExplicitPeriodFCFF()

    def getEquityValueFCFF(self):
        return self.getEnterpriceValueFCFF()+self.getFreeCashFlow()-self.getTotalLiabilities()

    def getEquityValueFCFE(self):
        return self.getNPVofExplicitPeriodFCFE()+self.getNPVofTerminalValueFCFE()

    def getStockPriceFCFF(self):
        return np.divide(self.getEquityValueFCFF(), self.getShares())

    def getStockPriceFCFE(self):
        return np.divide(self.getEquityValueFCFE(), self.getShares())

    def getDiscountRate(self):
        return pd.Series(config.DDM["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getTerminalYieldGrowth(self):
        return pd.Series(config.DDM["terminalYieldGrowth"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getYieldGrowthRate(self):
        return pd.Series(config.DDM["yieldGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthPeriod(self):
        return pd.Series(config.DDM["highGrowthPeriod"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getExplicitPeriodDDMH(self):
        return np.divide(1+self.getDiscountRate(), self.getDiscountRate()-self.getYieldGrowthRate())

    def getTerminalValueDDMH(self):
        return self.getDividend()*self.getHighGrowthPeriod()*np.divide(self.getYieldGrowthRate()-self.getTerminalYieldGrowth(), self.getDiscountRate()-self.getYieldGrowthRate())

    def getExplicitPeriodDDM2(self):
        section1 = np.divide(1+self.getDiscountRate(),
                             self.getDiscountRate()-self.getTerminalYieldGrowth())
        section2 = np.divide(np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod()),
                             np.power(self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*section2

    def getTerminalValueDDM2(self):
        section1 = np.divide(1+self.getDiscountRate(),
                             self.getDiscountRate()-self.getYieldGrowthRate())
        section2 = 1 - np.divide(np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod()),
                                 np.power(self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*section2

    def getStockPriceDDMH(self):
        return self.getExplicitPeriodDDMH()+self.getTerminalValueDDMH()

    def getStockPriceDDM2(self):
        return self.getExplicitPeriodDDM2()+self.getTerminalValueDDM2()

    def getDividendAfterNYears(self):
        return self.getDividend()*np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod())

    def setEBTPriceRatio(self):
        output = self.getEBTPriceRatio()
        self.setOutput(
            13, self.colName["EBTRatio"], output, self.latestYear)

    def setBenjaminGrahamPrice(self):
        output = self.getBenjaminGrahamPrice()
        self.setOutput(
            12, self.colName["BenjaminGraham"], output, self.latestYear)

    def setStockPriceFCFF(self):
        output = self.getStockPriceFCFF()
        self.setOutput(
            11, self.colName["PriceFCFF"], output, self.latestYear)

    def setStockPriceFCFE(self):
        output = self.getStockPriceFCFE()
        self.setOutput(
            10, self.colName["PriceFCFE"], output, self.latestYear)

    def setStockPriceDDMH(self):
        output = self.getStockPriceDDMH()
        self.setOutput(
            9, self.colName["PriceDDMH"], output, self.latestYear)

    def setStockPriceDDM2(self):
        output = self.getStockPriceDDM2()
        self.setOutput(
            8, self.colName["PriceDDM2"], output, self.latestYear)

    def setStockPrice(self):
        output = self.getPrice()
        self.setOutput(
            7, self.colName["stockPrice"], output, self.latestYear)

    def setTreasuriesYield(self):
        output = self.getTreasuriesYield()
        self.setOutput(
            6, self.colName["treasuriesYield"], output, self.latestYear)

    def setDividendAfterNYears(self):
        output = self.getDividendAfterNYears()
        self.setOutput(
            5, self.colName["dividendAfterNYears"], output, self.latestYear)

    def setMarginOfSafety(self):
        output = self.getMarginOfSafety()
        self.setOutput(
            4, self.colName["marginOfSafety"], output, self.latestYear)

    def setDiscountRate(self):
        output = self.getDiscountRate()
        self.setOutput(
            3, self.colName["discountRate"], output, self.latestYear)

    def setTerminalYieldGrowth(self):
        output = self.getTerminalYieldGrowth()
        self.setOutput(
            2, self.colName["terminalYieldGrowth"], output, self.latestYear)

    def setYieldGrowthRate(self):
        output = self.getYieldGrowthRate()
        self.setOutput(
            1, self.colName["yieldGrowthRate"], output, self.latestYear)

    def setHighGrowthPeriod(self):
        output = self.getHighGrowthPeriod()
        self.setOutput(
            0, self.colName["highGrowthPeriod"], output, self.latestYear)
