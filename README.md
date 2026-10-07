# Smart Sales Intelligence Dashboard

**End-to-end data analytics project** — Python EDA, SQL analysis, Power BI dashboard, and a natural-language AI query agent, built on the real **Sample Superstore** dataset (9,994 records, 2014–2017).

> A portfolio project demonstrating the complete data analyst workflow: data preparation → exploratory analysis → SQL business queries → BI dashboarding → AI-powered querying.

---

## Business Problem

A mid-sized retail company wants to understand **what drives its revenue and profit** across categories, regions, customers, and time — and identify where margins are leaking. This project turns raw transaction data into actionable business intelligence.

**Key questions answered:**
- Which categories and regions drive revenue vs profit?
- How do discounts affect profit margins?
- Who are the most valuable customers?
- What are the seasonal and year-over-year trends?
- Which products are profitable vs loss-making?

---

## Tech Stack

| Layer | Tools |
|-------|-------|
| Data Processing | Python, Pandas, NumPy |
| Visualization | Matplotlib, Seaborn |
| Database & Analysis | SQL (SQLite), Window functions, CTEs |
| Business Intelligence | Power BI (star schema, DAX) |
| AI Agent | Python (rule-based NLP, no API key needed) |
| Data Source | Real **Sample Superstore** dataset (9,994 records, 2014–2017) |

---

## Project Structure

```
sales_analytics_project/
├── data/
│   ├── generate_dataset.py          # synthetic dataset generator
│   ├── raw_sales_data.csv           # 5,000 raw records
│   ├── cleaned_sales_data.csv       # cleaned + 29 engineered features
│   └── sales.db                     # SQLite database
├── python/
│   ├── 01_data_cleaning.py          # audit, clean, feature engineering
│   ├── 02_eda.py                    # 12 visualizations + insights
│   └── 03_sql_analysis.py           # loads DB + runs 15 SQL queries
├── sql/
│   └── analysis_queries.sql         # 15 documented business queries
├── ai_agent/
│   └── agent.py                     # natural-language data query agent
├── powerbi/
│   ├── prepare_powerbi_data.py      # builds star-schema tables
│   ├── data_model/                  # fact + dimension CSVs
│   ├── DAX_measures.txt             # 30+ ready-to-paste DAX measures
│   ├── DASHBOARD_BUILD_GUIDE.md     # step-by-step dashboard guide
│   └── theme.json                   # Power BI color theme
├── outputs/
│   ├── plots/                       # 12 PNG visualizations
│   └── reports/                     # insights + SQL results + quality report
└── README.md
```

---

## How to Run

```bash
# 1. Generate the dataset
python data/generate_dataset.py

# 2. Clean and engineer features
python python/01_data_cleaning.py

# 3. Run EDA and generate all visualizations
python python/02_eda.py

# 4. Load into SQL and run 15 business queries
python python/03_sql_analysis.py

# 5. Prepare Power BI star-schema data
python powerbi/prepare_powerbi_data.py

# 6. Launch the AI agent (interactive)
python ai_agent/agent.py
```

**Requirements:** `pip install pandas numpy matplotlib seaborn`

---

## Dataset Overview

This project uses the real **Sample Superstore** dataset (the classic Tableau/Kaggle
retail dataset). The raw file is adapted to the project schema by
[`data/adapt_superstore.py`](data/adapt_superstore.py), which renames columns and
derives `unit_price` and `profit_margin`.

- **9,994** order records | **2014–2017** (4 years)
- **~800** unique customers | **1,850** products | **3** categories
  (Furniture, Office Supplies, Technology)
- **4** regions (Central, East, South, West), 500+ US cities
- **$2.30 M** total revenue | **$0.29 M** total profit | **12.5%** overall margin

**Engineered features:** date parts, days-to-ship, discount bands, sales bands, customer LTV, customer tier, revenue share, profitability flag.

> To reproduce: place `Superstore_full.csv` (the 21-column Sample Superstore file)
> in `data/`, then run the pipeline — `data/adapt_superstore.py` converts it automatically.

---

## Key Insights

### 1. Furniture is a margin trap
Furniture makes up ~32% of revenue but earns only a **2% profit margin** ($18K profit on
$742K sales), while Technology and Office Supplies both run **~17%**.
→ *Recommendation: Renegotiate furniture costs/pricing or reduce its discounting.*

### 2. Discounts push orders into losses
No-discount orders average a **34% margin**. Orders discounted above 20% turn **negative**
(-11.6%), and above 30% collapse to **-91.5%** — the store loses money on heavily
discounted orders.
→ *Recommendation: Cap discounts at ~20%; audit the deep-discount orders.*

### 3. Q4 seasonality is significant
Q4 (Oct–Dec) contributes **~38% of annual revenue**.
→ *Recommendation: Concentrate inventory and marketing spend ahead of Q4.*

### 4. West leads, Central lags on profitability
West achieves the highest effective margin (**14.9%**) while Central trails at **7.9%**.
→ *Recommendation: Investigate Central's discounting and product mix.*

### 5. Pareto principle in customers
A small set of customers (e.g. Sean Miller, Tamara Chand, Raymond Buch) drive a
disproportionate share of revenue.
→ *Recommendation: Launch a tiered loyalty program for top customers.*

Full insights: [`outputs/reports/key_insights.txt`](outputs/reports/key_insights.txt)

---

## SQL Analysis Highlights

15 documented queries in [`sql/analysis_queries.sql`](sql/analysis_queries.sql), covering:

- **Aggregations & HAVING** — category summaries, high-value customers
- **Window functions** — `RANK`, `DENSE_RANK`, `ROW_NUMBER`, `LAG`, `FIRST_VALUE`
- **CTEs** — single and chained (regional scorecard)
- **Subqueries** — correlated (customers vs segment average)
- **Running totals** — cumulative YTD revenue
- **CASE WHEN** — conditional aggregation / quarterly pivots
- **INTERSECT** — customer retention analysis
- **Date functions** — monthly/quarterly/yearly trends

Example — Month-over-Month growth with `LAG`:
```sql
WITH monthly AS (
    SELECT order_year, order_month, ROUND(SUM(sales),0) AS revenue
    FROM sales GROUP BY order_year, order_month
),
with_lag AS (
    SELECT *, LAG(revenue) OVER (ORDER BY order_year, order_month) AS prev_revenue
    FROM monthly
)
SELECT order_year, order_month, revenue, prev_revenue,
       ROUND((revenue - prev_revenue) * 100.0 / prev_revenue, 1) AS mom_growth_pct
FROM with_lag WHERE prev_revenue IS NOT NULL;
```

---

## Visualizations

12 publication-quality charts in [`outputs/plots/`](outputs/plots/):

| # | Chart | # | Chart |
|---|-------|---|-------|
| 01 | Monthly revenue trend | 07 | Shipping analysis |
| 02 | Category performance | 08 | Customer segments |
| 03 | Regional analysis | 09 | Quarterly heatmap |
| 04 | Discount impact | 10 | YoY growth by category |
| 05 | Top customers | 11 | Correlation matrix |
| 06 | Product profitability | 12 | Executive summary dashboard |

---

## AI Sales Agent

A natural-language query agent that answers business questions in plain English — **no API key or internet required** (rule-based intent classification).

```
Your question: which region has the highest profit margin?

============================================================
  Profit Margin by Region
============================================================
  West       ████████████████████ 35.1%  (Profit: Rs.50.3 L)
  South      ████████████████     32.8%  ...
  ...
```

**Supported questions:** revenue/profit by region or category, top customers/products, discount impact, quarterly/yearly comparisons, shipping analysis, executive summary, and more. Type `help` in the agent to see all.

```bash
python ai_agent/agent.py          # interactive
python ai_agent/agent.py --demo   # guided demo
```

---

## Power BI Dashboard

A 4-page interactive dashboard built on a **star-schema data model**.

### Page 1 — Executive Overview
KPIs, monthly revenue trend, category and region breakdown.

![Executive Overview](powerbi/screenshots/page1_executive_overview.png)

### Page 2 — Regional & Geographic Analysis
Map by city, revenue-vs-profit by region, region scorecard, AOV by region.

![Regional Analysis](powerbi/screenshots/page2_regional_analysis.png)

### Page 3 — Product & Category Deep Dive
Top products, category treemap, profit margin by category, product detail table.

![Product Deep Dive](powerbi/screenshots/page3_product_deep_dive.png)

### Page 4 — Customer & Discount Analysis
Customer segments, top customers, the discount-vs-margin combo chart, customer tiers.

![Customer & Discount](powerbi/screenshots/page4_customer_discount.png)

The build package includes:
- Star-schema CSVs (`powerbi/data_model/`)
- DAX measures (`powerbi/DAX_measures.txt`) — including time-intelligence (YoY, MoM, YTD)
- Step-by-step build guide (`powerbi/DASHBOARD_BUILD_GUIDE.md`)
- Custom color theme (`powerbi/theme.json`)

---

## Skills Demonstrated

- **Data cleaning & feature engineering** — data quality audits, derived features
- **Exploratory data analysis** — trend, distribution, correlation, segmentation
- **SQL proficiency** — window functions, CTEs, subqueries, conditional aggregation
- **Dimensional modeling** — star schema for BI
- **DAX & time intelligence** — YoY/MoM/YTD measures
- **Business storytelling** — translating data into recommendations
- **Automation** — reproducible end-to-end pipeline

---

## Author

**Manya Kumar**
B.Tech, IIT (ISM) Dhanbad | BS Data Science, IIT Madras

---

*This project uses the real **Sample Superstore** dataset (a widely used public retail dataset). The raw CSV is adapted to the project schema by `data/adapt_superstore.py`. The synthetic generator (`data/generate_dataset.py`) is retained as an optional fallback.*
