import os
import pandas as pd

os.makedirs("output", exist_ok=True)

sales = pd.read_csv("data/sales.csv")
budget = pd.read_csv("data/budget.csv")
expenses = pd.read_csv("data/expenses.csv")

# -----------------------------
# Actual monthly sales
# -----------------------------

actual = (
    sales.groupby(["month", "quarter"])
    .agg(
        units=("units", "sum"),
        revenue=("revenue", "sum"),
        cogs=("cogs", "sum"),
    )
    .reset_index()
)

actual["gross_profit"] = (
    actual["revenue"] - actual["cogs"]
)

# -----------------------------
# Operating expenses
# -----------------------------

opex = (
    expenses.groupby(["month", "quarter"])
    .agg(
        operating_expenses=("actual_expense", "sum"),
        budget_opex=("budget_expense", "sum"),
    )
    .reset_index()
)

# -----------------------------
# Combine actual + budget
# -----------------------------

variance = actual.merge(
    budget,
    on=["month", "quarter"],
    how="left",
)

variance = variance.merge(
    opex,
    on=["month", "quarter"],
    how="left",
)

# -----------------------------
# Budget gross profit
# -----------------------------

variance["budget_gross_profit"] = (
    variance["revenue_budget"]
    - variance["cogs_budget"]
)

# -----------------------------
# Variance calculations
# -----------------------------

variance["revenue_variance"] = (
    variance["revenue"]
    - variance["revenue_budget"]
)

variance["revenue_variance_pct"] = (
    variance["revenue_variance"]
    / variance["revenue_budget"]
    * 100
)

variance["units_variance"] = (
    variance["units"]
    - variance["units_budget"]
)

variance["units_variance_pct"] = (
    variance["units_variance"]
    / variance["units_budget"]
    * 100
)

variance["cogs_variance"] = (
    variance["cogs"]
    - variance["cogs_budget"]
)

variance["cogs_variance_pct"] = (
    variance["cogs_variance"]
    / variance["cogs_budget"]
    * 100
)

variance["gross_profit_variance"] = (
    variance["gross_profit"]
    - variance["budget_gross_profit"]
)

variance["gross_profit_variance_pct"] = (
    variance["gross_profit_variance"]
    / variance["budget_gross_profit"]
    * 100
)

variance["opex_variance"] = (
    variance["operating_expenses"]
    - variance["budget_opex"]
)

variance["opex_variance_pct"] = (
    variance["opex_variance"]
    / variance["budget_opex"]
    * 100
)

# -----------------------------
# Variance explanation
# -----------------------------

def explain_revenue(row):
    if row["revenue_variance_pct"] >= 3:
        return "Favorable revenue variance"
    elif row["revenue_variance_pct"] <= -3:
        return "Unfavorable revenue variance"
    return "Revenue broadly on budget"


def explain_cogs(row):
    if row["cogs_variance_pct"] <= -3:
        return "Favorable COGS variance"
    elif row["cogs_variance_pct"] >= 3:
        return "Unfavorable COGS variance"
    return "COGS broadly on budget"


def explain_opex(row):
    if row["opex_variance_pct"] <= -3:
        return "Favorable operating expense variance"
    elif row["opex_variance_pct"] >= 3:
        return "Unfavorable operating expense variance"
    return "Operating expenses broadly on budget"


variance["revenue_explanation"] = variance.apply(
    explain_revenue,
    axis=1,
)

variance["cogs_explanation"] = variance.apply(
    explain_cogs,
    axis=1,
)

variance["opex_explanation"] = variance.apply(
    explain_opex,
    axis=1,
)

# -----------------------------
# Save
# -----------------------------

variance.to_csv(
    "output/budget_vs_actual.csv",
    index=False,
)

# -----------------------------
# Print summary
# -----------------------------

print("Budget vs Actual analysis completed.")
print()

print(
    "Revenue variance: ${:,.2f}".format(
        variance["revenue_variance"].sum()
    )
)

print(
    "COGS variance: ${:,.2f}".format(
        variance["cogs_variance"].sum()
    )
)

print(
    "Gross profit variance: ${:,.2f}".format(
        variance["gross_profit_variance"].sum()
    )
)

print(
    "Operating expense variance: ${:,.2f}".format(
        variance["opex_variance"].sum()
    )
)

print()
print("Monthly variance report:")
print(
    variance[
        [
            "month",
            "revenue",
            "revenue_budget",
            "revenue_variance",
            "revenue_variance_pct",
            "gross_profit",
            "gross_profit_variance",
            "opex_variance",
        ]
    ].to_string(index=False)
)