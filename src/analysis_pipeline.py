"""Starter pipeline for apparel retail sales data.
Required CSV columns: order_date, sku, quantity.
Optional columns: category, unit_price, discount.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

REQUIRED_COLUMNS = {"order_date", "sku", "quantity"}


def clean_sales(input_path: Path):
    df = pd.read_csv(input_path)
    initial_rows = len(df)
    df.columns = [str(c).strip().lower() for c in df.columns]
    missing_columns = REQUIRED_COLUMNS - set(df.columns)
    if missing_columns:
        raise ValueError("Missing required columns: " + ", ".join(sorted(missing_columns)))

    df["sku"] = df["sku"].astype("string").str.strip()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
    for col in ("unit_price", "discount"):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    exact_duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates().copy()
    invalid = (
        df["order_date"].isna()
        | df["sku"].isna()
        | df["sku"].eq("")
        | df["quantity"].isna()
        | (df["quantity"] < 0)
    )
    invalid_rows = int(invalid.sum())
    df = df.loc[~invalid].copy()

    if "unit_price" in df.columns:
        df.loc[df["unit_price"] < 0, "unit_price"] = pd.NA
        df["gross_sales"] = df["quantity"] * df["unit_price"]
        if "discount" in df.columns:
            # Assumes discount is a fraction between 0 and 1.
            # Review source conventions before using this field.
            df["discount_out_of_range"] = df["discount"].notna() & ~df["discount"].between(0, 1)
            discount = df["discount"].fillna(0).where(df["discount"].between(0, 1), 0)
        else:
            discount = 0
        df["estimated_net_sales"] = df["gross_sales"] * (1 - discount)

    df["order_month"] = df["order_date"].dt.to_period("M").astype(str)
    quality = {
        "input_rows": initial_rows,
        "exact_duplicate_rows_removed": exact_duplicates,
        "invalid_rows_excluded": invalid_rows,
        "output_rows": len(df),
        "date_min": str(df["order_date"].min()) if not df.empty else None,
        "date_max": str(df["order_date"].max()) if not df.empty else None,
    }
    return df, quality


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to sales CSV")
    parser.add_argument("--output-dir", default="outputs", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    df, quality = clean_sales(Path(args.input))
    df.to_csv(output_dir / "cleaned_sales.csv", index=False)

    monthly = df.groupby("order_month", as_index=False).agg(
        units_sold=("quantity", "sum"),
        order_lines=("sku", "size"),
    )
    if "estimated_net_sales" in df.columns:
        sales = df.groupby("order_month", as_index=False).agg(
            estimated_net_sales=("estimated_net_sales", "sum")
        )
        monthly = monthly.merge(sales, on="order_month", how="left")
    monthly.to_csv(output_dir / "monthly_summary.csv", index=False)
    pd.Series(quality, name="value").to_csv(output_dir / "data_quality_summary.csv")
    print("Pipeline completed. Cleaned rows:", len(df))
    print("Outputs written to:", output_dir.resolve())
    print("Review source definitions and discount conventions before interpreting sales.")


if __name__ == "__main__":
    main()
