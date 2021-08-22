import copy
import numpy as np
import pandas as pd
from abc import ABC, abstractmethod, abstractproperty
import Config.config as config
import Config.criteria as criteriaSetting


# # def gt(para1, para2, criteria):
# #     if para2 is not None:
# #         return para1.div(para2).gt(criteria)
# #     else:
# #         return para1.gt(criteria)


# # def lt(para1, para2, criteria):
# #     if para2 is not None:
# #         return para1.div(para2).lt(criteria)
# #     else:
# #         return para1.lt(criteria)


# # def eq(para1, para2, criteria):
# #     if para2 is not None:
# #         return para1.div(para2).eq(criteria)
# #     else:
# #         return para1.eq(criteria)


# # def criteriaSwitcher(condition, parsTable, company):
# #     switch = {
# #         "gt": gt,
# #         "lt": lt,
# #         "eq": eq
# #     }
# #     function = switch.get(copy.deepcopy(condition["operator"]).pop())
# #     para1 = parsTable.get(condition["name"])
# #     criteria = pd.Series([condition["criteria"]], index=[
# #                          company])
# #     if "name2" in condition:
# #         para2 = parsTable.get(condition["name2"])
# #     else:
# #         para2 = None

# #     return function(para1, para2, criteria).get(company)


# # def checkCriteria(parsTable, company, test):
# #     # Test
# #     #   {
# #     #     "name": "dividendYield>2%",
# #     #     "mode": "valueInvestment",
# #     #     "data": [{"name": thisModule.ShareHolderName["dividendYield"],
# #     #               "criteria": "2%", "operator":"gt"}]
# #     #   }
# #     result = []
# #     for condition in test["data"]:
# #         result.append(criteriaSwitcher(condition, parsTable, company))
# #     return all(ele == True for ele in result)


# # def countTrue(countTrueDF, company, listName):
# #     trueNumber = {}
# #     total = {}
# #     ratioPars = {}
# #     result = pd.DataFrame()
# #     df = pd.concat(countTrueDF, axis=0)
# #     for index in df.axes[1].values:
# #         trueNumber[index] = np.sum(
# #             df.get(index).dropna().convert_dtypes(convert_boolean=True))
# #         total[index] = len(df.get(index).dropna())
# #         ratioPars[index] = np.divide(trueNumber[index], total[index])
# #         result.at[company, '-'.join([listName, str(index)])] = ratioPars[index]
# #     return result


# def isValueInThisPeriod(lowerBond, value, upperBond):
#     if ((lowerBond < value) and (value < upperBond or upperBond == value)):
#         return True
#     else:
#         return False


# def getKeyFromValueArr(value, Dict):
#     # Low level method for getting key
#     if Dict != 0:
#         for key, valueArr in Dict.items():
#             if (valueArr[0] > valueArr[1]):
#                 if isValueInThisPeriod(valueArr[1], value, valueArr[0]):
#                     return key
#             elif (valueArr[0] < valueArr[1]):
#                 if (isValueInThisPeriod(valueArr[0], value, valueArr[1])):
#                     return key
#         return '0'
#     else:
#         return '0'


# def getCriteriaLevel(par, criteriaLevelDict):
#     return getKeyFromValueArr(par, criteriaLevelDict)


# def getScore(par, criteriaDict):
#     return getKeyFromValueArr(par, criteriaDict)


# def getPars(parsList, parsTable):
#     result = 0
#     if len(parsList) == 2:
#         result = np.divide(parsTable.get(
#             parsList[0]).iloc[0], parsTable.get(parsList[1]).iloc[0])
#     else:
#         result = parsTable.get(parsList[0]).iloc[0]
#     return result


# def checkScoreCriteria(parsTable, company, test):
#     #     { "name": "dividendYield>2%",
#     #     "mode": ["valueInvestment"],
#     #     "data":{
#     #         "pars": [thisModule.ShareHolderName["dividendYield"]],
#     #         "condition": {
#     #             "pars": [config.ShareHolderName["dividendYield"]],
#     #             "criteriaLevel": {
#     #                 "lowYield": [0.04, np.inf],
#     #                 "midYield":[0.02, 0.04],
#     #                 "highYield":[0, 0.02],
#     #                 "0": [-np.inf, 0],
#     #             }
#     #         },
#     #         "criteria": {
#     #             "lowYield": {
#     #                 "5": [0.15, np.inf],
#     #                 "4":[0.12, 0.15],
#     #                 "3":[0.09, 0.12],
#     #                 "2":[0.05, 0.09],
#     #                 "1":[0, 0.05],
#     #                 "0": [-np.inf, 0],
#     #             }, "midYield": {
#     #                 "5": [0.12, np.inf],
#     #                 "4":[0.09, 0.12],
#     #                 "3":[0.05, 0.09],
#     #                 "2":[0.02, 0.05],
#     #                 "1":[0, 0.02],
#     #                 "0": [-np.inf, 0],
#     #             }, "highYield": {
#     #                 "5": [0.08, np.inf],
#     #                 "4":[0.05, 0.08],
#     #                 "3":[0.02, 0.05],
#     #                 "2":[0.01, 0.02],
#     #                 "1":[0, 0.01],
#     #                 "0": [-np.inf, 0],
#     #             },
#     #         },
#     #     }
#     # },
#     data = test['data']
#     par = getPars(data['pars'], parsTable)
#     if 'criteriaLevel' in data['condition']:
#         criteriaLevelDict = data['condition']["criteriaLevel"]
#         conditionPar = getPars(data['condition']['pars'], parsTable)
#         criteriaName = getCriteriaLevel(conditionPar, criteriaLevelDict)
#         score = getScore(par, data['criteria'][criteriaName])
#     else:
#         score = getScore(par, data['criteria'])

#     return int(score)


# def countScore(countTrueDFList, company, listName):
#     trueNumber = {}
#     total = {}
#     ratioPars = {}
#     result = pd.DataFrame()
#     if listName == 'FScore':
#         multiply = 1
#     else:
#         multiply = 5
#     df = pd.concat(countTrueDFList, axis=0)
#     for index in df.axes[1].sort_values().values:
#         trueNumber[index] = np.sum(
#             df.get(index).dropna())
#         total[index] = len(df.get(index).dropna())*multiply
#         result.at[company,
#                   '-'.join([listName, str(index), 'Score'])] = trueNumber[index]
#         result.at[company,
#                   '-'.join([listName, str(index), 'Full Credits'])] = total[index]
#     return result


# def getSumAndFullCredits(countScoreDF, company):
#     valueScoreDF = countScoreDF.filter(regex='valueInvestment-Score').iloc[0]
#     valueFullCreditsDF = countScoreDF.filter(
#         regex='valueInvestment-Full Credits').iloc[0]
#     growthScoreDF = countScoreDF.filter(regex='growthInvestment-Score').iloc[0]
#     growthFullCreditsDF = countScoreDF.filter(
#         regex='growthInvestment-Full Credits').iloc[0]

#     valueSum = np.sum(valueScoreDF.dropna())
#     valueFullCredits = np.sum(valueFullCreditsDF.dropna())
#     growthSum = np.sum(growthScoreDF.dropna())
#     growthFullCredits = np.sum(growthFullCreditsDF.dropna())

#     value = np.divide(valueSum, valueFullCredits)
#     growth = np.divide(growthSum, growthFullCredits)

#     invesementType = ''
#     finalScore = ''

#     if (value > growth):
#         invesementType = 'Value'
#         finalScore = valueSum
#     elif value < growth:
#         invesementType = 'Growth'
#         finalScore = growthSum
#     return {
#         'valueSum': valueSum,
#         'growthSum': growthSum,
#         'growthFullCredits': growthFullCredits,
#         'valueFullCredits': valueFullCredits,
#         'invesementType': invesementType,
#         'finalScore': finalScore
#     }


# def summarizeScore(countScoreDF, company):
#     result = pd.DataFrame()
#     sumAndFullCreditsDict = getSumAndFullCredits(countScoreDF, company)

#     result.at[company, config.AnalyzeName['sumGrowthInvestment']
#               ] = sumAndFullCreditsDict['growthSum']
#     result.at[company, config.AnalyzeName['fullCreditsGrowthInvestment']
#               ] = sumAndFullCreditsDict['growthFullCredits']
#     result.at[company, config.AnalyzeName['sumValueInvestment']
#               ] = sumAndFullCreditsDict['valueSum']
#     result.at[company, config.AnalyzeName['fullCreditsValueInvestment']
#               ] = sumAndFullCreditsDict['valueFullCredits']
#     result.at[company, config.AnalyzeName['investmentType']
#               ] = sumAndFullCreditsDict['invesementType']
#     result.at[company, config.AnalyzeName['finalScore']
#               ] = sumAndFullCreditsDict['finalScore']

#     return result


# def loopConfig(parsTable, company, listName):
#     # resultDF = pd.DataFrame(dtype="boolean")
#     # countTrueDFList = []
#     #
#     # for test in config.criteria[listName]:
#     #     boolean = checkCriteria(parsTable, company, test)
#     #     resultDF.at[company, test["name"]] = boolean
#     #     countTrueDFList.append(pd.DataFrame(
#     #         [[boolean]*len(test["mode"])], index=[test["name"]], columns=test["mode"], dtype="boolean"))

#     ScoreDF = pd.DataFrame(dtype="float64")
#     countScoreDFList = []

#     for test in criteriaSetting.criteria[listName]:
#         score = checkScoreCriteria(parsTable, company, test)
#         ScoreDF.at[company, test["name"]] = score
#         countScoreDFList.append(pd.DataFrame(
#             [[score]*len(test["mode"])], index=[test["name"]], columns=test["mode"], dtype="float64"))

#     countScoreDF = countScore(countScoreDFList, company, listName)
#     return {
#         "Score": ScoreDF,
#         "CountScore": countScoreDF,
#         # "TrueNum": countTrue(countTrueDFList, company, listName),
#     }


# def createAnalyzeTable(parsTable, company):
#     ShareHolder = loopConfig(parsTable, company, "ShareHolder")
#     Profit = loopConfig(parsTable, company, "Profit")
#     Growth = loopConfig(parsTable, company, "Growth")
#     Safety = loopConfig(parsTable, company, "Safety")
#     FScore = loopConfig(parsTable, company, "FScore")
#     countScoreDF = pd.concat([ShareHolder["CountScore"],
#                               Profit["CountScore"],
#                               Growth["CountScore"],
#                               Safety["CountScore"],
#                               FScore["CountScore"], ], axis=1)
#     summarizedScoreDF = summarizeScore(countScoreDF, company)

#     return pd.concat([ShareHolder["Score"],  Profit["Score"], Growth["Score"], Safety["Score"], FScore["Score"],
#                       countScoreDF, summarizedScoreDF], axis=1)


class CalculateScoreStrategy:
    def __init__(self):
        self._resultDF = pd.DataFrame(dtype="float64")
        self._scoreDFList = []

    def isValueInThisPeriod(self, lowerBond, value, upperBond):
        if ((lowerBond < value) and (value < upperBond or upperBond == value)):
            return True
        else:
            return False

    def getKeyFromValueArr(self, value, Dict):
        # Low level method for getting key
        if Dict != 0:
            for key, valueArr in Dict.items():
                if (valueArr[0] > valueArr[1]):
                    if self.isValueInThisPeriod(valueArr[1], value, valueArr[0]):
                        return key
                elif (valueArr[0] < valueArr[1]):
                    if (self.isValueInThisPeriod(valueArr[0], value, valueArr[1])):
                        return key
            return '0'
        else:
            return '0'

    def getScore(self, par, criteriaDict):
        return self.getKeyFromValueArr(par, criteriaDict)

    def getPars(self, parsList, parsTable):
        result = 0
        if len(parsList) == 2:
            result = np.divide(parsTable.get(
                parsList[0]).iloc[0], parsTable.get(parsList[1]).iloc[0])
        else:
            result = parsTable.get(parsList[0]).iloc[0]
        return result

    def getScoreWithCondition(self, par, data, parsTable):
        criteriaLevelDict = data['condition']["criteriaLevel"]
        conditionPar = self.getPars(data['condition']['pars'], parsTable)
        criteriaName = self.getScore(conditionPar, criteriaLevelDict)
        return self.getScore(par, data['criteria'][criteriaName])

    def getScoreWrapper(self, company, test, parsTable):
        data = test['data']
        parsList = data['pars']
        par = self.getPars(parsList, parsTable)
        if 'criteriaLevel' in data['condition']:
            return self.getScoreWithCondition(par, data, parsTable)
        else:
            return self.getScore(par, data['criteria'])

    def setScoreDF(self, company, test, score):
        name = test["name"]
        self._resultDF.at[company, name] = score

    def getScoreDFList(self):
        return self._scoreDFList

    def setScoreDFList(self, test, score):
        self._scoreDFList.append(pd.DataFrame(
            [[score]*len(test["mode"])],
            index=[test["name"]],
            columns=test["mode"],
            dtype="float64"))

    @property
    def doAlgorithm(self):
        return self._resultDF

    @doAlgorithm.setter
    def doAlgorithm(self, kwargs):
        listName = kwargs.get('listName')
        company = kwargs.get('company')
        parsTable = kwargs.get('parsTable')
        for test in criteriaSetting.criteria[listName]:
            score = int(self.getScoreWrapper(company, test, parsTable))
            self.setScoreDF(company, test, score)
            self.setScoreDFList(test, score)


class CountScoreStrategy:
    def __init__(self):
        self._resultDF = pd.DataFrame()

    def getSumScore(self, df, index):
        return np.sum(df.get(index).dropna())

    def getMultiply(self, listName):
        if listName == 'FScore':
            return 1
        else:
            return 5

    def getFullScore(self, df, index, listName):
        multiply = self.getMultiply(listName)
        return len(df.get(index).dropna())*multiply

    def setCountScoreDF(self, company, listName, sumScore, fullScore, index):
        self._resultDF.at[company,
                          '-'.join([listName, str(index), 'Score'])] = sumScore[index]
        self._resultDF.at[company,
                          '-'.join([listName, str(index), 'Full Credits'])] = fullScore[index]

    @property
    def doAlgorithm(self):
        return self._resultDF

    @doAlgorithm.setter
    def doAlgorithm(self, kwargs):
        listName = kwargs.get('listName')
        company = kwargs.get('company')
        countScoreDFList = kwargs.get('countScoreDFList')
        sumScore = {}
        fullScore = {}
        df = pd.concat(countScoreDFList, axis=0)
        for index in df.axes[1].sort_values().values:
            sumScore[index] = self.getSumScore(df, index)
            fullScore[index] = self.getFullScore(df, index, listName)
            self.setCountScoreDF(company, listName, sumScore, fullScore, index)


class SummarizeScoreStrategy:
    def __init__(self):
        self._resultDF = pd.DataFrame()

    def getSumAndFullCredits(self, countScoreDF):
        valueScoreDF = countScoreDF.filter(
            regex='valueInvestment-Score').iloc[0]
        valueFullCreditsDF = countScoreDF.filter(
            regex='valueInvestment-Full Credits').iloc[0]
        growthScoreDF = countScoreDF.filter(
            regex='growthInvestment-Score').iloc[0]
        growthFullCreditsDF = countScoreDF.filter(
            regex='growthInvestment-Full Credits').iloc[0]

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
        return {
            'valueSum': valueSum,
            'growthSum': growthSum,
            'growthFullCredits': growthFullCredits,
            'valueFullCredits': valueFullCredits,
            'invesementType': invesementType,
            'finalScore': finalScore
        }

    def setSummarizeScoreDF(self, company, countScoreDF):
        infoDict = self.getSumAndFullCredits(countScoreDF)
        self._resultDF.at[company, config.AnalyzeName['sumGrowthInvestment']
                          ] = infoDict['growthSum']
        self._resultDF.at[company, config.AnalyzeName['fullCreditsGrowthInvestment']
                          ] = infoDict['growthFullCredits']
        self._resultDF.at[company, config.AnalyzeName['sumValueInvestment']
                          ] = infoDict['valueSum']
        self._resultDF.at[company, config.AnalyzeName['fullCreditsValueInvestment']
                          ] = infoDict['valueFullCredits']
        self._resultDF.at[company, config.AnalyzeName['investmentType']
                          ] = infoDict['invesementType']
        self._resultDF.at[company, config.AnalyzeName['finalScore']
                          ] = infoDict['finalScore']

    @property
    def doAlgorithm(self):
        return self._resultDF

    @doAlgorithm.setter
    def doAlgorithm(self, kwargs):
        company = kwargs.get('company')
        summarizedScoreList = kwargs.get('summarizedScoreList')
        countScoreDF = pd.concat(summarizedScoreList, axis=1)
        self.setSummarizeScoreDF(company, countScoreDF)


def createCriteriaScoreDF(**kwargs):
    context = kwargs.get('context')
    context.company = kwargs.get('company')
    context.parsTable = kwargs.get('parsTable')
    context.listName = kwargs.get('listName')

    """
    @param: DataFrame
    @return: DataFrame
    """
    strategy = CalculateScoreStrategy()
    countScoreDFList = strategy.getScoreDFList()
    context.strategy = strategy
    scoreDF = context.doScoreAlgorithm()

    """
    @param: DataFrame List
    @return: DataFrame
    """
    context.countScoreDFList = countScoreDFList
    context.strategy = CountScoreStrategy()
    countScoreDF = context.doCountScoreAlgorithm()

    return {
        "Score": scoreDF,
        "CountScore": countScoreDF
    }


def createSummarizedScore(**kwargs):
    """
    @param: DataFrame List
    @return: DataFrame
    """
    context = kwargs.get('context')
    context.company = kwargs.get('company')
    context.summarizedScoreList = kwargs.get('summarizedScoreList')
    context.strategy = SummarizeScoreStrategy()
    return context.doSummarizedAlgorithm()


def createScoreAndCountScore(**kwargs):
    result = dict(
        Score=[],
        CountScore=[]
    )
    for name in ["ShareHolder", "Profit", "Growth", "Safety", "FScore"]:
        scoreDict = createCriteriaScoreDF(**kwargs, **dict(listName=name))
        result['Score'].append(scoreDict["Score"])
        result['CountScore'].append(scoreDict["CountScore"])
    return result


def ScoreTable(**kwargs):
    resultDict = createScoreAndCountScore(**kwargs)

    summarizedScoreList = dict(summarizedScoreList=resultDict['CountScore'])
    summarizedScoreDF = createSummarizedScore(**kwargs, **summarizedScoreList)

    return pd.concat([*resultDict['Score'], *resultDict['CountScore'], summarizedScoreDF], axis=1)
