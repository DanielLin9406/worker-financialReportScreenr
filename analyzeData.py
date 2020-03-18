import config
import pandas as pd
import numpy as np

# def getCriteriaList():
#     return config.checkValueInvestment()


def gt(para1, para2, criteria):
    if para2 is not None:
        return para1.div(para2).gt(criteria)
    else:
        return para1.gt(criteria)


def lt(para1, para2, criteria):
    if para2 is not None:
        print(para1)
        print(para2)
        return para1.div(para2).lt(criteria)
    else:
        return para1.lt(criteria)


def eq(para1, para2, criteria):
    if para2 is not None:
        return para1.div(para2).eq(criteria)
    else:
        return para1.eq(criteria)


def criteriaSwitcher(condition, parasTable, company):
    switch = {
        "gt": gt,
        "lt": lt,
        "eq": eq
    }

    function = switch.get(condition["operator"].pop())
    para1 = parasTable.get(condition["name"])
    print(para1)
    print(condition["name"])
    criteria = pd.Series([condition["criteria"]], index=[
                         company])
    if "name2" in condition:
        para2 = parasTable.get(condition["name2"])
    else:
        para2 = None

    return function(para1, para2, criteria).get(company)


def checkCriteria(parasTable, company, test):
    # Test
    #   {
    #     "name": "dividendYield>2%",
    #     "mode": "valueInvestment",
    #     "data": [{"name": thisModule.ShareHolderName["dividendYield"],
    #               "criteria": "2%", "operator":"gt"}]
    #   }
    result = []
    for condition in test["data"]:
        result.append(criteriaSwitcher(
            condition, parasTable, company))
    return all(ele == True for ele in result)


def loopConfig(parasTable, company, listName):
    result = pd.DataFrame()
    for test in config.criteria[listName]:
        result.at[company, test["name"]] = checkCriteria(
            parasTable, company, test)
    return result


def analyzeData(parasTable, company):
    return pd.concat([loopConfig(parasTable, company, "ShareHolder"), loopConfig(parasTable, company, "FScore"), loopConfig(parasTable, company, "Profit"), loopConfig(parasTable, company, "Growth"), loopConfig(parasTable, company, "Safety")], axis=1)
