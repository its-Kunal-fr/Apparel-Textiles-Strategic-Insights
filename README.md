# Apparel & Textiles Strategic Insights

An end-to-end analytics project for a fictional apparel retailer using a publicly shared **synthetic** fashion-sales dataset. The project demonstrates source documentation, data cleaning, KPI calculations, EDA visualizations, chronological baseline forecasting, and strategic recommendations.

> **Important:** The source data is explicitly described by its publisher as synthetic. Results demonstrate analytical methods and are not claims about a real retailer. The source currency is unspecified.

## Dataset
Source repository: [Wattzp/Snitch-Clothing-Sales](https://github.com/Wattzp/Snitch-Clothing-Sales)  
Original dataset: [Snitch_Fashion_Sales_Uncleaned.csv](https://github.com/Wattzp/Snitch-Clothing-Sales/blob/main/Snitch_Fashion_Sales_Uncleaned.csv)  
A copy with customer names removed is stored at [data/raw/snitch_fashion_sales_uncleaned.csv](data/raw/snitch_fashion_sales_uncleaned.csv).

## Measured results on the cleaned subset
- 2,500 source rows; 283 rows retained by the documented primary KPI rules (11.32%).
- Calculated sales: 2,291,800.92 source currency units across 978 units.
- Accessories is the largest category in the retained subset at 485,867.32 source currency units.
- One-step naive forecast evaluated on the final five months: MAE 24,655.09 and WAPE 20.00%.

These numbers are limited by missing and invalid data; see the report for caveats.

## Visual results
- [Monthly estimated sales chart](visualizations/monthly_sales.svg)
- [Estimated sales by category chart](visualizations/category_sales.svg)
- [Forecast versus actual chart](visualizations/forecast_holdout.svg)

## Project workflow
1. Data source and quality review
2. Cleaning and normalization
3. EDA and category/monthly/city KPI tables
4. Chronological naive forecast baseline
5. Strategic recommendations and final report

## Run the pipeline
Python 3.10 or newer is recommended.

```bash
pip install -r requirements.txt
python src/analysis_pipeline.py --input data/raw/snitch_fashion_sales_uncleaned.csv --output-dir outputs
```

The pipeline writes cleaned rows, quality checks, KPI tables, holdout predictions and metrics, and PNG charts. Generated outputs are ignored by Git so raw or derived data is not accidentally committed wholesale.

## Limitations
- The dataset is synthetic.
- Only 11.32% of source rows passed the primary KPI rules.
- Currency and profit definitions are unspecified.
- The forecast holdout has five months, so error estimates are unstable.
- Inventory, return, cost, and supplier tables are not provided.

See [reports/analysis_findings.md](reports/analysis_findings.md) for the complete Week 6 strategic analysis.
