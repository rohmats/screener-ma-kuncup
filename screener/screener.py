"""Core screener logic for MA Kuncup / MA Ketat pattern detection."""

from concurrent.futures import ThreadPoolExecutor

import pandas as pd

from screener.config import (
    RANGE_TICKS_THRESHOLD,
    VOL_PCT_THRESHOLD,
    MIN_VOLUME,
)
from screener.data import fetch_stock_data
from screener.indicators import calculate_all_indicators


OUTPUT_COLS = [
    "Ticker", "Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100",
    "Range_Ticks", "Vol_Pct", "Volume", "MA_Tight", "Signal",
]


def is_ma_tight(range_ticks: float, vol_pct: float) -> bool:
    """Return True if the MA kuncup (tight) condition is satisfied."""
    return range_ticks < RANGE_TICKS_THRESHOLD and vol_pct < VOL_PCT_THRESHOLD


def is_signal(row: pd.Series) -> bool:
    """Return True if the final entry signal is triggered for a given row."""
    if pd.isna(row.get("MA_Tight")) or pd.isna(row.get("Volume")) or pd.isna(row.get("MA100")):
        return False
    return (
        bool(row["MA_Tight"])
        and row["Volume"] > MIN_VOLUME
        and row["MA100"] <= row["Close"]
    )


def _screen_single_stock_with_params(
    ticker: str,
    range_ticks_threshold: float,
    vol_pct_threshold: float,
    min_volume: int,
    min_rows: int,
) -> pd.Series | None:
    """Fetch/process one stock with caller-supplied thresholds."""
    df = fetch_stock_data(ticker)
    if df is None or df.empty or len(df) < min_rows:
        return None

    df = calculate_all_indicators(df)
    df["MA_Tight"] = (
        (df["Range_Ticks"] < range_ticks_threshold)
        & (df["Vol_Pct"] < vol_pct_threshold)
    )

    latest = df.iloc[-1].copy()
    latest["Signal"] = bool(
        pd.notna(latest.get("MA_Tight"))
        and pd.notna(latest.get("Volume"))
        and pd.notna(latest.get("MA100"))
        and bool(latest["MA_Tight"])
        and latest["Volume"] > min_volume
        and latest["MA100"] <= latest["Close"]
    )
    latest["Ticker"] = ticker
    return latest


def screen_single_stock(ticker: str) -> pd.Series | None:
    """Fetch and process a single stock with default config thresholds."""
    return _screen_single_stock_with_params(
        ticker=ticker,
        range_ticks_threshold=RANGE_TICKS_THRESHOLD,
        vol_pct_threshold=VOL_PCT_THRESHOLD,
        min_volume=MIN_VOLUME,
        min_rows=100,
    )


def run_screener(
    symbols: list,
    range_ticks_threshold: float = RANGE_TICKS_THRESHOLD,
    vol_pct_threshold: float = VOL_PCT_THRESHOLD,
    min_volume: int = MIN_VOLUME,
    min_rows: int = 100,
    max_workers: int = 4,
) -> pd.DataFrame:
    """Run the screener over all symbols and return a summary DataFrame."""
    if not symbols:
        return pd.DataFrame()

    def _worker(ticker: str) -> pd.Series | None:
        try:
            return _screen_single_stock_with_params(
                ticker=ticker,
                range_ticks_threshold=range_ticks_threshold,
                vol_pct_threshold=vol_pct_threshold,
                min_volume=min_volume,
                min_rows=min_rows,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"[run_screener] Skip {ticker}: {exc}")
            return None

    worker_count = max(1, min(int(max_workers), len(symbols)))
    if worker_count == 1:
        results = (_worker(ticker) for ticker in symbols)
    else:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            results = executor.map(_worker, symbols)

    records = [result for result in results if result is not None]

    if not records:
        return pd.DataFrame()

    df_out = pd.DataFrame(records)
    df_out = df_out[[c for c in OUTPUT_COLS if c in df_out.columns]].reset_index(drop=True)
    return df_out
