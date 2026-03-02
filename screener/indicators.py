"""Technical indicators for the MA Kuncup screener."""

import pandas as pd
import numpy as np

from screener.tick_size import tick_size_series
from screener import config


def calculate_moving_averages(df: pd.DataFrame, periods: list) -> pd.DataFrame:
    """Calculate Simple Moving Averages for given periods and add to DataFrame."""
    for period in periods:
        df[f"MA{period}"] = df["Close"].rolling(window=period).mean()
    return df


def calculate_range_ticks(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate MA_max, MA_min and range_ticks using BEI tick size rules."""
    ma_columns = [f"MA{p}" for p in config.MA_PERIODS]
    price_columns = ["Close"] + ma_columns

    df["MA_max"] = df[price_columns].max(axis=1)
    df["MA_min"] = df[price_columns].min(axis=1)

    tick = tick_size_series(df["Close"])
    df["Range_Ticks"] = (df["MA_max"] - df["MA_min"]) / tick

    return df


def calculate_volatility(df: pd.DataFrame, period: int = config.VOL_ROLLING_PERIOD) -> pd.DataFrame:
    """Calculate rolling volatility as std dev of daily returns (in percent)."""
    daily_returns = df["Close"].pct_change()
    df["Vol_Pct"] = daily_returns.rolling(window=period).std() * 100
    return df


def calculate_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Run all indicator calculations and return the updated DataFrame."""
    df = calculate_moving_averages(df, config.MA_PERIODS + [config.MA_TREND_PERIOD])
    df = calculate_range_ticks(df)
    df = calculate_volatility(df)
    return df
