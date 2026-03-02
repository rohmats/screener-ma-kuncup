"""
Main entry point for the MA Kuncup screener.

Usage:
    python main.py                 # Scan stocks from stocks.csv, print to terminal
    python main.py --all           # Scan all BEI-listed stocks
    python main.py --all --save    # Scan all BEI stocks and save results to data/results/
    python main.py --save          # Scan stocks.csv and save results
"""

import argparse
import os
import sys

import pandas as pd

from screener.fetch_bei_stocks import fetch_all_bei_tickers
from screener.ma_screener import run_screener
from screener.save_results import save_screener_results

_STOCKS_CSV = os.path.join(os.path.dirname(__file__), "stocks.csv")
_DATA_DIR = os.path.join(os.path.dirname(__file__), "data", "results")


def load_tickers_from_csv(filepath: str) -> list[str]:
    """Load ticker list from stocks.csv."""
    if not os.path.exists(filepath):
        print(f"[main] File not found: {filepath}", file=sys.stderr)
        sys.exit(1)
    df = pd.read_csv(filepath)
    col = next(
        (c for c in df.columns if c.lower() in ("ticker", "code", "symbol", "kode")),
        df.columns[0],
    )
    return df[col].dropna().astype(str).str.strip().tolist()


def main() -> None:
    parser = argparse.ArgumentParser(description="Screener MA Kuncup")
    parser.add_argument(
        "--all",
        action="store_true",
        help="Scan all BEI-listed stocks instead of stocks.csv",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save results to data/results/",
    )
    args = parser.parse_args()

    # Determine ticker source
    if args.all:
        print("[main] Fetching all BEI-listed stocks...")
        tickers = fetch_all_bei_tickers()
        print(f"[main] {len(tickers)} tickers loaded from BEI.")
    else:
        tickers = load_tickers_from_csv(_STOCKS_CSV)
        print(f"[main] {len(tickers)} tickers loaded from {_STOCKS_CSV}.")

    if not tickers:
        print("[main] No tickers to process. Exiting.", file=sys.stderr)
        sys.exit(1)

    # Run screener
    print("[main] Running MA Kuncup screener...")
    df = run_screener(tickers)

    if df.empty:
        print("[main] Screener returned no results.")
        return

    # Display results
    signal_df = df[df["Signal"]]
    print(f"\n[main] Processed {len(df)} stocks. Signals found: {len(signal_df)}")
    if not signal_df.empty:
        print("\n--- MA Kuncup Signals ---")
        print(signal_df[["Ticker", "Price", "MA_Spread_Pct"]].to_string(index=False))
    else:
        print("[main] No MA Kuncup signals today.")

    # Save results if requested
    if args.save:
        save_screener_results(df, output_dir=_DATA_DIR)


if __name__ == "__main__":
    main()
