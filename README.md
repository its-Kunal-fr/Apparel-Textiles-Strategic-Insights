# Apparel & Textiles Strategic Insights

An end-to-end business analytics project for a fictional apparel retailer, Threadline Apparel. It demonstrates how data collection, cleaning, integration, exploratory data analysis (EDA), KPI visualization, and demand forecasting can support merchandising and supply-chain decisions.

> **Evidence note:** This is an academic project. Numerical examples are illustrative unless explicitly calculated from a documented dataset. Simulated examples must not be presented as real company results.

## Business problem

Apparel retailers balance changing consumer demand with supplier lead times, seasonal buying, inventory availability, returns, discounts, and margin pressure. Fragmented sales, product, inventory, marketing, and supplier records make decisions harder.

## Objectives

- Establish a documented, repeatable data workflow.
- Clean and validate source data before analysis.
- Integrate sales and product information using stable identifiers.
- Explore sales, category, pricing, returns, and inventory patterns.
- Define actionable KPIs for a retail dashboard.
- Compare demand forecasts against a transparent baseline.
- Translate verified findings into practical recommendations.

## Project workflow

1. **Data collection:** document source files, fields, date coverage, permissions, and limitations.
2. **Data cleaning:** standardize types and labels; inspect missing values, duplicates, ranges, and keys.
3. **Data integration:** join sources using stable identifiers and validate row counts and totals.
4. **EDA:** analyze trends, category mix, product contribution, discounting, returns, and inventory risks.
5. **Visualization:** present decision-focused KPIs and drill-downs.
6. **Forecasting:** establish a baseline, validate on later periods, and assess MAE, WAPE, and bias.
7. **Recommendations:** connect each action to a measured result, owner, and success metric.

## Repository structure

- `data/` — source-data instructions and data governance
- `notebooks/` — planned, sequential analysis notebooks
- `src/` — reusable Python analysis pipeline
- `visualizations/` — charts and dashboard exports
- `reports/` — final report and evaluation summaries
- `requirements.txt` — Python dependencies

## Getting started

Python 3.10 or newer is recommended.

Create and activate a virtual environment, then install dependencies with:

```bash
pip install -r requirements.txt
```

The starter pipeline expects a CSV with `order_date`, `sku`, and `quantity` columns. Optional fields include `category`, `unit_price`, and `discount`.

```bash
python src/analysis_pipeline.py --input data/sales.csv --output-dir outputs
```

The command creates a cleaned dataset and summary tables. It does not create a forecast; forecasting should be evaluated separately on a time-based holdout period.

## Core KPI definitions

| KPI | Definition |
|---|---|
| Net sales | Gross item sales less discounts and refunds, using a documented policy |
| Gross margin % | (Net sales − cost of goods sold) / net sales × 100 |
| Units sold | Sum of valid sold quantities in the chosen period |
| Sell-through % | Units sold / units available to sell for a defined cohort and period |
| MAE | Mean absolute difference between actual and forecast demand |
| WAPE | Sum of absolute forecast errors / sum of actual demand × 100 |

Definitions must be aligned with the actual data and accounting rules before results are reported.

## Expected deliverables

- Data-quality and cleaning summary
- Integrated analytical dataset
- EDA tables and charts
- KPI dashboard or dashboard design
- Forecast baseline and time-based validation results
- Final strategic report with evidence-backed recommendations

## Limitations

This repository begins with a reusable workflow, not verified company data. Add the actual dataset source, licence details, date range, data dictionary, charts, and measured findings as the project progresses. Do not upload private customer data, credentials, or unlicensed datasets.

## Author

Academic portfolio project in apparel and textiles business analytics.
