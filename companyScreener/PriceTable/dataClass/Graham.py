import pandas as pd
import numpy as np
import config
from PriceTable.dataClass.Price import Price


class Graham(Price):
    def __init__(self, *args):
        super().__init__(*args)

    def getBenjaminGrahamPrice(self):
        EPS = self.getEPS().get(self.latestYear)
        growthRate = self.getGrowthRatebyPRATModel().get(str(int(self.latestYear)+1))
        treasuriesYield = self.getTreasuriesYield().get(self.latestYear)
        return pd.Series(np.divide(EPS*(growthRate*100+7)*4.4, self.getTreasuriesYield()*100), index=[self.latestYear])

    def setBenjaminGrahamPrice(self):
        output = self.getBenjaminGrahamPrice()
        self.setOutput(
            0, self.colName["CBenjaminGraham"], output, self.latestYear)
        self.setOutput(
            1, self.colName["RBenjaminGraham"], output, self.latestYear)
        self.setOutput(
            2, self.colName["EBenjaminGraham"], output, self.latestYear)
