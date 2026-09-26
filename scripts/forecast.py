import os
import pandas as pd
import numpy as np

os.makedirs("output", exist_ok=True)

monthly = pd.read_csv(
    "output/monthly_financials.csv"
)

monthly["month"] = pd.to_datetime(monthly["month"])

monthly = monthly.sort_values("month")

# --------------------------------
# 3-month rolling revenue average
# --------------------------------

monthly["rolling_3m_revenue"] = (
    monthly["revenue"]
    .rolling(window=3)
    .mean()
)

# --------------------------------
# Linear trend forecast
# --------------------------------

monthly["month_number"] = np.arange(
    1,
    len(monthly) + 1
)

x = monthly["month_number"].values
y = monthly["revenue"].values

slope, intercept = np.polyfit(
    x,
    y,
    1
)

monthly["trend_revenue"] = (
    intercept + slope * monthly["month_number"]
)

# --------------------------------
# Next 3 months
# --------------------------------

last_month = monthly["month"].max()

future_months = pd.date_range(
    last_month + pd.offsets.MonthBegin(1),
    periods=3,
    freq="MS"
)

future_numbers = np.arange(
    len(monthly) + 1,
    len(monthly) + 4
)

forecast = pd.DataFrame(
    {
        "month": future_months,
        "trend_forecast": (
            intercept + slope * future_numbers
        ),
    }
)

# Rolling average baseline
rolling_average = (
    monthly["revenue"]
    .tail(3)
    .mean()
)

forecast["rolling_average_forecast"] = (
    rolling_average
)

# Combined forecast
forecast["forecast_revenue"] = (
    forecast["trend_forecast"]
    + forecast["rolling_average_forecast"]
) / 2

# --------------------------------
# Save outputs
# --------------------------------

monthly.to_csv(
    "output/revenue_forecast_history.csv",
    index=False
)

forecast.to_csv(
    "output/revenue_forecast.csv",
    index=False
)

# --------------------------------
# Print results
# --------------------------------

print("Revenue forecast completed.")
print()

print(
    "3-month rolling average: ${:,.2f}".format(
        rolling_average
    )
)

print(
    "Trend slope: ${:,.2f} per month".format(
        slope
    )
)

print()
print("Next-quarter forecast:")

print(
    forecast[
        [
            "month",
            "trend_forecast",
            "rolling_average_forecast",
            "forecast_revenue",
        ]
    ].to_string(index=False)
)

print()
print(
    "Next-quarter forecast revenue: ${:,.2f}".format(
        forecast["forecast_revenue"].sum()
    )
)