"""Data fetching and loading utilities."""

import pandas as pd
import yfinance as yf

from screener import config


def fetch_stock_data(ticker: str, period: str = config.DATA_PERIOD) -> pd.DataFrame:
    """Fetch OHLCV data from yfinance for a BEI stock (appends .JK suffix)."""
    ticker = str(ticker).strip().upper()
    symbol = ticker if ticker.endswith(".JK") else f"{ticker}.JK"
    df = yf.download(symbol, period=period, auto_adjust=True, progress=False)
    if df.empty:
        return df
    # Flatten MultiIndex columns if present (yfinance >= 0.2 may return them)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    preferred_cols = ["Open", "High", "Low", "Close", "Volume"]
    available_cols = [col for col in preferred_cols if col in df.columns]
    if not available_cols:
        return pd.DataFrame()

    df = df[available_cols].copy()
    df.index = pd.to_datetime(df.index)
    return df


def load_stock_list(filepath: str) -> list:
    """Read a CSV file with a 'ticker' column and return the list of tickers."""
    df = pd.read_csv(filepath)
    return df["ticker"].dropna().str.strip().loc[lambda s: s != ""].tolist()
