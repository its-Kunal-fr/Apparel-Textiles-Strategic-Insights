# Data

Place permitted source datasets in this folder locally. Do not commit confidential, personal, or unlicensed data.

## Suggested sources
- Sales transactions: order date, SKU, quantity, price, discount, channel
- Product catalogue: SKU, category, colour, size, material, unit cost
- Inventory snapshots: SKU, location, snapshot date, available units
- Supplier purchase orders: supplier ID, order date, promised date, receipt date
- Returns: order ID, SKU, return date, reason
- Campaign performance: campaign ID, spend, clicks, attributed orders

## Before analysis
1. Record source name, URL/provider, access date, licence, and date coverage.
2. Keep raw files unchanged and write cleaned outputs separately.
3. Document units, currency, tax treatment, missing-value rules, and table grain.
4. Validate identifiers and totals before joining tables.
5. Use anonymized or aggregated records where possible.

The starter pipeline expects a sales CSV with order_date, sku, and quantity columns. Additional fields are optional.
