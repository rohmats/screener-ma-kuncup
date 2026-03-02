"""Entry point for the MA Kuncup screener."""

import os
import sys
import argparse
import pandas as pd

from screener.data import load_stock_list
from screener.screener import run_screener
from screener.time_utils import now_jakarta

STOCKS_FILE = os.path.join(os.path.dirname(__file__), "stocks.csv")
BEI_STOCKS_FILE = os.path.join(os.path.dirname(__file__), "data", "bei_stocks.csv")
YAHOO_STOCKS_FILE = os.path.join(os.path.dirname(__file__), "data", "all_stocks.csv")

OUTPUT_COLS = [
    "Ticker", "Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100",
    "Range_Ticks", "Vol_Pct", "Volume", "MA_Tight", "Signal",
]

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)
pd.set_option("display.float_format", "{:.2f}".format)


def main():
    parser = argparse.ArgumentParser(description="MA Kuncup Screener")
    parser.add_argument(
        "--source",
        choices=["bei", "yahoo"],
        default="bei",
        help="Data source: 'bei' (default) or 'yahoo'",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save results to CSV file",
    )
    args = parser.parse_args()

    # Determine which file to use
    if args.source == "yahoo":
        stock_file = YAHOO_STOCKS_FILE
        source_name = "Yahoo Stocks"
    else:
        stock_file = BEI_STOCKS_FILE if os.path.exists(BEI_STOCKS_FILE) else STOCKS_FILE
        source_name = "BEI Stocks"

    print(f"Loading {source_name} from: {stock_file}")
    if not os.path.exists(stock_file):
        print(f"Error: Stock file not found at {stock_file}")
        sys.exit(1)

    symbols = load_stock_list(stock_file)
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

    # Save results if requested
    if args.save:
        timestamp = now_jakarta().strftime("%d-%m-%Y_%H%M%S")
        output_file = os.path.join(
            os.path.dirname(__file__),
            "data",
            "results",
            f"screener_{args.source}_{timestamp}.csv"
        )
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        results.to_csv(output_file, index=False)
        print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
