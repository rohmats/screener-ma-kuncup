"""Entry point for the MA Kuncup screener."""

import os
import pandas as pd

from screener.data import load_stock_list
from screener.screener import run_screener

STOCKS_FILE = os.path.join(os.path.dirname(__file__), "stocks.csv")

OUTPUT_COLS = [
    "Ticker", "Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100",
    "Range_Ticks", "Vol_Pct", "Volume", "MA_Tight", "Signal",
]

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.float_format", "{:.2f}".format)


def main():
    print("Loading stock list...")
    symbols = load_stock_list(STOCKS_FILE)
    print(f"Screening {len(symbols)} stocks...\n")

    results = run_screener(symbols)

    if results.empty:
        print("No results found.")
        return

    print("=== Screener Results ===")
    print(results.to_string(index=False))

    signals = results[results["Signal"]]
    print(f"\n=== {len(signals)} stock(s) with MA Kuncup signal ===")
    if not signals.empty:
        print(signals.to_string(index=False))


if __name__ == "__main__":
    main()
