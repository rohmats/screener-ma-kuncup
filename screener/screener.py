"""Core screener logic for MA Kuncup / MA Ketat pattern detection."""

import pandas as pd

from screener import config
from screener.data import fetch_stock_data
from screener.indicators import calculate_all_indicators


def is_ma_tight(range_ticks: float, vol_pct: float) -> bool:
    """Return True if the MA kuncup (tight) condition is satisfied."""
    return range_ticks < config.RANGE_TICKS_THRESHOLD and vol_pct < config.VOL_PCT_THRESHOLD


def is_signal(row: pd.Series) -> bool:
    """Return True if the final entry signal is triggered for a given row."""
    if pd.isna(row.get("MA_Tight")) or pd.isna(row.get("Volume")) or pd.isna(row.get("MA100")):
        return False
    return (
        bool(row["MA_Tight"])
        and row["Volume"] > config.MIN_VOLUME
        and row["MA100"] <= row["Close"]
    )


def screen_single_stock(ticker: str) -> pd.Series | None:
    """Fetch and process a single stock; return the latest-row Series or None."""
    df = fetch_stock_data(ticker)
    if df is None or df.empty or len(df) < 100:
        return None

    df = calculate_all_indicators(df)
    df["MA_Tight"] = (
        (df["Range_Ticks"] < config.RANGE_TICKS_THRESHOLD)
        & (df["Vol_Pct"] < config.VOL_PCT_THRESHOLD)
    )

    latest = df.iloc[-1].copy()
    latest["Signal"] = is_signal(latest)
    latest["Ticker"] = ticker
    return latest


def run_screener(symbols: list) -> pd.DataFrame:
    """Run the screener over all symbols and return a summary DataFrame."""
    records = []
    for ticker in symbols:
        result = screen_single_stock(ticker)
        if result is not None:
            records.append(result)

    if not records:
        return pd.DataFrame()

    output_cols = [
        "Ticker", "Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100",
        "Range_Ticks", "Vol_Pct", "Volume", "MA_Tight", "Signal",
    ]
    df_out = pd.DataFrame(records)
    df_out = df_out[[c for c in output_cols if c in df_out.columns]].reset_index(drop=True)
    return df_out
