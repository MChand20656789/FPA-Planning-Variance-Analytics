-- ============================================
-- FP&A Financial Reporting Queries
-- ============================================


-- 1. Monthly P&L
-- --------------------------------------------

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


-- 2. Product Profitability
-- --------------------------------------------

SELECT
    sku,
    units,
    revenue,
    cogs,
    gross_profit,
    gross_margin_pct
FROM sku_financials
ORDER BY gross_profit DESC;


-- 3. Channel Profitability
-- --------------------------------------------

SELECT
    channel,
    units,
    revenue,
    cogs,
    gross_profit,
    gross_margin_pct
FROM channel_financials
ORDER BY gross_profit DESC;


-- 4. Largest Revenue Variances
-- --------------------------------------------

SELECT
    month,
    revenue,
    revenue_budget,
    revenue_variance,
    revenue_variance_pct
FROM budget_vs_actual
ORDER BY revenue_variance ASC;


-- 5. Gross Profit Variance
-- --------------------------------------------

SELECT
    month,
    gross_profit,
    budget_gross_profit,
    gross_profit_variance,
    gross_profit_variance_pct
FROM budget_vs_actual
ORDER BY gross_profit_variance ASC;


-- 6. Operating Expense Variance
-- --------------------------------------------

SELECT
    month,
    operating_expenses,
    budget_opex,
    opex_variance,
    opex_variance_pct
FROM budget_vs_actual
ORDER BY opex_variance ASC;


-- 7. Highest-Margin Products
-- --------------------------------------------

SELECT
    sku,
    revenue,
    cogs,
    gross_profit,
    gross_margin_pct
FROM sku_financials
ORDER BY gross_margin_pct DESC;


-- 8. Revenue by Channel
-- --------------------------------------------

SELECT
    channel,
    SUM(revenue) AS total_revenue,
    SUM(units) AS total_units
FROM sales
GROUP BY channel
ORDER BY total_revenue DESC;


-- 9. Monthly Revenue Change
-- --------------------------------------------

SELECT
    month,
    revenue,
    revenue - LAG(revenue) OVER (
        ORDER BY month
    ) AS revenue_change
FROM monthly_financials
ORDER BY month;


-- 10. Management Summary
-- --------------------------------------------

SELECT
    SUM(revenue) AS actual_revenue,
    SUM(revenue_budget) AS budget_revenue,
    SUM(revenue_variance) AS total_revenue_variance,

    SUM(gross_profit) AS actual_gross_profit,
    SUM(budget_gross_profit) AS budget_gross_profit,
    SUM(gross_profit_variance) AS total_gross_profit_variance,

    SUM(operating_expenses) AS actual_opex,
    SUM(budget_opex) AS budget_opex,
    SUM(opex_variance) AS total_opex_variance

FROM budget_vs_actual;