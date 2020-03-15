from FinanceClass import Finance


def createValueInvestment(combinedDF, priceDF, company):
    financeInstance = Finance(combinedDF, priceDF, company)
    financeInstance.getDividend()
    return financeInstance.getOutput()
