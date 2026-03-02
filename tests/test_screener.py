"""Tests for screener logic: is_ma_tight and is_signal."""

import math
import pandas as pd
import pytest

from screener.screener import is_ma_tight, is_signal
from screener import config


class TestIsMaTight:
    def test_tight_when_range_and_vol_below_threshold(self):
        assert is_ma_tight(range_ticks=3.0, vol_pct=2.0) is True

    def test_not_tight_when_range_too_high(self):
        assert is_ma_tight(range_ticks=config.RANGE_TICKS_THRESHOLD, vol_pct=1.0) is False

    def test_not_tight_when_vol_too_high(self):
        assert is_ma_tight(range_ticks=2.0, vol_pct=config.VOL_PCT_THRESHOLD) is False

    def test_not_tight_when_both_exceed_threshold(self):
        assert is_ma_tight(range_ticks=10.0, vol_pct=5.0) is False

    def test_tight_at_just_below_thresholds(self):
        assert is_ma_tight(
            range_ticks=config.RANGE_TICKS_THRESHOLD - 0.001,
            vol_pct=config.VOL_PCT_THRESHOLD - 0.001,
        ) is True


class TestIsSignal:
    def _make_row(self, ma_tight, volume, ma100, close):
        return pd.Series({
            "MA_Tight": ma_tight,
            "Volume": volume,
            "MA100": ma100,
            "Close": close,
        })

    def test_signal_true_when_all_conditions_met(self):
        row = self._make_row(ma_tight=True, volume=2_000_000, ma100=900.0, close=1000.0)
        assert is_signal(row) is True

    def test_signal_false_when_not_ma_tight(self):
        row = self._make_row(ma_tight=False, volume=2_000_000, ma100=900.0, close=1000.0)
        assert is_signal(row) is False

    def test_signal_false_when_volume_too_low(self):
        row = self._make_row(ma_tight=True, volume=500_000, ma100=900.0, close=1000.0)
        assert is_signal(row) is False

    def test_signal_false_when_ma100_above_close(self):
        row = self._make_row(ma_tight=True, volume=2_000_000, ma100=1100.0, close=1000.0)
        assert is_signal(row) is False

    def test_signal_true_when_ma100_equals_close(self):
        row = self._make_row(ma_tight=True, volume=2_000_000, ma100=1000.0, close=1000.0)
        assert is_signal(row) is True

    def test_signal_false_when_ma100_is_nan(self):
        row = self._make_row(ma_tight=True, volume=2_000_000, ma100=float("nan"), close=1000.0)
        assert is_signal(row) is False

    def test_signal_false_when_volume_exactly_min(self):
        # Volume must be strictly greater than MIN_VOLUME
        row = self._make_row(ma_tight=True, volume=config.MIN_VOLUME, ma100=900.0, close=1000.0)
        assert is_signal(row) is False
