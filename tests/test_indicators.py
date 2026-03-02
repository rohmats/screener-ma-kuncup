"""Tests for indicators module."""

import numpy as np
import pandas as pd
import pytest

from screener.indicators import (
    calculate_moving_averages,
    calculate_range_ticks,
    calculate_volatility,
    calculate_all_indicators,
)


def make_df(prices, volumes=None):
    """Helper to create a minimal OHLCV-like DataFrame with Close and Volume."""
    if volumes is None:
        volumes = [1_000_000] * len(prices)
    return pd.DataFrame({"Close": prices, "Volume": volumes})


class TestCalculateMovingAverages:
    def test_ma3_correct(self):
        prices = [10.0, 20.0, 30.0, 40.0, 50.0]
        df = make_df(prices)
        df = calculate_moving_averages(df, [3])
        assert round(df["MA3"].iloc[-1], 4) == round((30 + 40 + 50) / 3, 4)

    def test_ma_nan_for_insufficient_data(self):
        prices = [10.0, 20.0]
        df = make_df(prices)
        df = calculate_moving_averages(df, [3])
        assert np.isnan(df["MA3"].iloc[-1])

    def test_multiple_periods(self):
        prices = list(range(1, 51))
        df = make_df(prices)
        df = calculate_moving_averages(df, [3, 5, 10])
        assert "MA3" in df.columns
        assert "MA5" in df.columns
        assert "MA10" in df.columns


class TestCalculateRangeTicks:
    def test_range_ticks_zero_when_all_ma_equal(self):
        # All prices the same => all MAs equal => range is 0
        prices = [1000.0] * 60
        df = make_df(prices)
        from screener import config
        df = calculate_moving_averages(df, config.MA_PERIODS)
        df = calculate_range_ticks(df)
        assert df["Range_Ticks"].iloc[-1] == pytest.approx(0.0)

    def test_range_ticks_positive(self):
        # Increasing prices create spread between short and long MAs
        prices = list(range(100, 160))
        df = make_df(prices)
        from screener import config
        df = calculate_moving_averages(df, config.MA_PERIODS)
        df = calculate_range_ticks(df)
        assert df["Range_Ticks"].iloc[-1] > 0


class TestCalculateVolatility:
    def test_vol_pct_zero_for_constant_prices(self):
        prices = [1000.0] * 30
        df = make_df(prices)
        df = calculate_volatility(df)
        # std dev of constant returns (all zero) should be 0
        assert df["Vol_Pct"].iloc[-1] == pytest.approx(0.0)

    def test_vol_pct_nan_for_insufficient_data(self):
        prices = [100.0, 200.0]
        df = make_df(prices)
        df = calculate_volatility(df, period=10)
        assert np.isnan(df["Vol_Pct"].iloc[-1])

    def test_vol_pct_positive_for_varying_prices(self):
        np.random.seed(42)
        prices = 1000 + np.cumsum(np.random.randn(50) * 10)
        df = make_df(prices.tolist())
        df = calculate_volatility(df)
        assert df["Vol_Pct"].iloc[-1] > 0


class TestCalculateAllIndicators:
    def test_all_columns_present(self):
        prices = [1000.0] * 110
        df = make_df(prices)
        df = calculate_all_indicators(df)
        for col in ["MA3", "MA5", "MA10", "MA20", "MA50", "MA100", "Range_Ticks", "Vol_Pct"]:
            assert col in df.columns
