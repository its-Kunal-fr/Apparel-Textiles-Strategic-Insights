# Dataset and data governance

## Included dataset
- File: `raw/snitch_fashion_sales_uncleaned.csv`
- Source repository: https://github.com/Wattzp/Snitch-Clothing-Sales
- Original file: https://github.com/Wattzp/Snitch-Clothing-Sales/blob/main/Snitch_Fashion_Sales_Uncleaned.csv
- The source repository describes these records as a **synthetic dataset** for retail data-cleaning and EDA practice.
- Customer names were removed before this copy was committed. Other source fields were retained for analysis.
- The source repository states MIT; verify its current licence before redistribution or reuse.

This is not real company transaction data. It demonstrates an analytics workflow and must not be used to claim actual retailer performance.

## Known data issues
The source includes missing dates, missing or non-positive quantities, missing prices, discount values outside 0–1, inconsistent city spellings, and a precomputed Sales_Amount field that is often zero. The analysis recalculates estimated sales from quantity, price, and valid discount rather than treating that source field as authoritative.

## Cleaning policy
1. Parse supported date formats; ambiguous dates are interpreted day-first and should be checked against source documentation.
2. Keep rows with a valid date, positive quantity, positive unit price, and discount between 0 and 1; missing discount is treated as zero for the derived-sales example.
3. Normalize common city aliases such as Bangalore/bengaluru and Hyd/Hyderabad.
4. Calculate estimated item sales as units × unit price × (1 − discount).
5. Do not impute missing quantity or price for the main KPI analysis.
6. Treat reported Profit as source-provided; it is not independently validated because cost details are unavailable.

See `../reports/analysis_findings.md` for measured results and limitations.
