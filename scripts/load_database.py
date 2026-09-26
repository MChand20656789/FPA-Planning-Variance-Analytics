import os
import sqlite3
import pandas as pd

# --------------------------------------------------
# Paths
# --------------------------------------------------

DATA_DIR = "data"
OUTPUT_DIR = "output"

os.makedirs(OUTPUT_DIR, exist_ok=True)

DB_PATH = os.path.join(
    OUTPUT_DIR,
    "fpa.db"
)

# --------------------------------------------------
# Connect to SQLite database
# --------------------------------------------------

connection = sqlite3.connect(DB_PATH)

# --------------------------------------------------
# Load raw data
# --------------------------------------------------

sales = pd.read_csv(
    os.path.join(DATA_DIR, "sales.csv")
)

products = pd.read_csv(
    os.path.join(DATA_DIR, "products.csv")
)

budget = pd.read_csv(
    os.path.join(DATA_DIR, "budget.csv")
)

expenses = pd.read_csv(
    os.path.join(DATA_DIR, "expenses.csv")
)

inventory = pd.read_csv(
    os.path.join(DATA_DIR, "inventory.csv")
)

# --------------------------------------------------
# Load calculated financial outputs
# --------------------------------------------------

sku_financials = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "sku_financials.csv"
    )
)

channel_financials = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "channel_financials.csv"
    )
)

monthly_financials = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "monthly_financials.csv"
    )
)

budget_vs_actual = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "budget_vs_actual.csv"
    )
)

revenue_forecast_history = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "revenue_forecast_history.csv"
    )
)

revenue_forecast = pd.read_csv(
    os.path.join(
        OUTPUT_DIR,
        "revenue_forecast.csv"
    )
)

# --------------------------------------------------
# Write tables to SQLite
# --------------------------------------------------

tables = {
    "sales": sales,
    "products": products,
    "budget": budget,
    "expenses": expenses,
    "inventory": inventory,
    "sku_financials": sku_financials,
    "channel_financials": channel_financials,
    "monthly_financials": monthly_financials,
    "budget_vs_actual": budget_vs_actual,
    "revenue_forecast_history": revenue_forecast_history,
    "revenue_forecast": revenue_forecast,
}

for table_name, dataframe in tables.items():

    dataframe.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

# --------------------------------------------------
# Verify database
# --------------------------------------------------

cursor = connection.cursor()

cursor.execute(
    """
    SELECT name
    FROM sqlite_master
    WHERE type = 'table'
    ORDER BY name;
    """
)

database_tables = cursor.fetchall()

print("SQLite database created successfully.")
print()
print(f"Database: {DB_PATH}")
print()
print("Tables:")

for table in database_tables:
    print(f"- {table[0]}")

print()

for table_name, dataframe in tables.items():

    cursor.execute(
        f"SELECT COUNT(*) FROM {table_name}"
    )

    row_count = cursor.fetchone()[0]

    print(
        f"{table_name}: "
        f"{row_count:,} rows"
    )

connection.close()

print()
print("Database connection closed.")