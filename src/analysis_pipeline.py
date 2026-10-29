"""Reproducible apparel retail data-cleaning, EDA, and baseline forecast pipeline.

Input is a synthetic fashion sales dataset.
Required fields: Order_Date, Units_Sold, Unit_Price, Discount_%.
"""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ALIASES = {
    "bangalore": "Bengaluru", "bengaluru": "Bengaluru",
    "hyd": "Hyderabad", "hyderabad": "Hyderabad",
    "hyderbad": "Hyderabad", "ahm": "Ahmedabad",
}
REQUIRED = {"Order_Date", "Units_Sold", "Unit_Price", "Discount_%"}


def clean_data(path: Path):
    raw = pd.read_csv(path)
    raw.columns = [str(c).strip() for c in raw.columns]
    missing = REQUIRED - set(raw.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")
    df = raw.copy()
    df["Order_Date"] = pd.to_datetime(df["Order_Date"], errors="coerce", dayfirst=True)
    for col in ("Units_Sold", "Unit_Price", "Discount_%", "Profit"):
        if col in df:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "City" in df:
        original_city = df["City"].astype("string").str.strip()
        df["City_Normalized"] = original_city.str.lower().map(ALIASES)
        df["City_Normalized"] = df["City_Normalized"].fillna(original_city.str.title())

    discount = df["Discount_%"]
    df["discount_missing"] = discount.isna()
    df["discount_invalid"] = discount.notna() & ~discount.between(0, 1)
    df["date_missing_or_invalid"] = df["Order_Date"].isna()
    df["quantity_missing"] = df["Units_Sold"].isna()
    df["quantity_nonpositive"] = df["Units_Sold"].notna() & (df["Units_Sold"] <= 0)
    df["price_missing"] = df["Unit_Price"].isna()
    df["price_nonpositive"] = df["Unit_Price"].notna() & (df["Unit_Price"] <= 0)

    valid = (
        df["Order_Date"].notna()
        & df["Units_Sold"].notna() & (df["Units_Sold"] > 0)
        & df["Unit_Price"].notna() & (df["Unit_Price"] > 0)
        & (discount.isna() | discount.between(0, 1))
    )
    clean = df.loc[valid].copy()
    clean["Discount_Used"] = clean["Discount_%"].fillna(0)
    clean["Estimated_Sales"] = clean["Units_Sold"] * clean["Unit_Price"] * (1 - clean["Discount_Used"])
    clean["Month"] = clean["Order_Date"].dt.to_period("M").astype(str)
    quality = {
        "raw_rows": len(df),
        "analysis_rows": len(clean),
        "retained_pct": round(100 * len(clean) / len(df), 2) if len(df) else 0,
        "missing_or_invalid_date": int(df["date_missing_or_invalid"].sum()),
        "missing_quantity": int(df["quantity_missing"].sum()),
        "nonpositive_quantity": int(df["quantity_nonpositive"].sum()),
        "missing_price": int(df["price_missing"].sum()),
        "nonpositive_price": int(df["price_nonpositive"].sum()),
        "invalid_discount": int(df["discount_invalid"].sum()),
        "missing_discount_treated_as_zero": int(df["discount_missing"].sum()),
    }
    return clean, quality


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="data/raw/snitch_fashion_sales_uncleaned.csv")
    parser.add_argument("--output-dir", default="outputs")
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)

    df, quality = clean_data(Path(args.input))
    df.to_csv(out / "cleaned_sales.csv", index=False)
    pd.Series(quality, name="value").to_csv(out / "data_quality_summary.csv")

    monthly = df.groupby("Month", as_index=False).agg(
        Estimated_Sales=("Estimated_Sales", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Order_Lines=("Order_ID", "count") if "Order_ID" in df else ("Month", "size"),
    ).sort_values("Month")
    monthly.to_csv(out / "monthly_kpis.csv", index=False)

    category = df.groupby("Product_Category", as_index=False).agg(
        Estimated_Sales=("Estimated_Sales", "sum"),
        Units_Sold=("Units_Sold", "sum"),
        Valid_Rows=("Estimated_Sales", "size"),
    ).sort_values("Estimated_Sales", ascending=False)
    category.to_csv(out / "category_kpis.csv", index=False)

    city_col = "City_Normalized" if "City_Normalized" in df else "City"
    if city_col in df:
        df.groupby(city_col, as_index=False).agg(
            Estimated_Sales=("Estimated_Sales", "sum"),
            Valid_Rows=("Estimated_Sales", "size"),
        ).sort_values("Estimated_Sales", ascending=False).to_csv(out / "city_kpis.csv", index=False)

    # Chronological holdout: final 20% of months are test data.
    monthly = monthly.sort_values("Month").reset_index(drop=True)
    test_n = max(1, int(round(len(monthly) * 0.20)))
    test_start = len(monthly) - test_n
    forecasts = []
    for i in range(test_start, len(monthly)):
        actual = float(monthly.loc[i, "Estimated_Sales"])
        prediction = float(monthly.loc[i - 1, "Estimated_Sales"])
        forecasts.append({
            "Month": monthly.loc[i, "Month"], "Actual_Sales": actual,
            "Naive_Forecast": prediction, "Absolute_Error": abs(actual - prediction),
        })
    forecast_df = pd.DataFrame(forecasts)
    forecast_df.to_csv(out / "forecast_holdout.csv", index=False)
    mae = forecast_df["Absolute_Error"].mean()
    denom = forecast_df["Actual_Sales"].sum()
    wape = forecast_df["Absolute_Error"].sum() / denom * 100 if denom else float("nan")
    pd.Series({
        "available_months": len(monthly), "train_months": test_start,
        "test_months": len(forecast_df), "naive_baseline_mae": mae,
        "naive_baseline_wape_pct": wape,
        "forecast_method": "last observed month (one-step naive)",
    }, name="value").to_csv(out / "forecast_metrics.csv")

    plt.figure(figsize=(10, 5))
    plt.plot(monthly["Month"], monthly["Estimated_Sales"], marker="o")
    plt.title("Monthly Estimated Sales — Synthetic Fashion Dataset")
    plt.xlabel("Month")
    plt.ylabel("Estimated sales (currency unspecified)")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    plt.savefig(out / "monthly_sales.png", dpi=160)
    plt.close()

    plt.figure(figsize=(9, 5))
    plt.bar(category["Product_Category"], category["Estimated_Sales"])
    plt.title("Estimated Sales by Product Category")
    plt.xlabel("Product category")
    plt.ylabel("Estimated sales (currency unspecified)")
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(out / "category_sales.png", dpi=160)
    plt.close()

    print("Pipeline complete.")
    print(pd.Series(quality).to_string())
    print(f"Baseline holdout MAE: {mae:,.2f}; WAPE: {wape:.2f}%")
    print(f"Outputs saved in {out.resolve()}")


if __name__ == "__main__":
    main()
