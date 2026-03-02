"""
Save screener results to the data/results/ directory.
"""

import os
from datetime import datetime

import pandas as pd


def save_screener_results(df: pd.DataFrame, output_dir: str = "data/results") -> None:
    """Save screener results to CSV files with a date-based filename.

    Two files are written:
    - ``{output_dir}/DD-MM-YYYY_screener.csv`` — all processed tickers.
    - ``{output_dir}/DD-MM-YYYY_signals.csv``  — only tickers where Signal is True.
    """
    os.makedirs(output_dir, exist_ok=True)
    today = datetime.now().strftime("%d-%m-%Y")

    screener_path = os.path.join(output_dir, f"{today}_screener.csv")
    df.to_csv(screener_path, index=False)
    print(f"[save_results] Saved {len(df)} rows to {screener_path}")

    signals = df[df["Signal"]]
    if not signals.empty:
        signals_path = os.path.join(output_dir, f"{today}_signals.csv")
        signals.to_csv(signals_path, index=False)
        print(f"[save_results] Saved {len(signals)} signals to {signals_path}")
    else:
        print("[save_results] No signals found today.")
