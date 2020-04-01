import pandas as pd
import numpy as np
import config
from ParsTable.dataClass.Super import Super


class Growth(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.GrowthName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getProvisionforIncomeTax(self):
        return -self.getParsSeries('Provision for Income Tax')

    def get1MinusTax(self):
        return self.divide(self.getPretaxIncome()-self.getProvisionforIncomeTax(), self.getPretaxIncome())

    def getReinvestmentRate(self):
        return self.divide(self.getCapitalExpenditures()+self.getChangeInWorkingCapital(), self.getEBIT()*self.get1MinusTax())

    def getROTA(self):
        return self.divide(self.getEBIT(), self.getTotalAssets())

    def getRevenueGrowth(self):
        latestYear = self.getRevenue().get(self.latestYear)
        lastYear = self.getRevenue().get(self.lastYear)
        twoYearsAgo = self.getRevenue().get(self.twoYearsAgo)
        threeYearsAgo = self.getRevenue().get(self.threeYearsAgo)
        output1 = self.divide((latestYear-lastYear), lastYear)
        output2 = self.divide((lastYear-twoYearsAgo), twoYearsAgo)
        output3 = self.divide((twoYearsAgo-threeYearsAgo), threeYearsAgo)
        return pd.Series([output1, output2, output3], index=[self.latestYear, self.lastYear, self.twoYearsAgo])

    def getOperatingIncomeAccelerateGrowth(self):
        latestYearGrowthRate = self.getOperatingIncomeGrowth().get(self.latestYear)
        twoYearsAgoGrowthRate = self.getOperatingIncomeGrowth().get(self.twoYearsAgo)
        output = self.divide(
            (latestYearGrowthRate-twoYearsAgoGrowthRate), twoYearsAgoGrowthRate)
        return pd.Series([output], index=[self.latestYear])

    def getYearPercentageOfOperatingIncomeGrowth(self):
        output = self.divide(
            np.sum(self.getOperatingIncomeGrowth().dropna().gt(0.15)),
            len(self.getOperatingIncomeGrowth().dropna()))
        return pd.Series([output], index=[self.latestYear])

    def getYearPercentageOfRevenueGrowth(self):
        output = self.divide(
            np.sum(self.getRevenueGrowth().dropna().gt(0)),
            len(self.getRevenueGrowth().dropna()))
        return pd.Series([output], index=[self.latestYear])

    def setEPSGrowth3YearAvg(self):
        output = self.getEPSGrowth3YearAvg()
        self.setOutput(
            0, self.colName["EPSGrowth3YearAvg"], output, self.latestYear)

    def setEPSGrowth(self):
        output = self.getEPSGrowth()
        self.setOutput(
            0, self.colName["EPSGrowth"], output, self.latestYear)

    def setYearPercentageOfRevenueGrowth(self):
        output = self.getYearPercentageOfRevenueGrowth()
        self.setOutput(
            0, self.colName["yearPercentageOfRevenueGrowth"], output, self.latestYear)

    def setRevenueGrowth(self):
        output = self.getRevenueGrowth()
        self.setOutput(
            0, self.colName["revenueGrowth"], output, self.latestYear)
        self.setOutput(
            0, self.colName["revenueGrowthn1"], output, self.lastYear)
        self.setOutput(
            0, self.colName["revenueGrowthn2"], output, self.twoYearsAgo)

    def setYearPercentageOfOperatingIncomeGrowth(self):
        output = self.getYearPercentageOfOperatingIncomeGrowth()
        self.setOutput(
            0, self.colName["yearPercentageOfOperatingIncomeGrowth"], output, self.latestYear)

    def setOperatingIncomeAccelerateGrowth(self):
        output = self.getOperatingIncomeAccelerateGrowth()
        self.setOutput(
            0, self.colName["operatingIncomeAccelerateGrowth"], output, self.latestYear)

    def setOperatingIncomeGrowth(self):
        output = self.getOperatingIncomeGrowth()
        self.setOutput(
            0, self.colName["operatingIncomeGrowth"], output, self.latestYear)
        self.setOutput(
            0, self.colName["operatingIncomeGrowthn1"], output, self.lastYear)
        self.setOutput(
            0, self.colName["operatingIncomeGrowthn2"], output, self.twoYearsAgo)

    def setResearch(self):
        output = self.getResearch()
        self.setOutput(
            0, self.colName["research"], output, self.latestYear)
        self.setOutput(
            0, self.colName["researchn1"], output, self.lastYear)

    def setReinvestmentRate(self):
        output = self.getReinvestmentRate()
        self.setOutput(
            0, self.colName["reinvestmentRate"], output, self.latestYear)

    def setAssetTurnoverRatio(self):
        output = self.getAssetTurnoverRatio()
        self.setOutput(
            0, self.colName["assetTurnoverRatio"], output, self.latestYear)
        self.setOutput(
            0, self.colName["assetTurnoverRation1"], output, self.lastYear)

    def setGrossMargin(self):
        output = self.getGrossMargin()
        self.setOutput(0, self.colName["grossMargin"], output, self.latestYear)
        self.setOutput(0, self.colName["grossMarginn1"], output, self.lastYear)

    def setROTA(self):
        output = self.getROTA()
        self.setOutput(0, self.colName["ROTA"], output, self.latestYear)
        self.setOutput(0, self.colName["ROTAn1"], output, self.lastYear)
