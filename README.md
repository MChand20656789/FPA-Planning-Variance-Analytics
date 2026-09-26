# FP&A Planning & Variance Analytics

A financial planning and analysis system built with Python, SQL, SQLite, and Streamlit to model revenue, COGS, gross profit, operating expenses, budgeting, forecasting, profitability, and financial variance analysis.

The project simulates a consumer-products business with 12 SKUs, multiple sales channels, departmental operating expenses, inventory data, monthly budgets, and financial forecasts.

## Project Overview

This project demonstrates how raw operational and financial data can be transformed into management-ready financial analysis.

The system answers questions such as:

* Are actual revenues above or below budget?
* Which products generate the most gross profit?
* Which products have the highest gross margins?
* Which sales channels are most profitable?
* Where are operating expenses exceeding budget?
* How is revenue trending?
* What revenue can management expect next quarter?
* Which financial variances require attention?

The project follows a simplified FP&A workflow:

**Raw Data → Financial Modeling → Budget vs. Actual → Forecasting → SQL Reporting → Management Dashboard → Management Report**

---

## Key Capabilities

### Financial Modeling

Calculates:

* Revenue
* COGS
* Gross Profit
* Gross Margin %
* Operating Expenses
* Operating Income
* Operating Margin %

### Budget vs. Actual Analysis

Compares monthly actual performance against budget for:

* Revenue
* Units
* COGS
* Gross Profit
* Operating Expenses

Calculates:

* Dollar variance
* Percentage variance
* Basic variance explanations

### Profitability Analysis

Analyzes profitability by:

* SKU
* Sales channel
* Product margin
* Gross profit

### Revenue Forecasting

Uses:

* 3-month rolling averages
* Linear trend analysis
* Combined forecast methodology

Produces a three-month forward revenue forecast.

### SQL Financial Reporting

Includes SQL queries for:

* Monthly P&L reporting
* Product profitability
* Channel profitability
* Revenue variance
* Gross profit variance
* Operating expense variance
* Margin analysis
* Revenue by channel
* Month-over-month revenue changes
* Management-level financial summaries

### Management Dashboard

The Streamlit dashboard provides:

* Revenue KPI
* Gross Profit KPI
* Gross Margin KPI
* Budget Variance KPI
* Next-Quarter Revenue Forecast
* Monthly Revenue Trend
* Actual vs. Budget Revenue
* Revenue Forecast
* Profitability by Channel
* Gross Margin by SKU
* Operating Expenses by Department
* Monthly Financial Variances
* Product Profitability Management View

---

## Financial Model

The project uses a simplified income-statement structure:

```text
Revenue
  ↓
COGS
  ↓
Gross Profit
  ↓
Operating Expenses
  ↓
Operating Income
```

### Core Calculations

```text
Gross Profit = Revenue - COGS

Gross Margin % = Gross Profit / Revenue

Operating Income = Gross Profit - Operating Expenses

Operating Margin % = Operating Income / Revenue
```

---

## Budget vs. Actual Framework

The system calculates financial variances using:

```text
Variance $ = Actual - Budget

Variance % = (Actual - Budget) / Budget
```

The analysis distinguishes between revenue, cost, profitability, and operating-expense variances so that management can identify where actual performance differs from plan.

---

## Forecasting Methodology

Historical monthly revenue is used to produce a short-term forecast.

Two approaches are calculated:

1. **Rolling Average**

   * Uses the most recent three months of revenue.
   * Provides a simple smoothing mechanism.

2. **Trend Forecast**

   * Uses a linear trend fitted to historical monthly revenue.
   * Captures directional movement over time.

The final forecast combines the two approaches:

```text
Combined Forecast =
    (Rolling Average + Trend Forecast) / 2
```

This is a simplified demonstration of forecasting methodology rather than a production forecasting model.

---

## Example Financial Results

Using the simulated 2025 dataset:

| Metric             |   Result |
| ------------------ | -------: |
| Revenue            | $489,681 |
| COGS               | $202,647 |
| Gross Profit       | $287,034 |
| Gross Margin       |   58.62% |
| Operating Expenses | $250,298 |
| Operating Income   |  $36,736 |

### Annual Budget Variance

| Metric             | Variance |
| ------------------ | -------: |
| Revenue            | -$13,328 |
| COGS               |  +$4,711 |
| Gross Profit       | -$18,039 |
| Operating Expenses |  -$3,849 |

Negative revenue and gross-profit variances indicate actual performance was below budget. The negative operating-expense variance indicates expenses were below budget.

All financial data in this project are simulated.

---

## Database

The project stores raw and calculated financial data in SQLite.

Database:

```text
output/fpa.db
```

Tables include:

```text
budget
budget_vs_actual
channel_financials
expenses
inventory
monthly_financials
products
revenue_forecast
revenue_forecast_history
sales
sku_financials
```

The database allows financial analysis to move beyond CSV-based processing into a relational reporting workflow.

---

## Project Structure

```text
FP&A-Planning-Variance-Analytics/
│
├── data/
│   ├── products.csv
│   ├── sales.csv
│   ├── budget.csv
│   ├── expenses.csv
│   └── inventory.csv
│
├── scripts/
│   ├── create_data.py
│   ├── calculate_financials.py
│   ├── calculate_variance.py
│   ├── forecast.py
│   ├── load_database.py
│   └── generate_report.py
│
├── sql/
│   └── financial_queries.sql
│
├── dashboard/
│   └── app.py
│
├── output/
│   ├── sku_financials.csv
│   ├── channel_financials.csv
│   ├── monthly_financials.csv
│   ├── budget_vs_actual.csv
│   ├── revenue_forecast.csv
│   ├── revenue_forecast_history.csv
│   └── management_report.md
│
├── ARCHITECTURE.md
├── README.md
├── requirements.txt
└── .gitignore
```

---

## Workflow

### 1. Generate Business Data

```bash
python scripts/create_data.py
```

Creates simulated:

* Product data
* Sales transactions
* Monthly budgets
* Department expenses
* Inventory data

### 2. Calculate Financials

```bash
python scripts/calculate_financials.py
```

Creates:

* SKU financials
* Channel financials
* Monthly financials

### 3. Calculate Budget Variances

```bash
python scripts/calculate_variance.py
```

Creates the budget-vs-actual analysis.

### 4. Generate Revenue Forecast

```bash
python scripts/forecast.py
```

Creates historical and forecast revenue datasets.

### 5. Load the SQLite Database

```bash
python scripts/load_database.py
```

Creates:

```text
output/fpa.db
```

### 6. Generate the Management Report

```bash
python scripts/generate_report.py
```

Creates:

```text
output/management_report.md
```

### 7. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

---

## SQL Reporting

The project includes a dedicated SQL reporting layer in:

```text
sql/financial_queries.sql
```

Example:

```sql
SELECT
    month,
    revenue,
    cogs,
    gross_profit,
    gross_margin_pct,
    operating_expenses,
    operating_income,
    operating_margin_pct
FROM monthly_financials
ORDER BY month;
```

Additional queries analyze profitability, variance, margins, channel performance, and month-over-month changes.

---

## Management Reporting

The project produces a management-oriented report containing:

* Executive Summary
* Budget vs. Actual Analysis
* Profitability Analysis
* Revenue Forecast
* Management Insights
* Methodology

The goal is to demonstrate the transition from technical data processing to financial decision support.

---

## Technology Stack

### Programming

* Python
* SQL

### Data Analysis

* Pandas
* NumPy

### Database

* SQLite

### Visualization

* Plotly
* Streamlit

### Development

* Git
* VS Code
* Python virtual environments

The project intentionally avoids PyArrow.

---

## Business Use Cases

This type of workflow can support FP&A and business operations teams with:

* Monthly financial reporting
* Budget tracking
* Forecasting
* Variance analysis
* Product profitability analysis
* Channel profitability
* COGS monitoring
* Operating expense monitoring
* KPI reporting
* Management reporting
* Financial data validation

---

## What This Project Demonstrates

This project combines technical analytics with financial planning concepts.

It demonstrates experience with:

* Financial modeling
* Budgeting
* Forecasting
* Variance analysis
* Profitability analysis
* COGS analysis
* Gross-margin analysis
* KPI development
* Financial reporting
* SQL reporting
* Relational database design
* ETL/data pipelines
* Data validation
* Dashboard development
* Management-oriented reporting

---

## Disclaimer

This project uses simulated business and financial data created for educational and portfolio purposes.

The forecasting and financial models are simplified demonstrations and are not intended for investment, accounting, tax, or operational decision-making.