# Visualizations

Charts in this folder are calculated from the cleaned subset of the synthetic fashion retail dataset documented in `../data/README.md`.

- [Monthly estimated sales](monthly_sales.svg) — July 2023 to July 2025.
- [Estimated sales by product category](category_sales.svg) — totals for retained rows.
- [Naive forecast vs actual](forecast_holdout.svg) — final five months held out chronologically.

The source currency is unspecified. Sales are calculated as units × unit price × (1 − discount), treating missing discount as zero and excluding invalid discounts. These are demonstration outputs, not evidence of real retailer performance.

Run `python src/analysis_pipeline.py --input data/raw/snitch_fashion_sales_uncleaned.csv --output-dir outputs` to generate PNG charts and CSV tables from the data.
