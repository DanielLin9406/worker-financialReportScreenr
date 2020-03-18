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
    grossMargin="Gross Margin",
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

checkValueInvestment = dict(
    ShareHolder=[
        [{"name": thisModule.ShareHolderName["dividendYield"],
          "criteria": "2%", "operator":"gt"}],
        [{"name": thisModule.ShareHolderName["payoutRatio"],
          "criteria": "80%", "operator":"gt"}],
        [{"name": thisModule.ShareHolderName["dividendGrowthinThreeYear"],
          "criteria": True, "operator":"eq"}],
        [{"name": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"],
          "criteria": 1, "operator":"gt"}],
        [{"name": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"], "criteriaName": thisModule.ShareHolderName["maxDividendinFiveYears"], "operator":"lt25%"},
         {"name": thisModule.ShareHolderName["minDividendinFiveYears"], "criteriaName": thisModule.ShareHolderName["fiveYearAverageDividendGrowth"], "operator":"lt25%"}]
    ],
    FScore=[
        [{"name": thisModule.ProfitName["ROA"],
          "criteria": 0, "operator":"gt"}],
        [{"name": thisModule.ProfitName["operatingCashFlow"],
          "criteria": 0, "operator":"gt"}],
        [{"name": thisModule.ProfitName["operatingCashFlow"],
          "criteriaName": thisModule.ProfitName["netIncome"], "operator":"gt"}],
        [{"name": thisModule.GrowthName["ROTA"],
          "criteriaName": thisModule.GrowthName["ROTAn1"], "operator":"gt"}],
        [{"name": thisModule.GrowthName["assetTurnoverRatio"],
          "criteriaName": thisModule.GrowthName["assetTurnoverRation1"], "operator":"gt"}],
        [{"name": thisModule.GrowthName["grossMargin"],
          "criteriaName": thisModule.GrowthName["grossMarginn1"], "operator":"gt"}],
        [{"name": thisModule.SafetyName["longTermDebt"],
          "criteriaName": thisModule.SafetyName["longTermDebtn1"], "operator":"lt"}],
        [{"name": thisModule.SafetyName["shareCapital"],
          "criteriaName": thisModule.SafetyName["shareCapitaln1"], "operator":"lt"}],
        [{"name": thisModule.SafetyName["currentRatio"],
          "criteriaName": thisModule.SafetyName["currentRation1"], "operator":"gt"}],
    ],
    Profit=[
        [{"name": thisModule.ProfitName["ROA"], "criteria": "15%", "operator":"gt"}],
        [{"name": thisModule.ProfitName["ROA"],
            "criteriaName": thisModule.ProfitName["ROE"], "operator":"gt80%"}],
        [{"name": thisModule.ProfitName["ROE"], "criteria": "15%", "operator":"gt"},
         {"name": thisModule.ProfitName["ROEn1"],
             "criteria": "15%", "operator":"gt"},
         {"name": thisModule.ProfitName["ROEn2"],
             "criteria": "15%", "operator":"gt"},
         {"name": thisModule.ProfitName["ROEn3"],
             "criteria": "15%", "operator":"gt"},
         {"name": thisModule.ProfitName["ROEn4"],
             "criteria": "15%", "operator":"gt"}],
        [{"name": thisModule.ProfitName["grossMargin"],
          "criteria": "15%", "operator":"gt"}],
        [{"name": thisModule.ProfitName["operatingMargin"],
          "criteria": "10%", "operator":"gt"}],
        [{"name": thisModule.ProfitName["maxROEinFiveyears"],
          "criteriaName": thisModule.ProfitName["minROEinFiveyears"], "operator":"lt400%"}],
        [{"name": thisModule.ProfitName["freeCashFlow"], "criteria": 0, "operator":"gt"},
         {"name": thisModule.ProfitName["freeCashFlow"], "criteriaName":thisModule.ShareHolderName['totalDividend'], "operator":"gt"}],
        [{"name": thisModule.ProfitName["freeCashFlow"],
            "criteriaName":thisModule.ProfitName['operatingCashFlow'], "operator":"gt80%"}]
    ],
    Growth=[
        [{"name": thisModule.GrowthName["reinvestmentRate"],
          "criteria": 0, "operator":"lt"}],
        [{"name": thisModule.GrowthName["reinvestmentRate"],
          "criteria": 0, "operator":"lt"}],

    ],
    Safety=[[{"name": thisModule.SafetyName["debtEquityRatio"],
              "criteria": 1, "operator":"lt"}],
            [{"name": thisModule.SafetyName["debtCapitalRatio"],
              "criteria": "50%", "operator":"lt"}],
            [{"name": thisModule.SafetyName["quickRatio"],
              "criteria": "100%", "operator":"gt"}],
            [{"name": thisModule.SafetyName["dividendsFCFRatio"],
              "criteria": "200%", "operator":"lt"}]]
)

checkGrowthInvestment = dict(
    ShareHolder=[
        [{"name": thisModule.ShareHolderName["payoutRatio"],
            "criteria": "80%", "operator":"lteq"}],
    ],
    Profit=[
        [{"name": thisModule.ProfitName["ROE"],
            "criteriaName": thisModule.ProfitName["maxROEinFiveyears"], "operator":"eq"}],
        [{"name": thisModule.ProfitName["ROA"],
            "criteriaName": thisModule.ProfitName["ROE"], "operator":"gt80%"}],
        [{"name": thisModule.ProfitName["ROA"], "criteria": 0, "operator":"gt"}],
        [{"name": thisModule.ProfitName["grossMargin"],
          "criteria": "30%", "operator":"gt"}],
        [{"name": thisModule.ProfitName["operatingMargin"],
          "criteria": "10%", "operator":"gt"}],
        [{"name": thisModule.ProfitName["freeCashFlow"],
            "criteria": 0, "operator":"lt"}],
        [{"name": thisModule.ProfitName["freeCashFlow"],
            "criteriaName":thisModule.ProfitName['operatingCashFlow'], "operator":"gt30%"}]
    ],
    Growth=[
        [{"name": thisModule.GrowthName["reinvestmentRate"],
          "criteria": 0, "operator":"gt"}],
        [{"name": thisModule.GrowthName["operatingIncomeGrowth"],
            "criteria": 0, "operator":"gt"}],
        [{"name": thisModule.GrowthName["operatingIncomeGrowthn1"],
            "criteria": "10%", "operator":"gt"}],
        [{"name": thisModule.GrowthName["operatingIncomeGrowth"], "criteria": "15%", "operator":"gt"},
         {"name": thisModule.GrowthName["operatingIncomeGrowthn1"],
             "criteria": "15%", "operator":"gt"},
         {"name": thisModule.GrowthName["operatingIncomeGrowthn2"], "criteria": "15%", "operator":"gt"}],
        [{"name": thisModule.GrowthName["revenueGrowth"], "criteria": "0", "operator":"gt"},
         {"name": thisModule.GrowthName["revenueGrowthn1"],
             "criteria": "0", "operator":"gt"},
         {"name": thisModule.GrowthName["revenueGrowthn2"], "criteria": "0", "operator":"gt"}]
    ],
    Safety=[[{"name": thisModule.SafetyName["debtCapitalRatio"],
              "criteria": "50%", "operator":"lt"}]]
)
