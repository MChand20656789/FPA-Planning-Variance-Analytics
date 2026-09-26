import os
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# Load analysis outputs
# --------------------------------------------------

monthly = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "monthly_financials.csv"
    )
)

variance = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "budget_vs_actual.csv"
    )
)

sku = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "sku_financials.csv"
    )
)

channel = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "channel_financials.csv"
    )
)

forecast = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "revenue_forecast.csv"
    )
)

# --------------------------------------------------
# Financial totals
# --------------------------------------------------

total_revenue = monthly["revenue"].sum()
total_cogs = monthly["cogs"].sum()
gross_profit = monthly["gross_profit"].sum()
gross_margin = gross_profit / total_revenue

total_opex = monthly["operating_expenses"].sum()
operating_income = monthly["operating_income"].sum()

revenue_budget = variance["revenue_budget"].sum()
revenue_variance = variance["revenue_variance"].sum()

gp_budget = variance["budget_gross_profit"].sum()
gp_variance = variance["gross_profit_variance"].sum()

opex_budget = variance["budget_opex"].sum()
opex_variance = variance["opex_variance"].sum()

forecast_total = forecast["forecast_revenue"].sum()

# --------------------------------------------------
# Identify key products and channels
# --------------------------------------------------

top_product = sku.loc[
    sku["gross_profit"].idxmax()
]

top_margin_product = sku.loc[
    sku["gross_margin_pct"].idxmax()
]

top_channel = channel.loc[
    channel["gross_profit"].idxmax()
]

# --------------------------------------------------
# Build report
# --------------------------------------------------

report = []

report.append(
    "# FP&A Planning & Variance Analytics"
)

report.append(
    "\n## Executive Summary\n"
)

report.append(
    f"""
The business generated **${total_revenue:,.0f} in revenue**
during the modeled period, producing **${gross_profit:,.0f} in
gross profit** and a **{gross_margin:.1%} gross margin**.

Operating expenses totaled **${total_opex:,.0f}**, resulting in
operating income of **${operating_income:,.0f}**.

Revenue finished **${abs(revenue_variance):,.0f}**
{"below" if revenue_variance < 0 else "above"} budget, while
operating expenses were **${abs(opex_variance):,.0f}**
{"below" if opex_variance < 0 else "above"} budget.

The next-quarter revenue forecast is approximately
**${forecast_total:,.0f}**.
"""
)

# --------------------------------------------------
# Budget vs Actual
# --------------------------------------------------

report.append(
    "\n## Budget vs Actual Analysis\n"
)

report.append(
    f"""
| Metric | Actual | Budget | Variance |
|---|---:|---:|---:|
| Revenue | ${total_revenue:,.0f} | ${revenue_budget:,.0f} | ${revenue_variance:,.0f} |
| Gross Profit | ${gross_profit:,.0f} | ${gp_budget:,.0f} | ${gp_variance:,.0f} |
| Operating Expenses | ${total_opex:,.0f} | ${opex_budget:,.0f} | ${opex_variance:,.0f} |
"""
)

# --------------------------------------------------
# Profitability
# --------------------------------------------------

report.append(
    "\n## Profitability Analysis\n"
)

report.append(
    f"""
### Highest Gross Profit Product

**{top_product["sku"]}**

- Revenue: ${top_product["revenue"]:,.0f}
- COGS: ${top_product["cogs"]:,.0f}
- Gross Profit: ${top_product["gross_profit"]:,.0f}
- Gross Margin: {top_product["gross_margin_pct"]:.1%}

### Highest Gross Margin Product

**{top_margin_product["sku"]}**

- Revenue: ${top_margin_product["revenue"]:,.0f}
- Gross Profit: ${top_margin_product["gross_profit"]:,.0f}
- Gross Margin: {top_margin_product["gross_margin_pct"]:.1%}

### Channel Profitability

The channel generating the highest gross profit in the modeled
period was **{top_channel["channel"]}**, with gross profit of
**${top_channel["gross_profit"]:,.0f}**.
"""
)

# --------------------------------------------------
# Forecast
# --------------------------------------------------

report.append(
    "\n## Revenue Forecast\n"
)

report.append(
    f"""
The revenue forecasting model combines the historical revenue
trend with a three-month rolling average.

- Recent three-month average: ${forecast["rolling_average_forecast"].iloc[0]:,.0f}
- Monthly trend: approximately ${forecast["trend_forecast"].diff().mean():,.0f}
- Next-quarter forecast: ${forecast_total:,.0f}
"""
)

# --------------------------------------------------
# Management insights
# --------------------------------------------------

report.append(
    "\n## Management Insights\n"
)

report.append(
    f"""
1. **Revenue performance:** Revenue was
   ${abs(revenue_variance):,.0f}
   {"below" if revenue_variance < 0 else "above"} budget.

2. **Gross profit:** Gross profit was
   ${abs(gp_variance):,.0f}
   {"below" if gp_variance < 0 else "above"} budget.

3. **Expense management:** Operating expenses were
   ${abs(opex_variance):,.0f}
   {"below" if opex_variance < 0 else "above"} budget.

4. **Product economics:** {top_product["sku"]} generated the
   highest gross profit among the modeled products.

5. **Channel economics:** {top_channel["channel"]} generated the
   highest gross profit among the modeled sales channels.

6. **Forward planning:** The next-quarter forecast indicates
   approximately ${forecast_total:,.0f} in revenue based on
   recent performance and historical trend.
"""
)

# --------------------------------------------------
# Methodology
# --------------------------------------------------

report.append(
    "\n## Methodology\n"
)

report.append(
    """
The analysis was built using Python, Pandas, SQLite, and
Streamlit.

The workflow includes:

1. Financial data generation
2. Data preparation and validation
3. Revenue and COGS modeling
4. Gross profit and margin calculations
5. Budget vs actual analysis
6. Variance calculations
7. Revenue forecasting
8. SQLite financial reporting
9. Management dashboard development
"""
)

# --------------------------------------------------
# Write report
# --------------------------------------------------

report_path = os.path.join(
    OUTPUT_DIR,
    "management_report.md"
)

with open(
    report_path,
    "w",
    encoding="utf-8"
) as file:

    file.write(
        "\n".join(report)
    )

print(
    f"Management report generated: {report_path}"
)