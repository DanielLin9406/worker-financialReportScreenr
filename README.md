# SEC financial report data pipeline
![image](https://github.com/user-attachments/assets/85c11edc-bf22-443d-bf54-7561702680ae)

![image](https://github.com/user-attachments/assets/1db9ec9f-0bc6-4461-b1cf-f189a705f7b5)

![image](https://github.com/user-attachments/assets/f353e96d-eab6-45da-ade1-36530236fd9b)


A SEC financial report is input and a well-organized table is output to Google Sheet.

## Features
- Two pipeline leveraging Python to build a SEC financial report.
- Company Screener
  - Input are three financial report files exported from morningstar and location is under ~/FinancialData/{ticker}, while output is custom report on Google Excel.
  ![Input file path](image.png)
- SEC Financial Report Scraper
  - Input is a ticker symbol, date of that stock, while output is custom report on Google Excel.

## Start Project

```bash
# Run pipeline 1
cd companyScreener
python3 main.py

# Run pipeline 2
cd secFinancialReportScrper
python3 main.py
```

## TechStacks

### Data Pipeline
- Python
- Google Sheet API

The contents in the following folders will be completed after this project's priority to the top again.

