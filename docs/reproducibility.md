# Reproducibility Guide

## 1. Environment

Use Python 3.10 or newer. From the repository root:

```bash
python -m venv .venv
```

Windows PowerShell: `\.venv\Scripts\Activate.ps1` (remove the leading slash when typing: `.venv\Scripts\Activate.ps1`).

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Run cleaning and EDA

```bash
python src/analysis_pipeline.py --input data/raw/snitch_fashion_sales_uncleaned.csv --output-dir outputs
```

This writes cleaned records, quality counts, monthly/category/city KPI tables, naive forecast predictions and metrics, and PNG charts into `outputs/`.

## 3. Compare forecasting baselines

After generating `outputs/monthly_kpis.csv`, run:

```bash
python src/forecasting.py --input outputs/monthly_kpis.csv --output-dir outputs --test-months 5
```

The comparison evaluates a one-step naive forecast and a seasonal-naive forecast using a chronological holdout. Seasonal-naive is scored only where a value from 12 months earlier exists. Compare metrics only across comparable periods.

## 4. Run tests

```bash
pytest -q
```

## 5. Interpretation safeguards

- The dataset is synthetic, not audited retailer data.
- Currency is unspecified; do not attach a currency symbol to totals.
- Missing discounts are assumed to be zero for derived sales.
- A high data-exclusion rate means category and trend results may be biased.
- Forecast performance on a short holdout is illustrative, not a production guarantee.
- Do not commit private customer information, API tokens, or virtual environments.

See [data README](../data/README.md) and [data dictionary](../data/data_dictionary.md) for source details and metric definitions.
