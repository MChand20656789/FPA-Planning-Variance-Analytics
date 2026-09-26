import os
import random
from datetime import date

import numpy as np
import pandas as pd

random.seed(42)
np.random.seed(42)

os.makedirs("data", exist_ok=True)

# -----------------------------
# Products
# -----------------------------

products = [
    ("SKU001", "Organic Matcha", "Beverages", 18.00, 7.20),
    ("SKU002", "Mochi Snack", "Snacks", 12.00, 4.80),
    ("SKU003", "Protein Bar", "Snacks", 10.00, 4.10),
    ("SKU004", "Green Tea", "Beverages", 14.00, 5.60),
    ("SKU005", "Coconut Chips", "Snacks", 9.00, 3.70),
    ("SKU006", "Fruit Gummies", "Snacks", 8.00, 3.20),
    ("SKU007", "Coffee Blend", "Beverages", 16.00, 6.80),
    ("SKU008", "Oat Cookies", "Snacks", 11.00, 4.50),
    ("SKU009", "Electrolyte Mix", "Wellness", 20.00, 8.50),
    ("SKU010", "Collagen Powder", "Wellness", 28.00, 12.00),
    ("SKU011", "Chia Pudding", "Wellness", 13.00, 5.40),
    ("SKU012", "Almond Spread", "Pantry", 15.00, 6.20),
]

products_df = pd.DataFrame(
    products,
    columns=["sku", "product", "category", "selling_price", "unit_cogs"]
)

products_df.to_csv("data/products.csv", index=False)

# -----------------------------
# Sales
# -----------------------------

channels = ["E-commerce", "Retail", "Wholesale"]

months = pd.date_range("2025-01-01", "2025-12-01", freq="MS")

sales_rows = []

for month in months:
    quarter = f"Q{((month.month - 1) // 3) + 1}"

    for sku, product, category, price, unit_cogs in products:
        for channel in channels:
            base_units = random.randint(35, 120)

            # Seasonal effect
            seasonal_factor = {
                "Q1": 0.95,
                "Q2": 1.00,
                "Q3": 1.08,
                "Q4": 1.18,
            }[quarter]

            # Channel effect
            channel_factor = {
                "E-commerce": 1.10,
                "Retail": 1.00,
                "Wholesale": 0.85,
            }[channel]

            units = int(
                base_units
                * seasonal_factor
                * channel_factor
                * np.random.normal(1.0, 0.08)
            )

            units = max(units, 1)

            sales_rows.append(
                [
                    month.strftime("%Y-%m-%d"),
                    quarter,
                    sku,
                    channel,
                    units,
                    price,
                    unit_cogs,
                ]
            )

sales_df = pd.DataFrame(
    sales_rows,
    columns=[
        "month",
        "quarter",
        "sku",
        "channel",
        "units",
        "selling_price",
        "unit_cogs",
    ],
)

sales_df["revenue"] = sales_df["units"] * sales_df["selling_price"]
sales_df["cogs"] = sales_df["units"] * sales_df["unit_cogs"]

sales_df.to_csv("data/sales.csv", index=False)

# -----------------------------
# Budget
# -----------------------------

budget_rows = []

for month in months:
    quarter = f"Q{((month.month - 1) // 3) + 1}"

    monthly_sales = sales_df[sales_df["month"] == month.strftime("%Y-%m-%d")]

    actual_revenue = monthly_sales["revenue"].sum()
    actual_units = monthly_sales["units"].sum()
    actual_cogs = monthly_sales["cogs"].sum()

    # Budget deliberately differs from actuals.
    revenue_budget = actual_revenue * np.random.normal(1.04, 0.025)
    units_budget = actual_units * np.random.normal(1.03, 0.02)
    cogs_budget = actual_cogs * np.random.normal(0.98, 0.02)

    budget_rows.append(
        [
            month.strftime("%Y-%m-%d"),
            quarter,
            round(revenue_budget, 2),
            round(units_budget, 0),
            round(cogs_budget, 2),
        ]
    )

budget_df = pd.DataFrame(
    budget_rows,
    columns=[
        "month",
        "quarter",
        "revenue_budget",
        "units_budget",
        "cogs_budget",
    ],
)

budget_df.to_csv("data/budget.csv", index=False)

# -----------------------------
# Operating Expenses
# -----------------------------

departments = {
    "Marketing": 5000,
    "Sales": 6500,
    "Operations": 5500,
    "Corporate": 4000,
}

expense_rows = []

for month in months:
    quarter = f"Q{((month.month - 1) // 3) + 1}"

    for department, base_expense in departments.items():
        actual_expense = base_expense * np.random.normal(1.0, 0.08)

        expense_rows.append(
            [
                month.strftime("%Y-%m-%d"),
                quarter,
                department,
                round(actual_expense, 2),
            ]
        )

expenses_df = pd.DataFrame(
    expense_rows,
    columns=["month", "quarter", "department", "actual_expense"],
)

expenses_df["budget_expense"] = (
    expenses_df["actual_expense"]
    * np.random.normal(1.02, 0.025, len(expenses_df))
).round(2)

expenses_df.to_csv("data/expenses.csv", index=False)

# -----------------------------
# Inventory
# -----------------------------

inventory_rows = []

for sku, product, category, price, unit_cogs in products:
    beginning_inventory = random.randint(250, 700)
    units_sold = int(sales_df[sales_df["sku"] == sku]["units"].sum())

    ending_inventory = max(
        beginning_inventory - int(units_sold * 0.65),
        25
    )

    inventory_rows.append(
        [
            sku,
            product,
            category,
            beginning_inventory,
            units_sold,
            ending_inventory,
            round(ending_inventory * unit_cogs, 2),
        ]
    )

inventory_df = pd.DataFrame(
    inventory_rows,
    columns=[
        "sku",
        "product",
        "category",
        "beginning_inventory",
        "units_sold",
        "ending_inventory",
        "ending_inventory_value",
    ],
)

inventory_df.to_csv("data/inventory.csv", index=False)

print("FP&A sample data generated successfully.")
print(f"Products: {len(products_df)}")
print(f"Sales records: {len(sales_df)}")
print(f"Budget records: {len(budget_df)}")
print(f"Expense records: {len(expenses_df)}")
print(f"Inventory records: {len(inventory_df)}")