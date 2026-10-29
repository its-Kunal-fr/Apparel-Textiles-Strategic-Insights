"""Simple, transparent time-series baselines for monthly retail sales."""
from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd


def evaluate_baselines(monthly: pd.DataFrame, test_months: int = 5) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Evaluate one-step naive and seasonal-naive baselines on a chronological holdout."""
    required = {"Month", "Estimated_Sales"}
    if not required.issubset(monthly.columns):
        raise ValueError(f"Expected columns: {sorted(required)}")
    data = monthly.loc[:, ["Month", "Estimated_Sales"]].copy()
    data["Month"] = pd.PeriodIndex(data["Month"], freq="M")
    data["Estimated_Sales"] = pd.to_numeric(data["Estimated_Sales"], errors="raise")
    data = data.sort_values("Month").drop_duplicates("Month").reset_index(drop=True)
    if test_months < 1 or test_months >= len(data):
        raise ValueError("test_months must be at least 1 and smaller than the number of months")

    split = len(data) - test_months
    results = data.iloc[split:].copy()
    results["Naive_Forecast"] = [float(data.loc[i - 1, "Estimated_Sales"]) for i in range(split, len(data))]
    lookup = dict(zip(data["Month"], data["Estimated_Sales"]))
    results["Seasonal_Naive_Forecast"] = [lookup.get(period - 12, float("nan")) for period in results["Month"]]
    results["Naive_Absolute_Error"] = (results["Estimated_Sales"] - results["Naive_Forecast"]).abs()
    results["Seasonal_Naive_Absolute_Error"] = (results["Estimated_Sales"] - results["Seasonal_Naive_Forecast"]).abs()

    metrics = []
    for method, forecast_col, error_col in [
        ("naive", "Naive_Forecast", "Naive_Absolute_Error"),
        ("seasonal_naive_12_month", "Seasonal_Naive_Forecast", "Seasonal_Naive_Absolute_Error"),
    ]:
        scored = results.dropna(subset=[forecast_col, error_col])
        if scored.empty:
            mae, wape, scored_n = float("nan"), float("nan"), 0
        else:
            mae = scored[error_col].mean()
            denominator = scored["Estimated_Sales"].sum()
            wape = scored[error_col].sum() / denominator * 100 if denominator else float("nan")
            scored_n = len(scored)
        metrics.append({"method": method, "scored_months": scored_n, "MAE": mae, "WAPE_pct": wape})

    results["Month"] = results["Month"].astype(str)
    return results, pd.DataFrame(metrics)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", default="outputs/monthly_kpis.csv")
    parser.add_argument("--output-dir", default="outputs")
    parser.add_argument("--test-months", type=int, default=5)
    args = parser.parse_args()
    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    monthly = pd.read_csv(args.input)
    predictions, metrics = evaluate_baselines(monthly, args.test_months)
    predictions.to_csv(out / "baseline_comparison.csv", index=False)
    metrics.to_csv(out / "baseline_comparison_metrics.csv", index=False)
    print(metrics.to_string(index=False))


if __name__ == "__main__":
    main()
