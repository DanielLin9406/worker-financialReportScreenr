import criteria as criteriaSetting
import pandas as pd
import numpy as np
import copy


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
        result.append(criteriaSwitcher(condition, parasTable, company))
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
        ratioPars[index] = np.divide(trueNumber[index], total[index])
        result.at[company, '-'.join([listName, str(index)])] = ratioPars[index]
    return result


def isValueInThisPeriod(lowerBond, value, upperBond):
    # print('lowerBond', lowerBond)
    # print('value', value)
    # print('upperBond', upperBond)
    if ((lowerBond < value) and (value < upperBond or upperBond == value)):
        return True
    else:
        return False


def getKeyFromValueArr(value, Dict):
    # Low level method for getting key
    if Dict != 0:
        for key, valueArr in Dict.items():
            if (valueArr[0] > valueArr[1]):
                if isValueInThisPeriod(valueArr[1], value, valueArr[0]):
                    return key
            elif (valueArr[0] < valueArr[1]):
                if (isValueInThisPeriod(valueArr[0], value, valueArr[1])):
                    return key
        return '0'
    else:
        return '0'


def getCriteriaLevel(par, criteriaLevelDict):
    return getKeyFromValueArr(par, criteriaLevelDict)


def getScore(par, criteriaDict):
    return getKeyFromValueArr(par, criteriaDict)


def getPars(parsList, parasTable):
    result = 0
    if len(parsList) == 2:
        result = np.divide(parasTable.get(
            parsList[0]).iloc[0], parasTable.get(parsList[1]).iloc[0])
    else:
        result = parasTable.get(parsList[0]).iloc[0]
    return result


def checkScoreCriteria(parasTable, company, test):
    #     { "name": "dividendYield>2%",
    #     "mode": ["valueInvestment"],
    #     "data":{
    #         "pars": [thisModule.ShareHolderName["dividendYield"]],
    #         "condition": {
    #             "pars": [config.ShareHolderName["dividendYield"]],
    #             "criteriaLevel": {
    #                 "lowYield": [0.04, np.inf],
    #                 "midYield":[0.02, 0.04],
    #                 "highYield":[0, 0.02],
    #                 "0": [-np.inf, 0],
    #             }
    #         },
    #         "criteria": {
    #             "lowYield": {
    #                 "5": [0.15, np.inf],
    #                 "4":[0.12, 0.15],
    #                 "3":[0.09, 0.12],
    #                 "2":[0.05, 0.09],
    #                 "1":[0, 0.05],
    #                 "0": [-np.inf, 0],
    #             }, "midYield": {
    #                 "5": [0.12, np.inf],
    #                 "4":[0.09, 0.12],
    #                 "3":[0.05, 0.09],
    #                 "2":[0.02, 0.05],
    #                 "1":[0, 0.02],
    #                 "0": [-np.inf, 0],
    #             }, "highYield": {
    #                 "5": [0.08, np.inf],
    #                 "4":[0.05, 0.08],
    #                 "3":[0.02, 0.05],
    #                 "2":[0.01, 0.02],
    #                 "1":[0, 0.01],
    #                 "0": [-np.inf, 0],
    #             },
    #         },
    #     }
    # },
    data = test['data']
    par = getPars(data['pars'], parasTable)
    if 'criteriaLevel' in data['condition']:
        criteriaLevelDict = data['condition']["criteriaLevel"]
        conditionPar = getPars(data['condition']['pars'], parasTable)
        criteriaName = getCriteriaLevel(conditionPar, criteriaLevelDict)
        score = getScore(par, data['criteria'][criteriaName])
    else:
        score = getScore(par, data['criteria'])

    return int(score)


def countScore(countTrueDF, company, listName):
    trueNumber = {}
    total = {}
    ratioPars = {}
    result = pd.DataFrame()
    if listName == 'FScore':
        multiply = 1
    else:
        multiply = 5
    df = pd.concat(countTrueDF, axis=0)
    for index in df.axes[1].sort_values().values:
        trueNumber[index] = np.sum(
            df.get(index).dropna())
        total[index] = len(df.get(index).dropna())*multiply
        result.at[company,
                  '-'.join([listName, str(index), 'Score'])] = trueNumber[index]
        result.at[company,
                  '-'.join([listName, str(index), 'Full Credits'])] = total[index]
    return result


def loopConfig(parasTable, company, listName):
    # resultDF = pd.DataFrame(dtype="boolean")
    ScoreDF = pd.DataFrame(dtype="float64")
    # countTrueDFList = []
    countScoreDFList = []
    # for test in config.criteria[listName]:
    #     boolean = checkCriteria(parasTable, company, test)
    #     resultDF.at[company, test["name"]] = boolean
    #     countTrueDFList.append(pd.DataFrame(
    #         [[boolean]*len(test["mode"])], index=[test["name"]], columns=test["mode"], dtype="boolean"))

    for test in criteriaSetting.criteria[listName]:
        score = checkScoreCriteria(parasTable, company, test)
        ScoreDF.at[company, test["name"]] = score
        countScoreDFList.append(pd.DataFrame(
            [[score]*len(test["mode"])], index=[test["name"]], columns=test["mode"], dtype="float64"))

    countScoreDF = countScore(countScoreDFList, company, listName)
    return {
        "Score": ScoreDF,
        "CountScore": countScoreDF,
        # "TrueNum": countTrue(countTrueDFList, company, listName),
    }


def summarizeScore(countScoreDF, company):
    result = pd.DataFrame()
    valueScoreDF = countScoreDF.filter(
        regex='valueInvestment-Score').iloc[0]
    valueFullCreditsDF = countScoreDF.filter(
        regex='valueInvestment-Full Credits').iloc[0]
    growthScoreDF = countScoreDF.filter(
        regex='growthInvestment-Score').iloc[0]
    growthFullCreditsDF = countScoreDF.filter(
        regex='growthInvestment-Full Credits').iloc[0]
    # print(growthFullCreditsDF)
    valueSum = np.sum(valueScoreDF.dropna())
    valueFullCredits = np.sum(valueFullCreditsDF.dropna())
    growthSum = np.sum(growthScoreDF.dropna())
    growthFullCredits = np.sum(growthFullCreditsDF.dropna())
    value = np.divide(valueSum, valueFullCredits)
    growth = np.divide(growthSum, growthFullCredits)
    invesementType = ''
    finalScore = ''

    if (value > growth):
        invesementType = 'Value'
        finalScore = valueSum
    elif value < growth:
        invesementType = 'Growth'
        finalScore = growthSum

    result.at[company, 'sum-growthInvestment'] = growthSum
    result.at[company, 'fullCredits-growthInvestment'] = growthFullCredits
    result.at[company, 'sum-valueInvestment'] = valueSum
    result.at[company, 'fullCredits-valueInvestment'] = valueFullCredits
    result.at[company, 'Investment Type'] = invesementType
    result.at[company, 'Final Score'] = finalScore

    return result


def analyzeData(parasTable, company):
    ShareHolder = loopConfig(parasTable, company, "ShareHolder")
    FScore = loopConfig(parasTable, company, "FScore")
    Profit = loopConfig(parasTable, company, "Profit")
    Growth = loopConfig(parasTable, company, "Growth")
    Safety = loopConfig(parasTable, company, "Safety")
    countScoreDF = pd.concat([FScore["CountScore"],
                              ShareHolder["CountScore"],
                              Profit["CountScore"],
                              Growth["CountScore"],
                              Safety["CountScore"]], axis=1)
    summarizedScoreDF = summarizeScore(countScoreDF, company)

    return pd.concat([ShareHolder["Score"],  Profit["Score"], Growth["Score"], Safety["Score"], FScore["Score"],
                      countScoreDF, summarizedScoreDF], axis=1)
