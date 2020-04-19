import pandas as pd
import Config.config as config
from .Super import Super


class Value(Super):
    def __init__(self, **kwargs):
        thisYear = kwargs.get('reportsDF').columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.ValueName
        self.reportsDF = kwargs.get('reportsDF')
        self.priceDF = kwargs.get('priceDF')
        self.company = kwargs.get('company')

    def getPRRatio(self):
        if (self.getResearch().sum() == 0):
            return pd.Series([0.],  index=[self.latestYear])
        else:
            return self.divide(self.getPrice()*self.getShares(), self.getResearch())

    def getPSRatio(self):
        return self.divide(self.getPrice()*self.getShares(), self.getRevenue())

    def getPERatio(self):
        return self.divide(self.getPrice(), self.getEPS())

    def getPEGRatio(self):
        return self.divide(self.getPERatio(), self.getEPSGrowth3YearAvg()*100)

    def getPBRatio(self):
        return self.divide(self.getPrice()*self.getShares(), self.getStockholdersEquity())

    def setPBRatio(self):
        output = self.getPBRatio()
        self.setOutput(4, self.colName["PBRatio"], output, self.latestYear)

    def setPEGRatio(self):
        output = self.getPEGRatio()
        self.setOutput(3, self.colName["PEGRatio"], output, self.latestYear)

    def setPERatio(self):
        output = self.getPERatio()
        self.setOutput(2, self.colName["PERatio"], output, self.latestYear)

    def setPSRatio(self):
        output = self.getPSRatio()
        self.setOutput(1, self.colName["PSRatio"], output, self.latestYear)

    def setPRRatio(self):
        output = self.getPRRatio()
        self.setOutput(0, self.colName["PRRatio"], output, self.latestYear)
