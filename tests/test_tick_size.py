"""Tests for tick_size module."""

import pytest
from screener.tick_size import tick_size, tick_size_series
import pandas as pd


class TestTickSize:
    def test_price_at_200_returns_1(self):
        assert tick_size(200) == 1

    def test_price_below_200_returns_1(self):
        assert tick_size(50) == 1
        assert tick_size(1) == 1
        assert tick_size(199) == 1

    def test_price_at_500_returns_2(self):
        assert tick_size(500) == 2

    def test_price_between_200_and_500_returns_2(self):
        assert tick_size(201) == 2
        assert tick_size(300) == 2
        assert tick_size(499) == 2

    def test_price_at_2000_returns_5(self):
        assert tick_size(2000) == 5

    def test_price_between_500_and_2000_returns_5(self):
        assert tick_size(501) == 5
        assert tick_size(1000) == 5
        assert tick_size(1999) == 5

    def test_price_at_5000_returns_10(self):
        assert tick_size(5000) == 10

    def test_price_between_2000_and_5000_returns_10(self):
        assert tick_size(2001) == 10
        assert tick_size(3000) == 10
        assert tick_size(4999) == 10

    def test_price_above_5000_returns_25(self):
        assert tick_size(5001) == 25
        assert tick_size(10000) == 25
        assert tick_size(50000) == 25


class TestTickSizeSeries:
    def test_series_returns_correct_ticks(self):
        prices = pd.Series([100, 200, 300, 500, 1000, 2000, 3000, 5000, 6000])
        expected = pd.Series([1, 1, 2, 2, 5, 5, 10, 10, 25])
        result = tick_size_series(prices)
        pd.testing.assert_series_equal(result.reset_index(drop=True), expected.reset_index(drop=True))

    def test_series_edge_case_at_boundary(self):
        prices = pd.Series([200, 500, 2000, 5000])
        expected = pd.Series([1, 2, 5, 10])
        result = tick_size_series(prices)
        pd.testing.assert_series_equal(result.reset_index(drop=True), expected.reset_index(drop=True))
