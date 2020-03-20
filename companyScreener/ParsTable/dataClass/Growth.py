import pandas as pd
import numpy as np
import config
from ParsTable.dataClass.Super import Super


class Growth(Super):
    def __init__(self, *args):
        Super.__init__(self)
        self.colName = config.GrowthName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getProvisionforIncomeTax(self):
        return -self.combinedDF.loc['Provision for Income Tax']

    def get1MinusTax(self):
        return np.divide(self.getPretaxIncome()-self.getProvisionforIncomeTax(), self.getPretaxIncome())

    def getReinvestmentRate(self):
        return np.divide(self.getCapitalExpenditures()+self.getChangeInWorkingCapital(), self.getEBIT()*self.get1MinusTax())

    def getROTA(self):
        return np.divide(self.getEBIT(), self.getTotalAssets())

    def getAssetTurnoverRatio(self):
        return np.divide(self.getRevenue(), self.getTotalAssets())

    def getRevenueGrowth(self):
        latestYear = self.getRevenue().get(self.latestYear)
        lastYear = self.getRevenue().get(self.lastYear)
        twoYearsAgo = self.getRevenue().get(self.twoYearsAgo)
        threeYearsAgo = self.getRevenue().get(self.threeYearsAgo)
        output1 = np.divide((latestYear-lastYear), lastYear)
        output2 = np.divide((lastYear-twoYearsAgo), twoYearsAgo)
        output3 = np.divide((twoYearsAgo-threeYearsAgo), threeYearsAgo)
        return pd.Series([output1, output2, output3], index=[self.latestYear, self.lastYear, self.twoYearsAgo])

    def setEPSGrowth(self):
        output = self.getEPSGrowth()
        self.setOutput(
            13, self.colName["EPSGrowth"], output, self.latestYear)

    def setRevenueGrowth(self):
        output = self.getRevenueGrowth()
        self.setOutput(
            12, self.colName["revenueGrowthn2"], output, self.twoYearsAgo)
        self.setOutput(
            11, self.colName["revenueGrowthn1"], output, self.lastYear)
        self.setOutput(
            10, self.colName["revenueGrowth"], output, self.latestYear)

    def setOperatingIncomeGrowth(self):
        output = self.getOperatingIncomeGrowth()
        self.setOutput(
            9, self.colName["operatingIncomeGrowthn2"], output, self.twoYearsAgo)
        self.setOutput(
            8, self.colName["operatingIncomeGrowthn1"], output, self.lastYear)
        self.setOutput(
            7, self.colName["operatingIncomeGrowth"], output, self.latestYear)

    def setReinvestmentRate(self):
        output = self.getReinvestmentRate()
        self.setOutput(
            6, self.colName["reinvestmentRate"], output, self.latestYear)

    def setAssetTurnoverRatio(self):
        output = self.getAssetTurnoverRatio()
        self.setOutput(
            5, self.colName["assetTurnoverRation1"], output, self.lastYear)
        self.setOutput(
            4, self.colName["assetTurnoverRatio"], output, self.latestYear)

    def setGrossMargin(self):
        output = self.getGrossMargin()
        self.setOutput(3, self.colName["grossMarginn1"], output, self.lastYear)
        self.setOutput(2, self.colName["grossMargin"], output, self.latestYear)

    def setROTA(self):
        output = self.getROTA()
        self.setOutput(1, self.colName["ROTAn1"], output, self.lastYear)
        self.setOutput(0, self.colName["ROTA"], output, self.latestYear)
