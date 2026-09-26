# FP&A Planning & Variance Analytics — Architecture

                    ┌─────────────────────┐
                    │   Raw Business Data │
                    │                     │
                    │ sales.csv           │
                    │ products.csv        │
                    │ budget.csv          │
                    │ expenses.csv        │
                    │ inventory.csv       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Financial Modeling │
                    │                     │
                    │ Revenue             │
                    │ COGS                │
                    │ Gross Profit        │
                    │ Gross Margin        │
                    │ Operating Income    │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                ▼              ▼              ▼
       ┌────────────────┐ ┌──────────────┐ ┌───────────────┐
       │ Budget vs      │ │ Forecasting  │ │ Profitability │
       │ Actual         │ │              │ │ Analysis      │
       │                │ │ Rolling Avg  │ │ SKU           │
       │ Variance $     │ │ Trend Model  │ │ Channel       │
       │ Variance %     │ │ Next Quarter │ │ Margin        │
       └───────┬────────┘ └──────┬───────┘ └───────┬───────┘
               │                 │                 │
               └─────────────────┼─────────────────┘
                                 ▼
                    ┌─────────────────────┐
                    │     SQLite DB       │
                    │                     │
                    │ Financial Reporting │
                    │ SQL Queries         │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │  Management Layer   │
                    │                     │
                    │ Streamlit Dashboard │
                    │ Management Report   │
                    └─────────────────────┘