import pandas as pd
import numpy as np
import Config.config as config
from .Super import Super


class AvgPrice(Super):
    def __init__(self, **kwargs):
        thisYear = kwargs.get('reportsDF').columns[0]
        super().__init__(thisYear)
        self.colName = config.PriceName
        self.priceDF = kwargs.get('priceDF')
        self.valueInvesementInstanceList = kwargs.get('valueInvesement')
        self.growthInvesementInstanceList = kwargs.get('growthInvesement')
        self.company = kwargs.get('company')

    def getDiscountPremium(self, currentPrice, estimatePrice):
        output = self.divide(currentPrice-estimatePrice, estimatePrice)
        if np.isnan(output):
            output = 0
        return pd.Series([output], index=[self.latestYear])

    def getDiscountPremiumOfEBT(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['EBT'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def getDiscountPremiumOfGraham(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['Graham'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def getDiscountPremiumOfDCF(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['DCF'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def getDiscountPremiumOfFCFE(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['FCFE'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def getDiscountPremiumOfDDMH(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['DDMH'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def getDiscountPremiumOfDDM2(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['DDM2'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def getDiscountPremiumOfDDM(self):
        currentPrice = self.getPrice().get(self.latestYear)
        estimatePrice = self.valueInvesementInstanceList['DDM'].getStockPrice(
        ).get(self.latestYear)
        return self.getDiscountPremium(currentPrice, estimatePrice)

    def setDiscountPremiumOfEBT(self):
        output = self.getDiscountPremiumOfEBT()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfEBT"], output, self.latestYear)

    def setDiscountPremiumOfGraham(self):
        output = self.getDiscountPremiumOfGraham()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfGraham"], output, self.latestYear)

    def setDiscountPremiumOfDCF(self):
        output = self.getDiscountPremiumOfDCF()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfDCF"], output, self.latestYear)

    def setDiscountPremiumOfFCFE(self):
        output = self.getDiscountPremiumOfFCFE()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfFCFE"], output, self.latestYear)

    def setDiscountPremiumOfDDMH(self):
        output = self.getDiscountPremiumOfDDMH()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfDDMH"], output, self.latestYear)

    def setDiscountPremiumOfDDM2(self):
        output = self.getDiscountPremiumOfDDM2()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfDDM2"], output, self.latestYear)

    def setDiscountPremiumOfDDM(self):
        output = self.getDiscountPremiumOfDDM()
        return self.setOutput(
            0, self.colName["DiscountPremiumOfDDM"], output, self.latestYear)

    def getAVGPriceofValueInvesement(self):
        output = np.nanmean([ele.getStockPrice().get(
            self.latestYear) for key, ele in self.valueInvesementInstanceList.items()])
        return pd.Series([output], index=[self.latestYear])

    def getAVGPriceofGrowthInvesement(self):
        output = np.nanmean([ele.getStockPrice().get(
            self.latestYear) for key, ele in self.growthInvesementInstanceList.items()])
        return pd.Series([output], index=[self.latestYear])

    def setAVGPriceofGrowthInvesement(self):
        output = self.getAVGPriceofGrowthInvesement()
        self.setOutput(
            0, self.colName["CAvgPriceofGrowthInvestment"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RAvgPriceofGrowthInvestment"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EAvgPriceofGrowthInvestment"], output, self.latestYear)

    def setAVGPriceofValueInvesement(self):
        output = self.getAVGPriceofValueInvesement()
        self.setOutput(
            0, self.colName["CAvgPriceofValueInvestment"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RAvgPriceofValueInvestment"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EAvgPriceofValueInvestment"], output, self.latestYear)
