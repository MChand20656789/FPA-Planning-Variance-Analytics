import os
import pandas as pd

os.makedirs("output", exist_ok=True)

sales = pd.read_csv("data/sales.csv")
expenses = pd.read_csv("data/expenses.csv")

# Product-level financials
sales["revenue"] = sales["units"] * sales["selling_price"]
sales["cogs"] = sales["units"] * sales["unit_cogs"]
sales["gross_profit"] = sales["revenue"] - sales["cogs"]
sales["gross_margin_pct"] = (
    sales["gross_profit"] / sales["revenue"] * 100
)

# SKU profitability
sku_financials = (
    sales.groupby("sku")
    .agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        cogs=("cogs", "sum"),
        gross_profit=("gross_profit", "sum"),
    )
    .reset_index()
)

sku_financials["gross_margin_pct"] = (
    sku_financials["gross_profit"]
    / sku_financials["revenue"]
    * 100
)

# Channel profitability
channel_financials = (
    sales.groupby("channel")
    .agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        cogs=("cogs", "sum"),
        gross_profit=("gross_profit", "sum"),
    )
    .reset_index()
)

channel_financials["gross_margin_pct"] = (
    channel_financials["gross_profit"]
    / channel_financials["revenue"]
    * 100
)

# Monthly P&L
monthly = (
    sales.groupby(["month", "quarter"])
    .agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        cogs=("cogs", "sum"),
        gross_profit=("gross_profit", "sum"),
    )
    .reset_index()
)

monthly_expenses = (
    expenses.groupby(["month", "quarter"])
    .agg(
        operating_expenses=("actual_expense", "sum")
    )
    .reset_index()
)

monthly = monthly.merge(
    monthly_expenses,
    on=["month", "quarter"],
    how="left"
)

monthly["gross_margin_pct"] = (
    monthly["gross_profit"]
    / monthly["revenue"]
    * 100
)

monthly["operating_income"] = (
    monthly["gross_profit"]
    - monthly["operating_expenses"]
)

monthly["operating_margin_pct"] = (
    monthly["operating_income"]
    / monthly["revenue"]
    * 100
)

# Save outputs
sku_financials.to_csv(
    "output/sku_financials.csv",
    index=False
)

channel_financials.to_csv(
    "output/channel_financials.csv",
    index=False
)

monthly.to_csv(
    "output/monthly_financials.csv",
    index=False
)

print("Financial model calculated successfully.")
print()
print("Total Revenue: ${:,.2f}".format(monthly["revenue"].sum()))
print("Total COGS: ${:,.2f}".format(monthly["cogs"].sum()))
print("Gross Profit: ${:,.2f}".format(monthly["gross_profit"].sum()))
print(
    "Gross Margin: {:.2f}%".format(
        monthly["gross_profit"].sum()
        / monthly["revenue"].sum()
        * 100
    )
)
print(
    "Operating Expenses: ${:,.2f}".format(
        monthly["operating_expenses"].sum()
    )
)
print(
    "Operating Income: ${:,.2f}".format(
        monthly["operating_income"].sum()
    )
)