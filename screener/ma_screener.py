"""
MA Kuncup (Tight Moving Average) screener logic.

Detects stocks where multiple moving averages are converging / tightly packed,
which often precedes a significant price move.
"""

import numpy as np
import pandas as pd
import yfinance as yf


# Moving average periods used for the screener
MA_PERIODS = [5, 10, 20, 50, 100, 200]

# Threshold: max spread between highest and lowest MA as a % of price
MA_TIGHT_THRESHOLD_PCT = 3.0


def _calc_mas(close: pd.Series) -> pd.DataFrame:
    """Return a DataFrame of simple moving averages for each period in MA_PERIODS."""
    mas = {}
    for p in MA_PERIODS:
        mas[f"ma{p}"] = close.rolling(p).mean()
    return pd.DataFrame(mas, index=close.index)


def screen_ticker(ticker: str, period: str = "1y") -> dict | None:
    """Download OHLCV data for *ticker* and compute MA Kuncup indicators.

    Returns a dict with indicator values, or None if data could not be fetched.
    """
    try:
        df = yf.download(ticker, period=period, progress=False, auto_adjust=True)
        if df.empty or len(df) < max(MA_PERIODS):
            return None

        close = df["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        close = close.dropna()

        mas_df = _calc_mas(close)
        last = mas_df.iloc[-1]

        # Check that all MAs have valid values
        if last.isna().any():
            return None

        latest_price = float(close.iloc[-1])
        if latest_price <= 0:
            return None
        ma_values = last.tolist()
        ma_max = max(ma_values)
        ma_min = min(ma_values)
        spread_pct = (ma_max - ma_min) / latest_price * 100

        ma_tight = spread_pct <= MA_TIGHT_THRESHOLD_PCT

        result = {
            "Ticker": ticker,
            "Price": round(latest_price, 2),
            "MA_Spread_Pct": round(spread_pct, 4),
            "MA_Tight": ma_tight,
            "Signal": ma_tight,
        }
        for col_name, val in zip(
            [f"MA{p}" for p in MA_PERIODS], ma_values
        ):
            result[col_name] = round(float(val), 2)

        return result
    except Exception as exc:  # noqa: BLE001
        print(f"[ma_screener] Error processing {ticker}: {exc}")
        return None


def run_screener(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    """Run the MA Kuncup screener across a list of *tickers*.

    Returns a DataFrame with one row per ticker (excluding those that failed).
    """
    results = []
    total = len(tickers)
    for idx, ticker in enumerate(tickers, start=1):
        if idx % 50 == 0 or idx == total:
            print(f"[ma_screener] Processing {idx}/{total}: {ticker}")
        row = screen_ticker(ticker, period=period)
        if row:
            results.append(row)

    if not results:
        return pd.DataFrame()

    cols = (
        ["Ticker", "Price", "MA_Spread_Pct", "MA_Tight", "Signal"]
        + [f"MA{p}" for p in MA_PERIODS]
    )
    df = pd.DataFrame(results, columns=cols)
    df.sort_values("MA_Spread_Pct", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
