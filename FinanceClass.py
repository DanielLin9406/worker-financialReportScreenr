import pandas as pd
import numpy as np


class Finance:
    def __init__(self, *args):
        self.combinedDF = args[0]
        self.priceDF = args[1]
        self.company = args[2]
        self.output = pd.DataFrame(np.array([0.]), columns=[0])

    def getDividend(self):
        df = self.combinedDF
        company = self.company
        totalDividend = df.loc['Cash Dividends Paid']
        shares = df.loc['Common Shares Issued']
        Dividend = np.divide(-totalDividend, shares)

        self.output = self.output.rename(
            columns={0: "Divided"}, index=lambda x: company)
        self.output.at[company, "Divided"] = Dividend['2019']

    def getOutput(self):
        return self.output
