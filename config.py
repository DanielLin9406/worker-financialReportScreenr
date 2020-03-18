import sys
thisModule = sys.modules[__name__]

ShareHolderName = dict(
    dividend="Dividend",
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
    ROEn4="ROE(n-4)",
    fiveYearAverageROE="5-year Average ROE",
    maxROEinFiveyears="Max ROE in 5 years",
    minROEinFiveyears="Min ROE in 5 years",
    ROA="ROA",
    # grossMargin="Gross Margin",
    operatingMargin="Operating Margin",
    operatingCashFlow="Operating Cash Flow",
    netIncome="Net Income",
    freeCashFlow="Free Cash Flow",
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
    operatingIncomeGrowth="Operating Income Growth",
    operatingIncomeGrowthn1="Operating Income Growth(n-1)",
    operatingIncomeGrowthn2="Operating Income Growth(n-2)",
    revenueGrowth="Revenue Growth",
    revenueGrowthn1="Revenue Growth(n-1)",
    revenueGrowthn2="Revenue Growth(n-1)",
    EPSGrowth="EPSGrowth",
)

SafetyName = dict(
    longTermDebt="Long-Term Debt",
    longTermDebtn1="Long-Term Debt(n-1)",
    currentRatio="Current Ratio",
    currentRation1="Current Ratio(n-1)",
    quickRatio="Quick Ratio",
    debtEquityRatio="Debt/Equity Ratio",
    debtCapitalRatio="Debt/Capital Ratio",
    debtAssetRatio="Debt/Asset Ratio",
    dividendsFCFRatio="Dividends/FCF Ratio",
    shareCapital="Share capital",
    shareCapitaln1="Share capital(n-1)",
)

PriceName = dict(
    highGrowthPeriod="High growth period",
    yieldGrowthRate="Yield growth, next N years",
    terminalYieldGrowth="Terminal Yield growth",
    discountRate="Discount rate",
    marginOfSafety="Margin of Safety",
    dividendAfterNYears="Dividend after N years",
    treasuriesYield="Treasuries Yield",
    stockPrice="Stock Price",
    PriceDDM2="Net present value (DDM-2)",
    PriceDDMH="Net present value (DDM-H)",
    BenjaminGraham="Benjamin Graham Price",
    EBTRatio="EBT(EBT/Price)",
    PriceFCFF="Price FCFF",
    PriceFCFE="Price FCFE",
)

ValueName = dict(
    PRRatio="PRRatio",
    PSRatio="PSRatio",
    PERatio="PERatio",
    PEGRatio="PEGRatio",
    PBRatio="PBRatio",
    PEG="PEG",
)

DDM = dict(
    highGrowthPeriod=10,
    yieldGrowthRate=0.1034,
    terminalYieldGrowth=0.03,
    discountRate=0.09
)

FCFF = dict(
    costOfCapital=0.09,
    infiniteGrowthRate=0.03,
    taxRate=0.3
)

FCFE = dict(
    costOfEquity=0.12,
    infiniteGrowthRate=0.03
)

marginOfSafety = 0.8

criteria = dict(
    ShareHolder=[
        {
            "name": "dividendYield>2%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ShareHolderName["dividendYield"],
                      "criteria": 0.02, "operator":["gt"]}]
        }, {
            "name": "payoutRatio>80%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ShareHolderName["payoutRatio"],
                      "criteria": 0.8, "operator":["gt"]}],
        }, {
            "name": "payoutRatio<80%",
            "mode": "growthInvestment",
            "data":  [{"name": thisModule.ShareHolderName["payoutRatio"],
                       "criteria": 0.8, "operator":["lt", "eq"]}],
        }, {
            "name": "dividendGrowthinThreeYear=True%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ShareHolderName["dividendGrowthinThreeYear"],
                      "criteria": True, "operator":["eq"]}],
        }, {
            "name": "fiveYearAverageDividendGrowth>1",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"],
                      "criteria": 1, "operator":["gt"]}],
        }, {
            "name": "dividend stability",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"], "name2": thisModule.ShareHolderName["maxDividendinFiveYears"], "operator":["lt"], "criteria":0.25},
                     {"name": thisModule.ShareHolderName["minDividendinFiveYears"], "name2": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"], "operator":["lt"], "criteria":0.25}]
        }
    ], FScore=[
        {
            "name": "ROA>0",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["ROA"],
                      "criteria": 0, "operator":["gt"]}],
        },
        {
            "name": "OCF>0",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["operatingCashFlow"],
                      "criteria": 0, "operator":["gt"]}],
        },
        {
            "name": "OCF>Net Income",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["operatingCashFlow"],
                      "name2": thisModule.ProfitName["netIncome"], "criteria":1, "operator":["gt"]}],
        },
        {
            "name": "ROTA(N) > ROTA(N-1)",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.GrowthName["ROTA"],
                      "name2": thisModule.GrowthName["ROTAn1"], "criteria":1, "operator":["gt"]}],
        },
        {
            "name": "Asset Turnover Ratio(N) >Asset Turnover Ratio(N-1)",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.GrowthName["assetTurnoverRatio"],
                      "name2": thisModule.GrowthName["assetTurnoverRation1"], "criteria":1, "operator":["gt"]}],
        },
        {
            "name": "Gross Margin(N) > Gross Margin(N-1)",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.GrowthName["grossMargin"],
                      "name2": thisModule.GrowthName["grossMarginn1"], "criteria":1, "operator":["gt"]}],
        },
        {
            "name": "Long-Term Debt(N)<Long-Term Debt(N-1)",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.SafetyName["longTermDebt"],
                      "name2": thisModule.SafetyName["longTermDebtn1"], "criteria":1, "operator":["lt"]}],

        },
        {
            "name": "Shares(N)<Shares(N-1)",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.SafetyName["shareCapital"],
                      "name2": thisModule.SafetyName["shareCapitaln1"], "criteria":1, "operator":["lt"]}],
        },
        {
            "name": "Current Ratio(N) > Current Ratio(N-1)",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.SafetyName["currentRatio"],
                      "name2": thisModule.SafetyName["currentRation1"], "criteria":1, "operator":["gt"]}],
        }
    ],
    Profit=[
        {
            "name": "ROE > 15%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["ROA"], "criteria": 0.15, "operator":["gt"]}],
        },
        {
            "name": "ROE(N) = Max(ROE)",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.ProfitName["ROE"],
                      "name2": thisModule.ProfitName["maxROEinFiveyears"], "criteria":1, "operator":["eq"]}],
        },
        {
            "name": "ROA/ROE>80%",
            "mode": "both",
            "data": [{"name": thisModule.ProfitName["ROA"],
                      "name2": thisModule.ProfitName["ROE"], "criteria":0.8, "operator":["gt"]}],
        },
        {
            "name": "ROA>0%",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.ProfitName["ROA"], "criteria": 0, "operator":["gt"]}],
        },
        {
            "name": "ROE>15%in 5 years",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.ProfitName["ROE"], "criteria": 0.15, "operator":["gt"]},
                     {"name": thisModule.ProfitName["ROEn1"],
                      "criteria": 0.15, "operator":["gt"]},
                     {"name": thisModule.ProfitName["ROEn2"],
                      "criteria": 0.15, "operator":["gt"]},
                     {"name": thisModule.ProfitName["ROEn3"],
                      "criteria": 0.15, "operator":["gt"]},
                     {"name": thisModule.ProfitName["ROEn4"],
                      "criteria": 0.15, "operator":["gt"]}],
        },
        {
            "name": "Gross Margin>15%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.GrowthName["grossMargin"],
                      "criteria": 0.15, "operator":["gt"]}],
        },
        {
            "name": "Gross Margin>30%",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.GrowthName["grossMargin"],
                      "criteria": 0.30, "operator":["gt"]}],
        },
        {
            "name": "Operating Margin>10%",
            "mode": "both",
            "data": [{"name": thisModule.ProfitName["operatingMargin"],
                      "criteria": 0.1, "operator":["gt"]}],
        },
        {
            "name": "ROE stability",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["maxROEinFiveyears"],
                      "name2": thisModule.ProfitName["minROEinFiveyears"], "criteria": 4, "operator":["lt"]}],
        },
        {
            "name": "High Free cash flow",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["freeCashFlow"], "criteria": 0, "operator":["gt"]},
                     {"name": thisModule.ProfitName["freeCashFlow"], "name2":thisModule.ShareHolderName['totalDividend'], "criteria": 1, "operator":["gt"]}],
        },
        {
            "name": "Allow negitative cash flow",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.ProfitName["freeCashFlow"],
                      "criteria": 0, "operator":["lt"]}],
        },
        {
            "name": "FCF/OCF>80%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.ProfitName["freeCashFlow"],
                      "name2":thisModule.ProfitName['operatingCashFlow'], "criteria": 0.8, "operator":["gt"]}]
        },
        {
            "name": "FCF/OCF >30%",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.ProfitName["freeCashFlow"],
                      "name2":thisModule.ProfitName['operatingCashFlow'], "criteria": 0.3, "operator":["gt"]}]
        }
    ],
    Growth=[
        {
            "name": "RR<=0",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.GrowthName["reinvestmentRate"],
                      "criteria": 0, "operator":["lt"]}],
        },
        {
            "name": "RR>0",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.GrowthName["reinvestmentRate"],
                      "criteria": 0, "operator":["gt"]}],
        },
        {
            "name": "Operating Income Growth % > 0",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.GrowthName["reinvestmentRate"],
                      "criteria": 0, "operator":["lt"]}],
        },
        {
            "name": "Operating Income Growth % > 10%",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.GrowthName["operatingIncomeGrowthn1"],
                      "criteria": 0.1, "operator":["gt"]}],
        },
        {
            "name": "Operating Income Growth % > 15% in 3 years",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.GrowthName["operatingIncomeGrowth"], "criteria": 0.15, "operator":["gt"]},
                     {"name": thisModule.GrowthName["operatingIncomeGrowthn1"],
                      "criteria": 0.15, "operator":["gt"]},
                     {"name": thisModule.GrowthName["operatingIncomeGrowthn2"], "criteria": 0.15, "operator":["gt"]}],
        },
        {
            "name": "total revenue % is positive in 3 years",
            "mode": "growthInvestment",
            "data": [{"name": thisModule.GrowthName["revenueGrowth"], "criteria": 0, "operator":["gt"]},
                     {"name": thisModule.GrowthName["revenueGrowthn1"],
                      "criteria": 0, "operator":["gt"]},
                     {"name": thisModule.GrowthName["revenueGrowthn2"], "criteria": 0, "operator":["gt"]}]
        }
    ],
    Safety=[
        {
            "name": "D/E<1",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.SafetyName["debtEquityRatio"],
                      "criteria": 1, "operator":["lt"]}],
        },
        {
            "name": "D/C Ratio<50%",
            "mode": "both",
            "data": [{"name": thisModule.SafetyName["debtCapitalRatio"],
                      "criteria": 0.5, "operator":["lt"]}],
        },
        {
            "name": "Quick Ratio>100%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.SafetyName["quickRatio"],
                      "criteria": 1, "operator":["gt"]}],
        },
        {
            "name": "Dividends / FCF Ratio <200%",
            "mode": "valueInvestment",
            "data": [{"name": thisModule.SafetyName["dividendsFCFRatio"],
                      "criteria": 2, "operator":["lt"]}]
        }
    ]
)
