import config
import pandas as pd


def createBuyDecisionTable(priceTable, analyzedTable, company):
    result = pd.DataFrame()
    stockPriceName = config.BuyDecisionTable["stockPrice"]
    finalScoreName = config.BuyDecisionTable['finalScore']
    investmentName = config.BuyDecisionTable["investmentType"]
    discountPremiumName = config.BuyDecisionTable["DiscountPremiumOfFCFE"]
    result.at[company, stockPriceName] = priceTable.get(
        stockPriceName).loc[company]
    result.at[company, finalScoreName] = analyzedTable.get(
        finalScoreName).loc[company]
    result.at[company, investmentName] = analyzedTable.get(
        investmentName).loc[company]
    result.at[company, discountPremiumName] = priceTable.get(
        discountPremiumName).loc[company]
    return result
