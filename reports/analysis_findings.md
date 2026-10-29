# Week 6 — Apparel & Textiles Strategic Analysis

## Executive summary

This report demonstrates an end-to-end retail analytics workflow using a publicly shared **synthetic** fashion-sales dataset. The source repository explicitly describes the data as synthetic and intentionally uncleaned. Findings below describe the retained sample after the documented cleaning rules; they are not claims about the real performance of a retailer.

The source file contained 2,500 rows. Applying the main analysis rules retained 283 rows (11.32%). The high exclusion rate is itself a major finding: the source is too incomplete for confident operational decisions without better source-data controls. Estimated sales are recalculated from positive units, positive unit prices, and valid discounts, rather than trusting the source Sales_Amount column, which contains many zero values.

## Dataset and method

**Source:** [Wattzp/Snitch-Clothing-Sales](https://github.com/Wattzp/Snitch-Clothing-Sales), file [Snitch_Fashion_Sales_Uncleaned.csv](https://github.com/Wattzp/Snitch-Clothing-Sales/blob/main/Snitch_Fashion_Sales_Uncleaned.csv).

The source README identifies this as synthetic practice data. Customer names were removed from the copy committed to this repository. Date parsing uses day-first interpretation for ambiguous dates. Rows are retained for the primary KPI analysis only when the date is parseable, quantity and unit price are positive, and discount is missing or lies from 0 to 1. Missing discounts are treated as zero for derived sales, and this assumption is documented.

Derived sales = units sold × unit price × (1 − discount). The source does not specify a currency, so monetary totals are reported in source units without a currency symbol. Source-reported Profit is not treated as independently validated margin because item costs and accounting definitions are not provided.

## Data quality results

| Check | Count / result |
|---|---:|
| Source rows | 2,500 |
| Rows retained for primary KPI analysis | 283 |
| Retained share | 11.32% |
| Missing or unparseable dates | 606 |
| Missing quantities | 1,306 |
| Non-positive quantities | 412 |
| Missing unit prices | 1,210 |
| Invalid discount values outside 0–1 | 189 |

These issue counts overlap; they must not be added together to infer the number of distinct rejected rows. Rows with missing discounts are kept with a zero-discount assumption; rows with invalid discounts are excluded. Non-positive quantities are excluded rather than converted to sales. The cleaning script exports a full data-quality summary when run.

## Observed results on the retained sample

- **283** transaction rows were retained across **25** months, from July 2023 to July 2025.
- Calculated sales total approximately **2,291,800.92 source currency units** across **978 units**.
- The largest category by calculated sales was **Accessories** (485,867.32; 21.2% of retained calculated sales), followed by Dresses (426,314.01) and Shoes (408,778.70).
- Category sales totals: Accessories 485,867.32; Dresses 426,314.01; Shoes 408,778.70; Jeans 352,928.10; T-Shirts 318,197.69; Jackets 299,715.10.
- City labels are inconsistent in the source. Common aliases (Bangalore/bengaluru, Hyd/Hyderabad, and hyderbad/Hyderabad) should be standardized before interpreting regional rankings.

These results describe only the cleaned subset. Because almost 89% of source rows do not meet the primary analysis criteria, category rankings and totals may be biased by missingness and should be treated as a demonstration rather than a reliable market estimate.

## Demand forecasting baseline

A one-step naive forecast was evaluated chronologically: each test month's estimate equals the previous month's observed calculated sales. The final 20% of the 25 available months (5 months) were held out from the earlier 20 months.

| Holdout month | Actual calculated sales | Naive forecast |
|---|---:|---:|
| 2025-03 | 105,665.16 | 84,303.42 |
| 2025-04 | 110,191.96 | 105,665.16 |
| 2025-05 | 146,660.02 | 110,191.96 |
| 2025-06 | 113,191.81 | 146,660.02 |
| 2025-07 | 140,642.46 | 113,191.81 |

- **Holdout MAE:** 24,655.09 source currency units per month
- **Holdout WAPE:** 20.00%

This is a baseline, not evidence that the model is production-ready. With only five test months and a high data-exclusion rate, performance estimates are unstable. A next iteration should compare seasonal-naive and moving-average baselines, preserve a chronological split, and report errors by category where the data supports it.

## Strategic recommendations

1. **Fix data capture before automating decisions.** Require order date, SKU/product, quantity, unit price, discount convention, and order identifier. Add validation at ingestion and monitor completeness weekly. Success metric: share of records passing the agreed schema and business rules.
2. **Create a documented sales metric.** Reconcile gross sales, discounts, returns/refunds, tax, and currency with finance. The source's precomputed sales field is not reliable enough to use as-is. Success metric: unexplained variance between transaction-level and finance totals.
3. **Standardize product and location dimensions.** Maintain controlled category and city dictionaries instead of manually merging inconsistent spellings. Success metric: proportion of records mapped to approved dimension values.
4. **Use category rankings as a hypothesis, not a buying instruction.** Accessories leads the retained sample, but missingness may distort the result. Recalculate category performance after source quality improves and include gross margin, return rate, stock availability, and seasonality.
5. **Adopt forecasting only after baseline validation.** Monitor MAE and WAPE against the naive benchmark over a rolling holdout; compare seasonal-naive and moving-average alternatives. Do not use forecasts for purchase orders until data completeness and stability are adequate.
6. **Build a decision-focused dashboard.** Show calculated net sales, units, order count, category mix, data-quality completeness, and forecast error. Include a visible data-quality warning when the retained share falls below an agreed threshold.

## Limitations

- The source explicitly labels itself synthetic; no real retailer conclusions should be drawn.
- Only 283 of 2,500 rows passed the primary KPI filters.
- The source currency is unspecified.
- Missing discount values are treated as zero for calculated sales; results may change if the actual convention differs.
- Reported profit lacks cost and accounting definitions and is not used as a verified margin KPI.
- The holdout contains five months only.
- No inventory, return, supplier lead-time, marketing-spend, or product-cost tables were provided; inventory and profitability recommendations require those sources.

## Reproducibility

From the repository root, install dependencies and run:

```bash
pip install -r requirements.txt
python src/analysis_pipeline.py --input data/raw/snitch_fashion_sales_uncleaned.csv --output-dir outputs
```

The script writes cleaned data, quality checks, monthly/category/city KPI tables, holdout forecast predictions and metrics, and PNG charts. The committed summary above records the current calculation from the source snapshot and should be regenerated if the dataset or cleaning rules change.
