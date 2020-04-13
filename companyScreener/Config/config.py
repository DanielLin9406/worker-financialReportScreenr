import sys
import numpy as np
thisModule = sys.modules[__name__]

IndustryName = dict(
    sector="Sector",
    industry="Industry",
    marketCapitalization="Market Capitalization"
)

ShareHolderName = dict(
    dividend="Dividend",
    dividendn1="Dividend (N-1)",
    dividendn2="Dividend (N-2)",
    dividendGrowth="Dividend Growth",
    dividendGrowthn1="Dividend Growth (N-1)",
    dividendGrowthn2="Dividend Growth (N-2)",
    totalDividend="Total Dividend",
    fiveYearAverageDividend="5-year Average Dividend",
    maxDividendinFiveYears="Max Dividend in 5-years",
    minDividendinFiveYears="Min Dividend in 5-years",
    fiveYearAverageDividendGrowth="5-year Average Dividend Growth",
    dividendGrowthinThreeYear="Dividend Growth in 3 year",
    threeYearAverageDividendGrowth="3-year Average Dividend Growth",
    dividendYield="Dividend Yield",
    payoutRatio="Payout ratio",
)

ProfitName = dict(
    ROE="ROE",
    ROEn1="ROE(n-1)",
    ROEn2="ROE(n-2)",
    ROEn3="ROE(n-3)",
    fourYearAverageROE="4-year Average ROE",
    maxROEinFourYears="Max ROE in 4 years",
    minROEinFouryears="Min ROE in 4 years",
    yearPercentageOfHighROE="How many years Of high ROE in total data period",
    ROA="ROA",
    ROS="ROS",
    operatingMargin="Operating Margin",
    operatingCashFlow="Operating Cash Flow",
    netIncome="Net Income",
    EPS="EPS",
    EPSn1="EPS(n-1)",
    EPSn2="EPS(n-2)",
    EPSn3="EPS(n-3)",
)
GrowthName = dict(
    ROTA="ROTA",
    ROTAn1="ROTA(n-1)",
    grossMargin="Gross Margin",
    grossMarginn1="Gross Margin(n-1)",
    assetTurnoverRatio="Asset Turnover Ratio",
    assetTurnoverRation1="Asset Turnover Ratio(n-1)",
    reinvestmentRate="Reinvestment Rate",
    research="R&D Expense",
    researchn1="R&D Expense(n-1)",
    operatingIncomeGrowth="Operating Income Growth",
    operatingIncomeGrowthn1="Operating Income Growth(n-1)",
    operatingIncomeGrowthn2="Operating Income Growth(n-2)",
    operatingIncomeAccelerateGrowth="Operating Income Accelerate Growth",
    yearPercentageOfOperatingIncomeGrowth="How many years Of high Operating Income Growth in total data period",
    revenueGrowth="Revenue Growth",
    revenueGrowthn1="Revenue Growth(n-1)",
    revenueGrowthn2="Revenue Growth(n-2)",
    yearPercentageOfRevenueGrowth="How many years Of high Revenue Growth in total data period",
    EPSGrowth="EPSGrowth",
    EPSGrowth3YearAvg="3 Years Average EPSGrowth",
)

SafetyName = dict(
    totalAssets="Total Assets",
    totalAssetsn1="Total Assets (n-1)",
    totalLiabilities="Total Liabilities",
    totalLiabilitiesn1="Total Liabilities (n-1)",
    longTermDebt="Long-Term Debt",
    longTermDebtn1="Long-Term Debt(n-1)",
    freeCashFlow="Free Cash Flow",
    yearPercentageOfPositiveFreeCashFlow="How many years Of high FCF in total data period",
    currentRatio="Current Ratio",
    currentRation1="Current Ratio(n-1)",
    quickRatio="Quick Ratio",
    quickRation1="Quick Ratio(n-1)",
    debtEquityRatio="Debt/Equity Ratio",
    debtCapitalRatio="Debt/Capital Ratio",
    debtAssetRatio="Debt/Asset Ratio",
    totalDividendsFCFRatio="Total Dividends/FCF Ratio",
    shareCapital="Share capital",
    shareCapitaln1="Share capital(n-1)",
)

PriceName = dict(
    dividend=thisModule.ShareHolderName["dividend"],
    avgGrowthRate="Avg. Growth Rate",
    highGrowthPeriod="High growth period",
    highGrowthRate="High growth, next N years",
    discountRate="Discount rate",
    marginOfSafety="Margin of Safety",
    dividendAfterNYears="Dividend after N years",
    treasuriesYield="Treasuries Yield",
    stockPrice="Stock Price",
    growthRateByPRATModel="Growth Rate By PRAT Model",
    CPriceDDM="Cheap present value (DDM)",
    RPriceDDM="Net present value (DDM)",
    EPriceDDM="Expensive present value (DDM)",
    CPriceDDM2="Cheap present value (DDM-2)",
    RPriceDDM2="Net present value (DDM-2)",
    EPriceDDM2="Expensive present value (DDM-2)",
    CPriceDDMH="Cheap present value (DDM-H)",
    RPriceDDMH="Net present value (DDM-H)",
    EPriceDDMH="Expensive present value (DDM-H)",
    avgNetIncomeMargin="Avg Net Income Margin",
    avgFCFNetIncomeRatio="Avg FCF/ Net Income",
    revenueEstimateDCFHalfYear="Estimate Revenue 0.5 year",
    revenueEstimateDCFOneYear="Estimate Revenue 1 year",
    perpetualGrowthRate="Perpetual Growth",
    CPriceDCF="Cheap present value (DCF)",
    RPriceDCF="Net present value (DCF)",
    EPriceDCF="Expensive present value (DCF)",
    CBenjaminGraham="Cheap Benjamin Graham Price",
    RBenjaminGraham="Benjamin Graham Price",
    EBenjaminGraham="Expensive Benjamin Graham Price",
    CEBTRatio="Cheap EBT(EBT/Price)",
    REBTRatio="EBT(EBT/Price)",
    EEBTRatio="Expensive EBT(EBT/Price)",
    CPriceFCFF="Cheap Price FCFF",
    RPriceFCFF="Price FCFF",
    EPriceFCFF="Expensive Price FCFF",
    CPriceFCFE="Cheap Price FCFE",
    RPriceFCFE="Price FCFE",
    EPriceFCFE="Expensive Price FCFE",
    CAvgPriceofValueInvestment="Cheap Avg price of Value Investment",
    RAvgPriceofValueInvestment="Avg price of Value Investment",
    EAvgPriceofValueInvestment="Expensive Avg price of Value Investment",
    CAvgPriceofGrowthInvestment="Cheap Avg price of Growth Investment",
    RAvgPriceofGrowthInvestment="Avg price of Growth Investment",
    EAvgPriceofGrowthInvestment="Expensive Avg price of Growth Investment",
    DiscountPremiumOfDDM="Discount Premium Of DDM",
    DiscountPremiumOfDDM2="Discount Premium Of DDM2",
    DiscountPremiumOfDDMH="Discount Premium Of DDMH",
    DiscountPremiumOfFCFE="Discount Premium Of FCFE",
    DiscountPremiumOfDCF="Discount Premium Of DCF",
    DiscountPremiumOfGraham="Discount Premium Of Graham",
    DiscountPremiumOfEBT="Discount Premium Of EBT",
)

ValueName = dict(
    PRRatio="PRRatio",
    PSRatio="PSRatio",
    PERatio="PERatio",
    PEGRatio="PEGRatio",
    PBRatio="PBRatio",
    PEG="PEG",
)

AnalyzeName = dict(
    sumValueInvestment='sum-valueInvestment',
    sumGrowthInvestment='sum-growthInvestment',
    fullCreditsValueInvestment='fullCredits-valueInvestment',
    fullCreditsGrowthInvestment='fullCredits-growthInvestment',
    investmentType="Investment Type",
    finalScore="Final Score"
)

BuyDecisionTable = dict(
    stockPrice=thisModule.PriceName["stockPrice"],
    finalScore=thisModule.AnalyzeName["finalScore"],
    investmentType=thisModule.AnalyzeName["investmentType"],
    DiscountPremiumOfFCFE=thisModule.PriceName["DiscountPremiumOfFCFE"],
)

SellDecisionTable = dict(
    dividend=thisModule.ShareHolderName["dividend"],
    stockPrice=thisModule.PriceName["stockPrice"],
    finalScore=thisModule.AnalyzeName["finalScore"],
    lastYearFinalScore='Last Year Final Score',
    investmentType=thisModule.AnalyzeName["investmentType"],
    lastYearInvestmentType='Last Year Investment Type',
    DiscountPremiumOfFCFE=thisModule.PriceName["DiscountPremiumOfFCFE"],
)

DDM = dict(
    discountRate=0.1312,  # From WACC
)


DDM2 = dict(
    highGrowthPeriod=15,
    highGrowthRate=0.129,
    perpetualGrowthRate=0.025,
    discountRate=0.07,  # From WACC
)

DDMH = dict(
    highGrowthPeriod=15,
    highGrowthRate=0.129,
    perpetualGrowthRate=0.025,
    discountRate=0.07,  # From WACC
)


DCF = dict(
    perpetualGrowthRate=0.02,
    discountRate=0.07,  # From WACC
)

FCFF = dict(
    perpetualGrowthRate=0.03,
    discountRate=0.09,  # From WACC
    taxRate=0.3
)

FCFE = dict(
    discountRate=0.1307,  # From WACC
)

marginOfSafety = 0.8

# criteria = dict(
#     ShareHolder=[
#         {
#             "name": "dividendYield>2%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ShareHolderName["dividendYield"],
#                       "criteria": 0.02, "operator":["gt"]}]
#         }, {
#             "name": "payoutRatio>80%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ShareHolderName["payoutRatio"],
#                       "criteria": 0.8, "operator":["gt"]}],
#         }, {
#             "name": "payoutRatio<80%",
#             "mode": ["growthInvestment"],
#             "data":  [{"name": thisModule.ShareHolderName["payoutRatio"],
#                        "criteria": 0.8, "operator":["lt"]},
#                       {"name": thisModule.ShareHolderName["payoutRatio"],
#                        "criteria": 0, "operator":["gt"]}
#                       ],
#         }, {
#             "name": "dividendGrowthinThreeYear=True",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ShareHolderName["dividendGrowthinThreeYear"],
#                       "criteria": True, "operator":["eq"]}],
#         }, {
#             "name": "fiveYearAverageDividendGrowth>1",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"],
#                       "criteria": 1, "operator":["gt"]}],
#         }, {
#             "name": "dividend stability",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"], "name2": thisModule.ShareHolderName["maxDividendinFiveYears"], "operator":["lt"], "criteria":0.25},
#                      {"name": thisModule.ShareHolderName["minDividendinFiveYears"], "name2": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"], "operator":["lt"], "criteria":0.25}]
#         }
#     ], FScore=[
#         {
#             "name": "ROA>0",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["ROA"],
#                       "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "OCF>0",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["operatingCashFlow"],
#                       "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "OCF>Net Income",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["operatingCashFlow"],
#                       "name2": thisModule.ProfitName["netIncome"], "criteria":1, "operator":["gt"]}],
#         },
#         {
#             "name": "ROTA(N) > ROTA(N-1)",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.GrowthName["ROTA"],
#                       "name2": thisModule.GrowthName["ROTAn1"], "criteria":1, "operator":["gt"]}],
#         },
#         {
#             "name": "Asset Turnover Ratio(N) >Asset Turnover Ratio(N-1)",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.GrowthName["assetTurnoverRatio"],
#                       "name2": thisModule.GrowthName["assetTurnoverRation1"], "criteria":1, "operator":["gt"]}],
#         },
#         {
#             "name": "Gross Margin(N) > Gross Margin(N-1)",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.GrowthName["grossMargin"],
#                       "name2": thisModule.GrowthName["grossMarginn1"], "criteria":1, "operator":["gt"]}],
#         },
#         {
#             "name": "Long-Term Debt(N)<Long-Term Debt(N-1)",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.SafetyName["longTermDebt"],
#                       "name2": thisModule.SafetyName["longTermDebtn1"], "criteria":1, "operator":["lt"]}],

#         },
#         {
#             "name": "Shares(N)<Shares(N-1)",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.SafetyName["shareCapital"],
#                       "name2": thisModule.SafetyName["shareCapitaln1"], "criteria":1, "operator":["lt"]}],
#         },
#         {
#             "name": "Current Ratio(N) > Current Ratio(N-1)",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.SafetyName["currentRatio"],
#                       "name2": thisModule.SafetyName["currentRation1"], "criteria":1, "operator":["gt"]}],
#         }
#     ],
#     Profit=[
#         {
#             "name": "ROE > 15%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["ROA"], "criteria": 0.15, "operator":["gt"]}],
#         },
#         {
#             "name": "ROE(N) = Max(ROE)",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["ROE"],
#                       "name2": thisModule.ProfitName["maxROEinFourYears"], "criteria":1, "operator":["eq"]}],
#         },
#         {
#             "name": "ROA/ROE>80%",
#             "mode": ["valueInvestment", "growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["ROA"],
#                       "name2": thisModule.ProfitName["ROE"], "criteria":0.8, "operator":["gt"]}],
#         },
#         {
#             "name": "ROA>0%",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["ROA"], "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "ROE>15%in 5 years",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["ROE"], "criteria": 0.15, "operator":["gt"]},
#                      {"name": thisModule.ProfitName["ROEn1"],
#                       "criteria": 0.15, "operator":["gt"]},
#                      {"name": thisModule.ProfitName["ROEn2"],
#                       "criteria": 0.15, "operator":["gt"]},
#                      {"name": thisModule.ProfitName["ROEn3"],
#                       "criteria": 0.15, "operator":["gt"]}],
#         },
#         {
#             "name": "Gross Margin>15%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.GrowthName["grossMargin"],
#                       "criteria": 0.15, "operator":["gt"]}],
#         },
#         {
#             "name": "Gross Margin>30%",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.GrowthName["grossMargin"],
#                       "criteria": 0.30, "operator":["gt"]}],
#         },
#         {
#             "name": "Operating Margin>10%",
#             "mode": ["valueInvestment", "growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["operatingMargin"],
#                       "criteria": 0.1, "operator":["gt"]}],
#         },
#         {
#             "name": "ROE stability",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["maxROEinFourYears"],
#                       "name2": thisModule.ProfitName["minROEinFouryears"], "criteria": 4, "operator":["lt"]}],
#         },
#         {
#             "name": "High Free cash flow",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["freeCashFlow"], "criteria": 0, "operator":["gt"]},
#                      {"name": thisModule.ProfitName["freeCashFlow"], "name2":thisModule.ShareHolderName['totalDividend'], "criteria": 1, "operator":["gt"]}],
#         },
#         {
#             "name": "Allow negitative cash flow",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["freeCashFlow"],
#                       "criteria": 0, "operator":["lt"]}],
#         },
#         {
#             "name": "FCF/OCF>80%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.ProfitName["freeCashFlow"],
#                       "name2":thisModule.ProfitName['operatingCashFlow'], "criteria": 0.8, "operator":["gt"]}]
#         },
#         {
#             "name": "FCF/OCF >30%",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.ProfitName["freeCashFlow"],
#                       "name2":thisModule.ProfitName['operatingCashFlow'], "criteria": 0.3, "operator":["gt"]}]
#         }
#     ],
#     Growth=[
#         {
#             "name": "RR<=0",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.GrowthName["reinvestmentRate"],
#                       "criteria": 0, "operator":["lt"]}],
#         },
#         {
#             "name": "RR>0",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.GrowthName["reinvestmentRate"],
#                       "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "Operating Income Growth % > 0",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.GrowthName["operatingIncomeGrowth"],
#                       "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "Operating Income Growth % > 10%",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.GrowthName["operatingIncomeGrowth"],
#                       "criteria": 0.1, "operator":["gt"]}],
#         },
#         {
#             "name": "Operating Income Growth % > 15% in 3 years",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.GrowthName["operatingIncomeGrowth"], "criteria": 0.15, "operator":["gt"]},
#                      {"name": thisModule.GrowthName["operatingIncomeGrowthn1"],
#                       "criteria": 0.15, "operator":["gt"]},
#                      {"name": thisModule.GrowthName["operatingIncomeGrowthn2"], "criteria": 0.15, "operator":["gt"]}],
#         },
#         {
#             "name": "total revenue % is positive in 3 years",
#             "mode": ["growthInvestment"],
#             "data": [{"name": thisModule.GrowthName["revenueGrowth"], "criteria": 0, "operator":["gt"]},
#                      {"name": thisModule.GrowthName["revenueGrowthn1"],
#                       "criteria": 0, "operator":["gt"]},
#                      {"name": thisModule.GrowthName["revenueGrowthn2"], "criteria": 0, "operator":["gt"]}]
#         }
#     ],
#     Safety=[
#         {
#             "name": "D/E<1",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.SafetyName["debtEquityRatio"],
#                       "criteria": 1, "operator":["lt"]},
#                      {"name": thisModule.SafetyName["debtEquityRatio"],
#                       "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "D/C Ratio<50%",
#             "mode": ["valueInvestment", "growthInvestment"],
#             "data": [{"name": thisModule.SafetyName["debtCapitalRatio"],
#                       "criteria": 0.5, "operator":["lt"]},
#                      {"name": thisModule.SafetyName["debtCapitalRatio"],
#                       "criteria": 0, "operator":["gt"]}],
#         },
#         {
#             "name": "Quick Ratio>100%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.SafetyName["quickRatio"],
#                       "criteria": 1, "operator":["gt"]}],
#         },
#         {
#             "name": "Dividends / FCF Ratio <200%",
#             "mode": ["valueInvestment"],
#             "data": [{"name": thisModule.SafetyName["totalDividendsFCFRatio"],
#                       "criteria": 2, "operator":["lt"]}]
#         }
#     ]
# )
