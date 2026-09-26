import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="FP&A Planning & Variance Analytics",
    layout="wide"
)

# --------------------------------------------------
# Load data
# --------------------------------------------------

monthly = pd.read_csv("output/monthly_financials.csv")
variance = pd.read_csv("output/budget_vs_actual.csv")
sku = pd.read_csv("output/sku_financials.csv")
channel = pd.read_csv("output/channel_financials.csv")
forecast = pd.read_csv("output/revenue_forecast.csv")
expenses = pd.read_csv("data/expenses.csv")

monthly["month"] = pd.to_datetime(monthly["month"])
variance["month"] = pd.to_datetime(variance["month"])
forecast["month"] = pd.to_datetime(forecast["month"])

# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("FP&A Planning & Variance Analytics")

st.caption(
    "Financial planning, profitability, budget variance, "
    "and revenue forecasting dashboard"
)

# --------------------------------------------------
# KPI calculations
# --------------------------------------------------

total_revenue = monthly["revenue"].sum()
total_cogs = monthly["cogs"].sum()
gross_profit = monthly["gross_profit"].sum()
gross_margin = gross_profit / total_revenue
operating_expense = monthly["operating_expenses"].sum()
operating_income = monthly["operating_income"].sum()

revenue_variance = variance["revenue_variance"].sum()
forecast_revenue = forecast["forecast_revenue"].sum()

# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Revenue",
        f"${total_revenue:,.0f}"
    )

with col2:
    st.metric(
        "Gross Profit",
        f"${gross_profit:,.0f}"
    )

with col3:
    st.metric(
        "Gross Margin",
        f"{gross_margin:.1%}"
    )

with col4:
    st.metric(
        "Budget Variance",
        f"${revenue_variance:,.0f}"
    )

with col5:
    st.metric(
        "Next-Quarter Forecast",
        f"${forecast_revenue:,.0f}"
    )

# --------------------------------------------------
# Management summary
# --------------------------------------------------

st.subheader("Management Summary")

st.write(
    f"""
Revenue totaled **${total_revenue:,.0f}** with gross profit of
**${gross_profit:,.0f}** and a gross margin of **{gross_margin:.1%}**.

Revenue was **${abs(revenue_variance):,.0f}**
{"below" if revenue_variance < 0 else "above"} budget.

The next-quarter revenue forecast is
**${forecast_revenue:,.0f}**, based on a combination of recent
three-month performance and the historical revenue trend.
"""
)

# --------------------------------------------------
# Revenue trend
# --------------------------------------------------

st.subheader("Revenue Trend")

fig = px.line(
    monthly,
    x="month",
    y="revenue",
    markers=True,
    title="Monthly Revenue"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Actual vs Budget
# --------------------------------------------------

st.subheader("Actual Revenue vs Budget")

budget_chart = variance[
    [
        "month",
        "revenue",
        "revenue_budget"
    ]
].melt(
    id_vars="month",
    var_name="type",
    value_name="amount"
)

budget_chart["type"] = budget_chart["type"].replace(
    {
        "revenue": "Actual",
        "revenue_budget": "Budget"
    }
)

fig = px.line(
    budget_chart,
    x="month",
    y="amount",
    color="type",
    markers=True,
    title="Actual vs Budget Revenue"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Revenue ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Forecast
# --------------------------------------------------

st.subheader("Revenue Forecast")

forecast_chart = forecast[
    [
        "month",
        "trend_forecast",
        "rolling_average_forecast",
        "forecast_revenue"
    ]
].melt(
    id_vars="month",
    var_name="forecast_type",
    value_name="revenue"
)

forecast_chart["forecast_type"] = forecast_chart[
    "forecast_type"
].replace(
    {
        "trend_forecast": "Trend Forecast",
        "rolling_average_forecast": "3-Month Average",
        "forecast_revenue": "Combined Forecast"
    }
)

fig = px.line(
    forecast_chart,
    x="month",
    y="revenue",
    color="forecast_type",
    markers=True,
    title="Next-Quarter Revenue Forecast"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Forecast Revenue ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Profitability by channel
# --------------------------------------------------

st.subheader("Profitability by Channel")

fig = px.bar(
    channel,
    x="channel",
    y="gross_profit",
    title="Gross Profit by Sales Channel",
    text_auto=".2s"
)

fig.update_layout(
    xaxis_title="Sales Channel",
    yaxis_title="Gross Profit ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Gross margin by SKU
# --------------------------------------------------

st.subheader("Gross Margin by SKU")

sku_sorted = sku.sort_values(
    "gross_margin_pct",
    ascending=False
)

fig = px.bar(
    sku_sorted,
    x="sku",
    y="gross_margin_pct",
    title="Gross Margin by Product",
    text_auto=".1%"
)

fig.update_layout(
    xaxis_title="SKU",
    yaxis_title="Gross Margin"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Operating expense analysis
# --------------------------------------------------

st.subheader("Operating Expenses by Department")

department_expenses = (
    expenses
    .groupby("department", as_index=False)
    .agg(
        actual_expense=("actual_expense", "sum"),
        budget_expense=("budget_expense", "sum")
    )
)

department_expenses["variance"] = (
    department_expenses["actual_expense"]
    - department_expenses["budget_expense"]
)

fig = px.bar(
    department_expenses,
    x="department",
    y=["actual_expense", "budget_expense"],
    barmode="group",
    title="Actual vs Budget Operating Expenses"
)

fig.update_layout(
    xaxis_title="Department",
    yaxis_title="Expense ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Budget variance
# --------------------------------------------------

st.subheader("Budget Variance")

variance_chart = variance[
    [
        "month",
        "revenue_variance",
        "gross_profit_variance",
        "opex_variance"
    ]
].melt(
    id_vars="month",
    var_name="metric",
    value_name="variance"
)

fig = px.bar(
    variance_chart,
    x="month",
    y="variance",
    color="metric",
    barmode="group",
    title="Monthly Financial Variances"
)

fig.update_layout(
    xaxis_title="Month",
    yaxis_title="Variance ($)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# --------------------------------------------------
# Management table
# --------------------------------------------------

st.subheader("Product Profitability Management View")

management = sku[
    [
        "sku",
        "revenue",
        "cogs",
        "gross_profit",
        "gross_margin_pct"
    ]
].copy()

management = management.sort_values(
    "gross_profit",
    ascending=False
)

for _, row in management.iterrows():

    st.write(
        f"**{row['sku']}**  |  "
        f"Revenue: ${row['revenue']:,.0f}  |  "
        f"COGS: ${row['cogs']:,.0f}  |  "
        f"Gross Profit: ${row['gross_profit']:,.0f}  |  "
        f"Margin: {row['gross_margin_pct']:.1%}"
    )