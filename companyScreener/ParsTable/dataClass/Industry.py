import pandas as pd
import config
from ParsTable.dataClass.Super import Super


class Industry(Super):
    def __init__(self, *args):
        thisYear = args[0].columns[0]
        Super.__init__(self, thisYear)
        self.colName = config.IndustryName
        self.combinedDF = args[0]
        self.priceDF = args[1][0]
        self.company = args[2]

    def getMarketCapitalization(self):
        return self.divide(self.getPrice()*self.getShares(), 1e6)

    def setMarketCapitalization(self):
        output = self.getMarketCapitalization()
        self.setOutput(
            0, self.colName["marketCapitalization"], output, self.latestYear)
