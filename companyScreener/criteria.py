import numpy as np
import config

criteria = dict(
    ShareHolder=[
        {
            "name": "dividendYield level",
            "mode": ["valueInvestment"],
            "data": {
                "pars": [config.ShareHolderName["dividendYield"]],
                "condition":{},
                "criteria": {
                    "5": [0.39, np.inf],
                    "4":[0.29, 0.39],
                    "3":[0.19, 0.29],
                    "2":[0.1, 0.19],
                    "1":[0, 0.1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "payoutRatio level",
            "mode": ["valueInvestment", "growthInvestment"],
            "data": {
                "pars": [config.ShareHolderName["payoutRatio"]],
                "condition":{},
                "criteria": {
                    "5": [0, 0.20],
                    "4":[0.20, 0.40],
                    "3":[0.40, 0.60],
                    "2":[0.60, 0.80],
                    "1":[0.80, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "fiveYearAverageDividendGrowth level",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.ShareHolderName["fiveYearAverageDividendGrowth"]],
                "condition": {
                    "pars": [config.ShareHolderName["dividendYield"]],
                    "criteriaLevel": {
                        "lowYield": [0.04, np.inf],
                        "midYield":[0.02, 0.04],
                        "highYield":[0, 0.02],
                        "0": [-np.inf, 0],
                    }
                },
                "criteria": {
                    "lowYield": {
                        "5": [0.15, np.inf],
                        "4":[0.12, 0.15],
                        "3":[0.09, 0.12],
                        "2":[0.05, 0.09],
                        "1":[0, 0.05],
                        "0": [-np.inf, 0],
                    }, "midYield": {
                        "5": [0.12, np.inf],
                        "4":[0.09, 0.12],
                        "3":[0.05, 0.09],
                        "2":[0.02, 0.05],
                        "1":[0, 0.02],
                        "0": [-np.inf, 0],
                    }, "highYield": {
                        "5": [0.08, np.inf],
                        "4":[0.05, 0.08],
                        "3":[0.02, 0.05],
                        "2":[0.01, 0.02],
                        "1":[0, 0.01],
                        "0": [-np.inf, 0],
                    }, "0":{
                        "0": [-np.inf, np.inf],
                    }

                },
            }
        },
        {
            "name": "dividend stability",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [
                    config.ShareHolderName["fiveYearAverageDividendGrowth"],
                    config.ShareHolderName["maxDividendinFiveYears"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                },
            }
        }
    ], Profit=[
        {
            "name": "ROE Level",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.ProfitName["ROE"]],
                "condition":{},
                "criteria": {
                    "5": [0.30, np.inf],
                    "4":[0.18, 0.30],
                    "3":[0.10, 0.18],
                    "2":[0.01, 0.10],
                    "1":[0, 0.01],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "ROE(N) = Max(ROE)",
            "mode": ["growthInvestment"],
            "data":{
                "pars": [config.ProfitName["ROE"],
                         config.ProfitName["maxROEinFourYears"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "ROA/ROE>80%",
            "mode": ["valueInvestment", "growthInvestment"],
            "data":{
                "pars": [config.ProfitName["ROA"],
                         config.ProfitName["ROE"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "ROA>0%",
            "mode": ["growthInvestment"],
            "data":{
                "pars": [config.ProfitName["ROA"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "ROE>15% in 5 years",
            "mode": ["growthInvestment"],
            "data":{
                "pars": [config.ProfitName["yearPercentageOfHighROE"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Gross Margin Level",
            "mode": ["valueInvestment", "growthInvestment"],
            "data":{
                "pars": [config.GrowthName["grossMargin"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Operating Margin Level",
            "mode": ["valueInvestment", "growthInvestment"],
            "data":{
                "pars": [config.ProfitName["operatingMargin"]],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "ROE stability",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [
                    config.ProfitName["minROEinFouryears"],
                    config.ProfitName["maxROEinFourYears"],
                ],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Continually Free Cash Flow",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [
                    config.SafetyName["yearPercentageOfPositiveFreeCashFlow"],
                ],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "FCF/OCF",
            "mode": ["valueInvestment", "growthInvestment"],
            "data":{
                "pars": [
                    config.SafetyName["freeCashFlow"],
                    config.ProfitName["operatingCashFlow"],
                ],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
    ], Growth=[
        {
            "name": "RR>0",
            "mode": ["growthInvestment"],
            "data":{
                "pars": [
                    config.GrowthName["reinvestmentRate"],
                ],
                "condition":{},
                "criteria": {
                    "5": [0.5, 1],
                    "4":[0.3, 0.5],
                    "3":[0.2, 0.3],
                    "2":[0.1, 0.2],
                    "1":[0, 0.1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Operating Income Growth %",
            "mode": ["valueInvestment", "growthInvestment"],
            "data":{
                "pars": [
                    config.GrowthName["operatingIncomeGrowth"],
                ],
                "condition":{},
                "criteria": {
                    "5": [1, np.inf],
                    "4":[0.75, 1],
                    "3":[0.5, 0.75],
                    "2":[0.15, 0.5],
                    "1":[0, 0.15],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Operating Income Growth % > 15% in 3 years",
            "mode": ["growthInvestment"],
            "data":{
                "pars": [
                    config.GrowthName["yearPercentageOfOperatingIncomeGrowth"],
                ],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "total revenue % is positive in 3 years",
            "mode": ["growthInvestment"],
            "data":{
                "pars": [
                    config.GrowthName["yearPercentageOfOperatingIncomeGrowth"],
                ],
                "condition":{},
                "criteria": {
                    "5": [0.8, 1],
                    "4":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "2":[0.2, 0.4],
                    "1":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
    ], Safety=[
        {
            "name": "D/E Ratio Level",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [
                    config.SafetyName["debtEquityRatio"],
                ],
                "condition":{},
                "criteria": {
                    "1": [0.8, 1],
                    "2":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "4":[0.2, 0.4],
                    "5":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "D/C Ratio level",
            "mode": ["valueInvestment", "growthInvestment"],
            "data":{
                "pars": [
                    config.SafetyName["debtCapitalRatio"],
                ],
                "condition":{},
                "criteria": {
                    "1": [0.8, 1],
                    "2":[0.6, 0.8],
                    "3":[0.4, 0.6],
                    "4":[0.2, 0.4],
                    "5":[0, 0.2],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Quick Ratio level",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [
                    config.SafetyName["quickRatio"],
                ],
                "condition":{},
                "criteria": {
                    "5": [1, np.inf],
                    "4":[0.75, 1],
                    "3":[0.5, 0.75],
                    "2":[0.15, 0.5],
                    "1":[0, 0.15],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Dividends / FCF Ratio",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [
                    config.SafetyName["totalDividendsFCFRatio"],
                ],
                "condition":{},
                "criteria": {
                    "5": [1.6, 2],
                    "4":[1.2, 1.6],
                    "3":[0.8, 1.2],
                    "2":[0.4, 0.8],
                    "1":[0, 0.4],
                    "0": [-np.inf, 0],
                }
            }
        },
    ], FScore=[
        {
            "name": "ROA>0",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.ProfitName["ROA"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "OCF>0",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.ProfitName["operatingCashFlow"]],
                "condition":{},
                "criteria": {
                    "1": [0, np.inf],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "OCF>Net Income",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.ProfitName["netIncome"],
                         config.ProfitName["operatingCashFlow"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "ROTA(N) > ROTA(N-1)",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.GrowthName["ROTAn1"],
                         config.GrowthName["ROTA"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Asset Turnover Ratio(N) >Asset Turnover Ratio(N-1)",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.GrowthName["assetTurnoverRation1"],
                         config.GrowthName["assetTurnoverRatio"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Gross Margin(N) > Gross Margin(N-1)",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.GrowthName["grossMarginn1"],
                         config.GrowthName["grossMargin"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Long-Term Debt(N)<Long-Term Debt(N-1)",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.SafetyName["longTermDebt"],
                         config.SafetyName["longTermDebtn1"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Shares(N)<Shares(N-1)",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.SafetyName["shareCapital"],
                         config.SafetyName["shareCapitaln1"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
        {
            "name": "Current Ratio(N) > Current Ratio(N-1)",
            "mode": ["valueInvestment"],
            "data":{
                "pars": [config.SafetyName["currentRation1"],
                         config.SafetyName["currentRatio"]],
                "condition":{},
                "criteria": {
                    "1": [0, 1],
                    "0": [-np.inf, 0],
                }
            }
        },
    ],
)
