import pandas as pd
import numpy as np
import config
from dataClass.SuperData import Super


class Value(Super):
    def __init__(self, *args):
        Super.__init__(self, *args)
        self.colName = config.ValueName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getResearch(self):
        return -self.combinedDF.loc["Research and Development Expenses"]

    def getPRRatio(self):
        return np.divide(self.getPrice()*self.getShares(), self.getResearch())

    def getPSRatio(self):
        return np.divide(self.getPrice()*self.getShares(), self.getRevenue())

    def getPERatio(self):
        return np.divide(self.getPrice(), self.getEPS())

    def getPEGRatio(self):
        return np.divide(self.getPERatio(), self.getOperatingIncomeGrowth())

    def getPBRatio(self):
        return np.divide(self.getPrice()*self.getShares(), self.getStockholdersEquity())

    def setPBRatio(self):
        output = self.getPBRatio()
        self.setOutput(4, self.colName["PBRatio"], output, self.latestYear)

    def setPEGRatio(self):
        output = self.getPEGRatio()
        self.setOutput(3, self.colName["PEGRatio"], output, self.latestYear)

    def setPERatio(self):
        output = self.getPEGRatio()
        self.setOutput(2, self.colName["PERatio"], output, self.latestYear)

    def setPSRatio(self):
        output = self.getPSRatio()
        self.setOutput(1, self.colName["PSRatio"], output, self.latestYear)

    def setPRRatio(self):
        output = self.getPRRatio()
        self.setOutput(0, self.colName["PRRatio"], output, self.latestYear)
