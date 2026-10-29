# Data Dictionary

This dictionary describes fields in `raw/snitch_fashion_sales_uncleaned.csv`. The dataset is synthetic; see [data README](README.md).

| Field | Meaning | Handling in this project |
|---|---|---|
| `Order_ID` | Source order or transaction-line identifier | Used for line counts when present; uniqueness is not assumed without validation |
| `Order_Date` | Order date | Parsed to a date; unparseable dates excluded from primary monthly KPIs |
| `Product_Name` | Product label | Retained as a descriptive dimension |
| `Product_Category` | Product category | Used for category aggregation; missing labels should be reviewed |
| `Units_Sold` | Quantity on the row | Must be numeric and greater than zero |
| `Unit_Price` | Unit price | Must be numeric and greater than zero |
| `Discount_%` | Discount rate represented as a decimal | Values from 0 through 1 accepted; missing values treated as zero only for the illustrative sales calculation |
| `Sales_Amount` | Source-provided sales value | Not trusted as the primary metric because many rows contain zero values |
| `Profit` | Source-provided profit field | Descriptive only; cost and accounting definitions are not independently available |
| `City` | City/location label | Common spelling aliases normalized in the analysis output |
| `Segment` | Customer or market segment label | Used only as a descriptive dimension |

## Derived fields

- `Discount_Used = Discount_%` when valid, otherwise zero when the discount is missing.
- `Estimated_Sales = Units_Sold × Unit_Price × (1 − Discount_Used)`.
- `Month` is the parsed order date expressed as YYYY-MM.
- `City_Normalized` standardizes a small documented set of common aliases.

## Metric definitions

- **Units sold:** sum of valid quantities in the selected group.
- **Estimated sales:** sum of calculated row-level sales; currency is unspecified by the source.
- **MAE:** mean absolute difference between actual and forecast sales.
- **WAPE:** sum of absolute errors divided by sum of actual sales, multiplied by 100.

Do not label estimated sales as audited net revenue. Returns, taxes, shipping, currency, and accounting adjustments are not fully specified in the source.
