from pathlib import Path
import pandas as pd

from src.analysis_pipeline import clean_data


def test_clean_data_filters_invalid_rows_and_calculates_sales(tmp_path: Path):
    sample = pd.DataFrame({
        "Order_Date": ["2025-01-02", "2025-01-03", "not-a-date", "2025-01-05"],
        "Units_Sold": [2, 0, 1, 3],
        "Unit_Price": [100, 50, 100, 20],
        "Discount_%": [0.10, 0.0, 0.0, None],
        "Order_ID": ["A", "B", "C", "D"],
        "City": ["Bangalore", "Delhi", "Hyderabad", "Hyd"],
    })
    path = tmp_path / "sample.csv"
    sample.to_csv(path, index=False)

    clean, quality = clean_data(path)

    assert len(clean) == 2
    assert quality["raw_rows"] == 4
    assert quality["analysis_rows"] == 2
    assert round(clean["Estimated_Sales"].sum(), 2) == 240.00
    assert set(clean["City_Normalized"]) == {"Bengaluru", "Hyderabad"}
    assert quality["quantity_nonpositive"] == 1
    assert quality["missing_or_invalid_date"] == 1


def test_invalid_discount_is_excluded(tmp_path: Path):
    sample = pd.DataFrame({
        "Order_Date": ["2025-01-02", "2025-01-03"],
        "Units_Sold": [1, 1],
        "Unit_Price": [100, 100],
        "Discount_%": [1.2, 0.25],
    })
    path = tmp_path / "discounts.csv"
    sample.to_csv(path, index=False)

    clean, quality = clean_data(path)

    assert len(clean) == 1
    assert round(clean.iloc[0]["Estimated_Sales"], 2) == 75.00
    assert quality["invalid_discount"] == 1
