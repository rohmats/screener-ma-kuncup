"""Halaman detail saham — chart harga, MA, volume, dan indikator."""

from datetime import datetime
from pathlib import Path
import re

import pandas as pd
import streamlit as st

from screener.data import fetch_stock_data
from screener.indicators import calculate_all_indicators
from screener.screener import is_signal
from ui.components import render_price_chart


RESULTS_DIR = Path(__file__).parent.parent.parent / "data" / "results"

# Default parameters (fallback)
DEFAULT_RANGE_TICKS_THRESHOLD = 6
DEFAULT_VOL_PCT_THRESHOLD = 3.8


def _to_bool_value(value) -> bool:
    """Normalize mixed boolean-like values from CSV/session state."""
    if pd.isna(value):
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes", "y", "on", "aktif"}
    return bool(value)


def _to_bool_series(series: pd.Series) -> pd.Series:
    """Normalize a series containing bool/int/string flags into strict booleans."""
    return series.apply(_to_bool_value).astype(bool)


def _fetch_and_compute(ticker: str, range_ticks_threshold: float = None, vol_pct_threshold: float = None) -> pd.DataFrame:
    """Fetch stock data and compute all indicators with configurable thresholds."""
    # Use session state parameters if available, otherwise fallback to defaults
    if range_ticks_threshold is None:
        range_ticks_threshold = st.session_state.get("range_ticks_threshold", DEFAULT_RANGE_TICKS_THRESHOLD)
    if vol_pct_threshold is None:
        vol_pct_threshold = st.session_state.get("vol_pct_threshold", DEFAULT_VOL_PCT_THRESHOLD)
    
    df = fetch_stock_data(ticker)
    if df is None or df.empty:
        return pd.DataFrame()
    if len(df) < 10:
        return df
    df = calculate_all_indicators(df)
    df["MA_Tight"] = (
        (df["Range_Ticks"] < range_ticks_threshold) & (df["Vol_Pct"] < vol_pct_threshold)
    )
    return df


@st.cache_data(ttl=120)
def _load_latest_history_results() -> pd.DataFrame:
    """Load latest historical screener result file from data/results/ as fallback source."""
    if not RESULTS_DIR.exists():
        return pd.DataFrame()

    result_files = list(RESULTS_DIR.glob("*.csv"))
    if not result_files:
        return pd.DataFrame()

    def _extract_timestamp(filepath: Path) -> datetime:
        stem = filepath.stem
        # Match YYYYMMDD_HHMMSS at the start
        match_new = re.match(r"^(\d{8})_(\d{6})", stem)
        # Legacy format: DD-MM-YYYY_HHMMSS
        match_legacy = re.search(r"(\d{2}-\d{2}-\d{4})_(\d{6})", stem)

        try:
            if match_new:
                return datetime.strptime(
                    f"{match_new.group(1)}_{match_new.group(2)}",
                    "%Y%m%d_%H%M%S",
                )
            if match_legacy:
                return datetime.strptime(
                    f"{match_legacy.group(1)}_{match_legacy.group(2)}",
                    "%d-%m-%Y_%H%M%S",
                )
        except ValueError:
            pass

        return datetime.fromtimestamp(filepath.stat().st_mtime)

    result_files = sorted(result_files, key=_extract_timestamp, reverse=True)

    try:
        return pd.read_csv(result_files[0])
    except Exception:
        return pd.DataFrame()


def render_stock_detail() -> None:
    """Render the stock detail page."""
    st.title("📈 Detail Saham")
    st.markdown("Tampilkan chart harga, Moving Average, dan indikator untuk saham pilihan.")
    st.divider()

    # Ticker source: prefer current session results; fallback to latest history file.
    session_results = st.session_state.get("results", pd.DataFrame())
    history_results = _load_latest_history_results() if session_results.empty else pd.DataFrame()
    results = session_results if not session_results.empty else history_results
    
    # Show info if using historical results
    if session_results.empty and not history_results.empty:
        st.info("ℹ️ Screener belum dijalankan pada sesi ini. Daftar ticker diambil dari riwayat terbaru.")
    
    # Status filters - always available
    st.subheader("🔍 Filter Status")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_ma = st.multiselect(
            "🔗 Filter Status MA",
            options=["MA Tight", "Tidak MA Tight"],
            default=["MA Tight", "Tidak MA Tight"],
            help="Filter berdasarkan kondisi MA Kuncup/MA Ketat",
            key="stock_detail_filter_ma",
        )
    with col_f2:
        filter_signal = st.multiselect(
            "🚀 Filter Status Entry",
            options=["Sinyal Aktif", "Belum Sinyal"],
            default=["Sinyal Aktif", "Belum Sinyal"],
            help="Filter berdasarkan sinyal entry yang valid",
            key="stock_detail_filter_signal",
        )

    st.divider()
    
    if not results.empty and "Ticker" in results.columns:
        # Prepare results with proper boolean columns
        filtered_results = results.copy()
        
        # Ensure MA_Tight column exists and is boolean
        if "MA_Tight" in filtered_results.columns:
            filtered_results["MA_Tight"] = _to_bool_series(filtered_results["MA_Tight"])
        else:
            filtered_results["MA_Tight"] = False
            
        # Ensure Signal column exists and is boolean
        if "Signal" in filtered_results.columns:
            filtered_results["Signal"] = _to_bool_series(filtered_results["Signal"])
        else:
            filtered_results["Signal"] = False
        
        # Apply MA filter
        if filter_ma:
            ma_mask = pd.Series([False] * len(filtered_results), index=filtered_results.index)
            if "MA Tight" in filter_ma:
                ma_mask = ma_mask | filtered_results["MA_Tight"].eq(True)
            if "Tidak MA Tight" in filter_ma:
                ma_mask = ma_mask | filtered_results["MA_Tight"].eq(False)
            filtered_results = filtered_results[ma_mask]
        
        # Apply Signal filter
        if filter_signal:
            signal_mask = pd.Series([False] * len(filtered_results), index=filtered_results.index)
            if "Sinyal Aktif" in filter_signal:
                signal_mask = signal_mask | filtered_results["Signal"].eq(True)
            if "Belum Sinyal" in filter_signal:
                signal_mask = signal_mask | filtered_results["Signal"].eq(False)
            filtered_results = filtered_results[signal_mask]

        ticker_list = sorted(filtered_results["Ticker"].dropna().unique().tolist())
        
        if not ticker_list:
            st.warning("Tidak ada saham yang sesuai dengan filter yang dipilih.")
            return

        # Get previously selected ticker from session state, reset if not in filtered list
        previously_selected = st.session_state.get("stock_detail_selected_ticker", None)
        if previously_selected in ticker_list:
            default_index = ticker_list.index(previously_selected)
        else:
            default_index = 0

        ticker = st.selectbox(
            "Pilih Ticker",
            options=ticker_list,
            index=default_index,
            help=f"Daftar saham dari hasil screener/riwayat (tersaring: {len(ticker_list)} saham)",
            key="stock_detail_ticker_select",
        )
        
        # Store selected ticker in session state
        st.session_state["stock_detail_selected_ticker"] = ticker

        if session_results.empty and not history_results.empty:
            st.caption("ℹ️ Screener belum dijalankan pada sesi ini, daftar ticker diambil dari riwayat terbaru.")
    else:
        ticker = st.text_input(
            "Masukkan Ticker Saham (contoh: BBCA)",
            value="BBCA",
            help="Masukkan kode saham BEI tanpa suffix .JK",
        ).upper().strip()

    if not ticker:
        st.warning("Masukkan kode saham terlebih dahulu.")
        return

    # Get parameters from session state (from dashboard or use defaults)
    range_ticks_threshold = st.session_state.get("range_ticks_threshold", DEFAULT_RANGE_TICKS_THRESHOLD)
    vol_pct_threshold = st.session_state.get("vol_pct_threshold", DEFAULT_VOL_PCT_THRESHOLD)
    
    with st.spinner(f"Mengambil data {ticker}..."):
        df = _fetch_and_compute(ticker, range_ticks_threshold, vol_pct_threshold)

    if df.empty:
        st.error(
            f"Data untuk **{ticker}** tidak tersedia. "
            "Pastikan kode saham benar dan terdaftar di BEI."
        )
        return

    # Show parameters being used
    with st.expander("⚙️ Parameter yang Digunakan", expanded=False):
        param_col1, param_col2, param_col3 = st.columns(3)
        with param_col1:
            st.metric("Range Ticks", f"< {range_ticks_threshold}")
        with param_col2:
            st.metric("Vol Pct", f"< {vol_pct_threshold}%")
        with param_col3:
            min_volume = st.session_state.get("min_volume", 1_000_000)
            st.metric("Min Volume", f"{min_volume:,.0f}")
        st.caption("Parameter ini digunakan untuk menghitung MA Tight dan Signal. Jika data tidak sesuai, kemungkinan parameter berbeda dari hasil riwayat.")

    st.divider()
    
    # Status badges - use values from screener results if available, otherwise compute from raw data
    latest = df.iloc[-1]
    
    # Try to get status from loaded screener/history results first (for consistency)
    if not results.empty and "Ticker" in results.columns and ticker in results["Ticker"].values:
        source_row = results[results["Ticker"] == ticker].iloc[-1]
        ma_tight_val = _to_bool_value(source_row.get("MA_Tight", False))
        signal_val = _to_bool_value(source_row.get("Signal", False))
        data_source = "dari hasil screener sesi ini" if not session_results.empty else "dari hasil riwayat"
    else:
        # Compute from raw data if not in screener results
        ma_tight_val = _to_bool_value(latest.get("MA_Tight", False))
        min_volume = st.session_state.get("min_volume", 1_000_000)
        signal_val = False
        if "Range_Ticks" in latest and "Vol_Pct" in latest and "Volume" in latest and "MA100" in latest:
            signal_val = (
                bool(ma_tight_val)
                and latest["Volume"] > min_volume
                and latest["MA100"] <= latest["Close"]
            )
        data_source = "dihitung ulang dari data terbaru"

    col1, col2, col3 = st.columns(3)
    with col1:
        close_val = latest.get("Close", 0)
        st.metric("Harga Terakhir", f"Rp {close_val:,.0f}" if pd.notna(close_val) else "-")
    with col2:
        tight_text = "✅ MA Tight" if ma_tight_val else "❌ Tidak MA Tight"
        st.metric("Status MA", tight_text)
    with col3:
        signal_text = "✅ Sinyal Aktif" if signal_val else "❌ Belum Sinyal"
        st.metric("Sinyal Entry", signal_text)

    st.caption(f"ℹ️ Status {data_source}")

    st.divider()

    # Price + MA + Volume chart
    st.subheader(f"📊 Chart Harga & Moving Average — {ticker}")
    render_price_chart(df, ticker)

    st.divider()

    # Indicator table (last 20 days)
    st.subheader("📋 Tabel Indikator (20 Hari Terakhir)")
    indicator_cols = [
        "Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100",
        "Range_Ticks", "Vol_Pct", "Volume", "MA_Tight",
    ]
    available_cols = [c for c in indicator_cols if c in df.columns]
    recent_df = df[available_cols].tail(20).copy().sort_index(ascending=False)
    recent_df.index = recent_df.index.strftime("%d-%m-%Y")

    # Format boolean columns
    if "MA_Tight" in recent_df.columns:
        recent_df["MA_Tight"] = recent_df["MA_Tight"].map(lambda v: "✅" if bool(v) else "❌")

    # Apply formatting
    styled = recent_df.style.format(
        {
            "Close": "{:,.2f}",
            "MA3": "{:,.2f}",
            "MA5": "{:,.2f}",
            "MA10": "{:,.2f}",
            "MA20": "{:,.2f}",
            "MA50": "{:,.2f}",
            "MA100": "{:,.2f}",
            "Range_Ticks": "{:,.2f}",
            "Vol_Pct": "{:,.2f}%",
            "Volume": "{:,.0f}",
        },
        na_rep="-",
    )

    st.dataframe(styled, width="stretch")

    # Footer
    st.divider()
    st.caption(
        "⚠️ **Disclaimer**: Informasi ini hanya untuk tujuan edukasi. "
        "Bukan merupakan rekomendasi investasi."
    )
