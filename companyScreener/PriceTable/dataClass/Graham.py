import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class Graham(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getGrowthRate(self):
        return self.getGrowthRateByPRATModel()

    def getStockPrice(self):
        EPS = self.getEPS().get(self.latestYear)
        growthRate = self.getGrowthRate().get(str(int(self.latestYear)+1))
        treasuriesYield = self.getTreasuriesYield().get(self.latestYear)
        return pd.Series(np.divide(EPS*(growthRate*100+7)*4.4, self.getTreasuriesYield()*100), index=[self.latestYear])

    def setGrowthRate(self):
        output = self.getGrowthRate()
        self.setOutput(
            0, self.colName["growthRateByPRATModel"], output, str(int(self.latestYear)+1))

    def setStockPrice(self):
        output = self.getStockPrice()
        self.setOutput(
            0, self.colName["CBenjaminGraham"], output, self.latestYear)
        self.setOutput(
            0, self.colName["RBenjaminGraham"], output, self.latestYear)
        self.setOutput(
            0, self.colName["EBenjaminGraham"], output, self.latestYear)
