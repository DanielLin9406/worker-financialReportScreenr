import pandas as pd
import numpy as np
from dataClass.SuperClass import Super


class Growth(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.combinedDF = args[0]
        self.priceDF = args[1]
        self.company = args[2]

    def getOperatingExpenses(self):
        return -self.combinedDF.loc["Operating Income/Expenses"]

    def getPretaxIncome(self):
        return self.combinedDF.loc['Pretax Income']

    def getProvisionforIncomeTax(self):
        return -self.combinedDF.loc['Provision for Income Tax']

    def getChangeInWorkingCapital(self):
        return np.divide(self.getCurrentLiabilities(), self.getCurrentAssets())

    def get1MinusTax(self):
        return np.divide(self.getPretaxIncome()-self.getProvisionforIncomeTax(), self.getPretaxIncome())

    def getEBIT(self):
        return self.getRevenue()-self.getFreeCashFlow()-self.getOperatingExpenses()

    def getReinvestmentRate(self):
        return np.divide(self.getCapitalExpenditures()+self.getChangeInWorkingCapital(), self.getEBIT()*self.get1MinusTax())

    def getROTA(self):
        return np.divide(self.getEBIT(), self.getTotalAssets())

    def getAssetTurnoverRatio(self):
        return np.divide(self.getRevenue(), self.getTotalAssets())

    def setOperatingIncome(self):
        output = self.getOperatingIncome()
        self.setOutput(8, "Operating Income(n-1)", output, self.lastYear)
        self.setOutput(7, "Operating Income", output, self.latestYear)

    def setReinvestmentRate(self):
        output = self.getReinvestmentRate()
        self.setOutput(6, "Reinvestment Rate", output, self.latestYear)

    def setAssetTurnoverRatio(self):
        output = self.getAssetTurnoverRatio()
        self.setOutput(5, "Asset Turnover Ratio(n-1)", output, self.lastYear)
        self.setOutput(4, "Asset Turnover Ratio", output, self.latestYear)

    def setGrossMargin(self):
        output = self.getGrossMargin()
        self.setOutput(3, "Gross Margin(n-1)", output, self.lastYear)
        self.setOutput(2, "Gross Margin", output, self.latestYear)

    def setROTA(self):
        output = self.getROTA()
        self.setOutput(1, "ROTA(n-1)", output, self.lastYear)
        self.setOutput(0, "ROTA", output, self.latestYear)
