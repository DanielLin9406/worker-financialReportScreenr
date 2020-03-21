import config
import pandas as pd
import numpy as np
import copy

# def getCriteriaList():
#     return config.checkValueInvestment()


def gt(para1, para2, criteria):
    if para2 is not None:
        return para1.div(para2).gt(criteria)
    else:
        return para1.gt(criteria)


def lt(para1, para2, criteria):
    if para2 is not None:
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
    function = switch.get(copy.deepcopy(condition["operator"]).pop())
    para1 = parasTable.get(condition["name"])
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


def countTrue(countTrueDF, company, listName):
    trueNumber = {}
    total = {}
    ratioPars = {}
    result = pd.DataFrame()
    df = pd.concat(countTrueDF, axis=0)
    for index in df.axes[1].values:
        trueNumber[index] = np.sum(
            df.get(index).dropna().convert_dtypes(convert_boolean=True))
        total[index] = len(df.get(index).dropna())
        ratioPars[index] = '/'.join([str(trueNumber[index]),
                                     str(total[index])])
        result.at[company, '-'.join([listName, str(index)])] = ratioPars[index]
    return result


def loopConfig(parasTable, company, listName):
    resultDF = pd.DataFrame()
    countTrueDFList = []
    for test in config.criteria[listName]:
        boolean = checkCriteria(parasTable, company, test)
        resultDF.at[company, test["name"]] = boolean
        countTrueDFList.append(pd.DataFrame(
            [[boolean]*len(test["mode"])], index=[test["name"]], columns=test["mode"], dtype="boolean"))

    return {"DF": resultDF, "TrueNum": countTrue(countTrueDFList, company, listName)}


def analyzeData(parasTable, company):
    ShareHolder = loopConfig(parasTable, company, "ShareHolder")
    FScore = loopConfig(parasTable, company, "FScore")
    Profit = loopConfig(parasTable, company, "Profit")
    Growth = loopConfig(parasTable, company, "Growth")
    Safety = loopConfig(parasTable, company, "Safety")
    return pd.concat([ShareHolder["DF"], FScore["DF"], Profit["DF"], Growth["DF"], Safety["DF"], FScore["TrueNum"], ShareHolder["TrueNum"],
                      Profit["TrueNum"], Growth["TrueNum"], Safety["TrueNum"]], axis=1)
