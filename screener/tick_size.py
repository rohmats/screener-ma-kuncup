"""Tick size rules based on official IDX (BEI) regulations."""

import pandas as pd


def tick_size(close: float) -> int:
    """Return the tick size for a given closing price per IDX rules."""
    if close <= 200:
        return 1
    elif close <= 500:
        return 2
    elif close <= 2000:
        return 5
    elif close <= 5000:
        return 10
    else:
        return 25


def tick_size_series(series: pd.Series) -> pd.Series:
    """Vectorized tick size calculation for a pandas Series."""
    result = pd.Series(25, index=series.index, dtype=int)
    result = result.where(series > 5000, 10)
    result = result.where(series > 2000, 5)
    result = result.where(series > 500, 2)
    result = result.where(series > 200, 1)
    return result
