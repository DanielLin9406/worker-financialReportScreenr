import pandas as pd
import numpy as np
import config
from ParsTable.dataClass.Super import Super


class Price(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.PriceName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.treasuriesYieldDF = args[1][1]
        self.company = args[2]

    def getTreasuriesYield(self):
        return pd.Series(self.treasuriesYieldDF.iloc[0][0]/100, index=[self.latestYear], dtype="float")

    def getDepreciation(self):
        return self.getParsSeries("Depreciation, Amortization and Depletion, Non-Cash Adjustment")

    def getNetBorrowings(self):
        return self.getParsSeries("Issuance of/Repayments for Debt, Net")

    def getTaxRate(self):
        return pd.Series(config.FCFF["taxRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getMarginOfSafety(self):
        return pd.Series(config.marginOfSafety,  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getBenjaminGrahamPrice(self):
        EPS = self.getEPS().get(self.latestYear)
        EPSGrowth = self.getEPSGrowth3YearAvg().get(self.latestYear)
        treasuriesYield = self.getTreasuriesYield().get(self.latestYear)
        return pd.Series(np.divide(EPS*(EPSGrowth*100+7)*4.4, self.getTreasuriesYield()*100), index=[self.latestYear])

    def getEBT(self):
        return self.divide(self.getPretaxIncome(), self.getShares())

    def getEBTPriceRatio(self):
        return self.divide(self.getEBT(), 0.1)

    def getCostOfCapital(self):
        return pd.Series(config.FCFF["costOfCapital"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getCostofEquity(self):
        return pd.Series(config.FCFE["costOfEquity"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getInfiniteGrowthRateFCFF(self):
        return pd.Series(config.FCFF["infiniteGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getInfiniteGrowthRateFCFE(self):
        return pd.Series(config.FCFE["infiniteGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getFCFF(self):
        return (self.getEBIT()*(1-self.getTaxRate()) + self.getDepreciation() +
                self.getChangeInWorkingCapital() - self.getCapitalExpenditures())

    def getFCFE(self):
        return (self.getNetIncome()+self.getDepreciation()+self.getChangeInWorkingCapital() +
                self.getCapitalExpenditures()+self.getNetBorrowings())

    def getNPVofExplicitPeriodFCFF(self):
        return np.npv(self.getCostOfCapital().get(self.latestYear), self.getFCFF().tolist())

    def getNPVofExplicitPeriodFCFE(self):
        return np.npv(self.getCostofEquity().get(self.latestYear), self.getFCFE().tolist())

    def getNPVofTerminalValueFCFF(self):
        return self.divide(self.getFCFF().get(self.latestYear)*(1+self.getInfiniteGrowthRateFCFF().get(self.latestYear)), self.getCostOfCapital().get(self.latestYear)-self.getInfiniteGrowthRateFCFF().get(self.latestYear))

    def getNPVofTerminalValueFCFE(self):
        print(self.getFCFE())
        return self.divide(self.getFCFE().get(self.latestYear)*(1+self.getInfiniteGrowthRateFCFE().get(self.latestYear)), self.getCostofEquity().get(self.latestYear)-self.getInfiniteGrowthRateFCFE().get(self.latestYear))

    def getEnterpriceValueFCFF(self):
        return self.getNPVofTerminalValueFCFF()+self.getNPVofExplicitPeriodFCFF()

    def getEquityValueFCFF(self):
        return self.getEnterpriceValueFCFF()+self.getFreeCashFlow()-self.getTotalLiabilities()

    def getEquityValueFCFE(self):
        # print(self.getNPVofExplicitPeriodFCFE())
        # print(self.getNPVofTerminalValueFCFE())
        return self.sum([self.getNPVofExplicitPeriodFCFE(), self.getNPVofTerminalValueFCFE()])

    def getStockPriceFCFF(self):
        # print('FCFF', self.getFCFF())
        return self.divide(self.getEquityValueFCFF(), self.getShares())

    def getStockPriceFCFE(self):
        return self.divide(self.getEquityValueFCFE(), self.getShares())

    def getDiscountRate(self):
        return pd.Series(config.DDM["discountRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getTerminalYieldGrowth(self):
        return pd.Series(config.DDM["terminalYieldGrowth"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getYieldGrowthRate(self):
        return pd.Series(config.DDM["yieldGrowthRate"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getHighGrowthPeriod(self):
        return pd.Series(config.DDM["highGrowthPeriod"],  index=[self.latestYear, self.lastYear, self.twoYearsAgo, self.threeYearsAgo, self.fourYearsAgo], dtype="float")

    def getExplicitPeriodDDMH(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getTerminalYieldGrowth())
        return self.getDividend()*section1

    def getTerminalValueDDMH(self):
        section1 = self.divide(self.getYieldGrowthRate(
        )-self.getTerminalYieldGrowth(), self.getDiscountRate()-self.getTerminalYieldGrowth())
        return self.getDividend()*self.getHighGrowthPeriod()*section1

    def getExplicitPeriodDDM2(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getYieldGrowthRate())
        section2 = self.divide(np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod()),
                               np.power(1+self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*(1-section2)

    def getTerminalValueDDM2(self):
        section1 = self.divide(1+self.getDiscountRate(),
                               self.getDiscountRate()-self.getTerminalYieldGrowth())
        section2 = self.divide(np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod()),
                               np.power(1+self.getDiscountRate(), self.getHighGrowthPeriod()))
        return self.getDividend()*section1*section2

    def getStockPriceDDMH(self):
        return self.getExplicitPeriodDDMH()+self.getTerminalValueDDMH()

    def getStockPriceDDM2(self):
        return self.getExplicitPeriodDDM2()+self.getTerminalValueDDM2()

    def getDividendAfterNYears(self):
        return self.getDividend()*np.power(1+self.getYieldGrowthRate(), self.getHighGrowthPeriod())

    def getAVGPriceofGrowthInvesement(self):
        output = np.average(
            [self.getStockPriceFCFE().get(self.latestYear), self.getStockPriceFCFF().get(self.latestYear), self.getEBTPriceRatio().get(self.latestYear)])
        return pd.Series([output], index=[self.latestYear])

    def getAVGPriceofValueInvesement(self):
        output = np.average([self.getStockPriceDDM2().get(self.latestYear), self.getStockPriceDDMH(
        ).get(self.latestYear), self.getBenjaminGrahamPrice().get(self.latestYear), self.getEBTPriceRatio().get(self.latestYear)])
        return pd.Series([output], index=[self.latestYear])

    def setAVGPriceofGrowthInvesement(self):
        output = self.getAVGPriceofGrowthInvesement()
        self.setOutput(
            29, self.colName["CAvgPriceofGrowthInvestment"], output, self.latestYear)
        self.setOutput(
            30, self.colName["RAvgPriceofGrowthInvestment"], output, self.latestYear)
        self.setOutput(
            31, self.colName["EAvgPriceofGrowthInvestment"], output, self.latestYear)

    def setAVGPriceofValueInvesement(self):
        output = self.getAVGPriceofValueInvesement()
        self.setOutput(
            26, self.colName["CAvgPriceofValueInvestment"], output, self.latestYear)
        self.setOutput(
            27, self.colName["RAvgPriceofValueInvestment"], output, self.latestYear)
        self.setOutput(
            28, self.colName["EAvgPriceofValueInvestment"], output, self.latestYear)

    def setEBTPriceRatio(self):
        output = self.getEBTPriceRatio()
        self.setOutput(
            23, self.colName["CEBTRatio"], output, self.latestYear)
        self.setOutput(
            24, self.colName["REBTRatio"], output, self.latestYear)
        self.setOutput(
            25, self.colName["EEBTRatio"], output, self.latestYear)

    def setBenjaminGrahamPrice(self):
        output = self.getBenjaminGrahamPrice()
        self.setOutput(
            20, self.colName["CBenjaminGraham"], output, self.latestYear)
        self.setOutput(
            21, self.colName["RBenjaminGraham"], output, self.latestYear)
        self.setOutput(
            22, self.colName["EBenjaminGraham"], output, self.latestYear)

    def setStockPriceFCFF(self):
        output = self.getStockPriceFCFF()
        self.setOutput(
            17, self.colName["CPriceFCFF"], output, self.latestYear)
        self.setOutput(
            18, self.colName["RPriceFCFF"], output, self.latestYear)
        self.setOutput(
            19, self.colName["EPriceFCFF"], output, self.latestYear)

    def setStockPriceFCFE(self):
        output = self.getStockPriceFCFE()
        self.setOutput(
            14, self.colName["CPriceFCFE"], output, self.latestYear)
        self.setOutput(
            15, self.colName["RPriceFCFE"], output, self.latestYear)
        self.setOutput(
            16, self.colName["EPriceFCFE"], output, self.latestYear)

    def setStockPriceDDMH(self):
        output = self.getStockPriceDDMH()
        self.setOutput(
            11, self.colName["CPriceDDMH"], output, self.latestYear)
        self.setOutput(
            12, self.colName["RPriceDDMH"], output, self.latestYear)
        self.setOutput(
            13, self.colName["EPriceDDMH"], output, self.latestYear)

    def setStockPriceDDM2(self):
        output = self.getStockPriceDDM2()
        self.setOutput(
            8, self.colName["CPriceDDM2"], output, self.latestYear)
        self.setOutput(
            9, self.colName["RPriceDDM2"], output, self.latestYear)
        self.setOutput(
            10, self.colName["EPriceDDM2"], output, self.latestYear)

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
