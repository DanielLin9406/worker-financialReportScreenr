import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.DDM import DDM
from PriceTable.dataClass.DDM2 import DDM2
from PriceTable.dataClass.DCF import DCF
from PriceTable.dataClass.DDMH import DDMH
from PriceTable.dataClass.EBT import EBT
from PriceTable.dataClass.FCFF import FCFF
from PriceTable.dataClass.FCFE import FCFE
from PriceTable.dataClass.Graham import Graham


class AvgPrice(DDM, DDM2, DDMH, DCF, EBT, FCFF, FCFE, Graham):
    def __init__(self, *args):
        super().__init__(*args)

    def getAVGPriceofGrowthInvesement(self):
        output = np.average(
            [self.getStockPriceFCFE().get(self.latestYear), self.getEBTPriceRatio().get(self.latestYear)])
        return pd.Series([output], index=[self.latestYear])

    def getAVGPriceofValueInvesement(self):
        output = np.average([self.getStockPriceDDM2().get(self.latestYear), self.getStockPriceDDM().get(self.latestYear), self.getStockPriceDDMH(
        ).get(self.latestYear), self.getStockPriceFCFE().get(self.latestYear), self.getBenjaminGrahamPrice().get(self.latestYear), self.getEBTPriceRatio().get(self.latestYear)])
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
