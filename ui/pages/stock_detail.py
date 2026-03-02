"""Halaman detail saham — chart harga, MA, volume, dan indikator."""

import pandas as pd
import streamlit as st

from screener.data import fetch_stock_data
from screener.indicators import calculate_all_indicators
from screener.screener import is_ma_tight, is_signal
from ui.components import render_price_chart


@st.cache_data(ttl=300)
def _fetch_and_compute(ticker: str) -> pd.DataFrame:
    """Fetch stock data and compute all indicators, cached for 5 minutes."""
    df = fetch_stock_data(ticker)
    if df is None or df.empty:
        return pd.DataFrame()
    if len(df) < 10:
        return df
    df = calculate_all_indicators(df)
    df["MA_Tight"] = (
        (df["Range_Ticks"] < 6) & (df["Vol_Pct"] < 3.8)
    )
    return df


def render_stock_detail() -> None:
    """Render the stock detail page."""
    st.title("📈 Detail Saham")
    st.markdown("Tampilkan chart harga, Moving Average, dan indikator untuk saham pilihan.")
    st.divider()

    # Ticker input
    results = st.session_state.get("results", pd.DataFrame())
    
    # Status filters - always available
    st.subheader("🔍 Filter Status")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        filter_ma = st.multiselect(
            "🔗 Filter Status MA",
            options=["MA Tight", "Tidak MA Tight"],
            default=["MA Tight", "Tidak MA Tight"],
            help="Filter berdasarkan kondisi MA Kuncup/MA Ketat",
        )
    with col_f2:
        filter_signal = st.multiselect(
            "🚀 Filter Status Entry",
            options=["Sinyal Aktif", "Belum Sinyal"],
            default=["Sinyal Aktif", "Belum Sinyal"],
            help="Filter berdasarkan sinyal entry yang valid",
        )

    st.divider()
    
    if not results.empty and "Ticker" in results.columns:
        # Apply filters
        filtered_results = results.copy()
        if filter_ma:
            if "MA Tight" in filter_ma and "Tidak MA Tight" not in filter_ma:
                filtered_results = filtered_results[filtered_results["MA_Tight"] == True]
            elif "Tidak MA Tight" in filter_ma and "MA Tight" not in filter_ma:
                filtered_results = filtered_results[filtered_results["MA_Tight"] == False]

        if filter_signal:
            if "Sinyal Aktif" in filter_signal and "Belum Sinyal" not in filter_signal:
                filtered_results = filtered_results[filtered_results["Signal"] == True]
            elif "Belum Sinyal" in filter_signal and "Sinyal Aktif" not in filter_signal:
                filtered_results = filtered_results[filtered_results["Signal"] == False]

        ticker_list = sorted(filtered_results["Ticker"].dropna().unique().tolist())
        
        if not ticker_list:
            st.warning("Tidak ada saham yang sesuai dengan filter yang dipilih.")
            return

        ticker = st.selectbox(
            "Pilih Ticker",
            options=ticker_list,
            help=f"Daftar saham dari hasil scan terakhir (tersaring: {len(ticker_list)} saham)",
        )
    else:
        ticker = st.text_input(
            "Masukkan Ticker Saham (contoh: BBCA)",
            value="BBCA",
            help="Masukkan kode saham BEI tanpa suffix .JK",
        ).upper().strip()

    if not ticker:
        st.warning("Masukkan kode saham terlebih dahulu.")
        return

    with st.spinner(f"Mengambil data {ticker}..."):
        df = _fetch_and_compute(ticker)

    if df.empty:
        st.error(
            f"Data untuk **{ticker}** tidak tersedia. "
            "Pastikan kode saham benar dan terdaftar di BEI."
        )
        return

    # Status badges
    latest = df.iloc[-1]
    ma_tight_val = latest.get("MA_Tight", False)
    signal_val = False
    if "Range_Ticks" in latest and "Vol_Pct" in latest:
        signal_val = is_signal(latest)

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
    recent_df = df[available_cols].tail(20).copy()
    recent_df.index = recent_df.index.strftime("%Y-%m-%d")

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
