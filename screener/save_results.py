"""
Save screener results to the data/results/ directory.
"""

import os

import pandas as pd

from screener.time_utils import now_jakarta


def save_screener_results(df: pd.DataFrame, output_dir: str = "data/results", source: str = "screener") -> None:
    """Save screener results to CSV file with a date-time-based filename.

    File format: ``{output_dir}/YYYYMMDD_HHMMSS_source.csv``
    Contains all processed tickers. Filter by Signal column to get signals only.
    """
    os.makedirs(output_dir, exist_ok=True)
    timestamp = now_jakarta().strftime("%Y%m%d_%H%M%S")

    screener_path = os.path.join(output_dir, f"{timestamp}_{source}.csv")
    df.to_csv(screener_path, index=False)
    
    signal_count = int(df["Signal"].sum()) if "Signal" in df.columns else 0
    print(f"[save_results] Saved {len(df)} rows ({signal_count} signals) to {screener_path}")
