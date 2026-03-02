"""Dashboard utama Screener MA Kuncup."""

import os
from datetime import datetime

import pandas as pd
import streamlit as st

from screener.data import fetch_stock_data, load_stock_list
from screener.fetch_bei_stocks import fetch_all_bei_tickers_from_yahoo
from screener.indicators import calculate_all_indicators
from ui.components import render_metric_cards, render_results_table

BEI_STOCKS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "bei_stocks.csv")
BEI_STOCKS_FILE = os.path.abspath(BEI_STOCKS_FILE)
YAHOO_STOCKS_FILE = os.path.join(os.path.dirname(__file__), "..", "..", "data", "all_stocks.csv")
YAHOO_STOCKS_FILE = os.path.abspath(YAHOO_STOCKS_FILE)


def _screen_with_params(
    ticker: str,
    range_ticks_threshold: float,
    vol_pct_threshold: float,
    min_volume: int,
) -> "pd.Series | None":
    """Screen a single stock using caller-supplied thresholds (no global mutation)."""
    df = fetch_stock_data(ticker)
    if df is None or df.empty or len(df) < 100:
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


@st.cache_data(ttl=300)
def cached_run_screener(
    symbols: tuple,
    range_ticks_threshold: float,
    vol_pct_threshold: float,
    min_volume: int,
) -> pd.DataFrame:
    """Run screener with custom thresholds, cached for 5 minutes."""
    records = []
    for ticker in symbols:
        result = _screen_with_params(ticker, range_ticks_threshold, vol_pct_threshold, min_volume)
        if result is not None:
            records.append(result)

    if not records:
        return pd.DataFrame()

    output_cols = [
        "Ticker", "Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100",
        "Range_Ticks", "Vol_Pct", "Volume", "MA_Tight", "Signal",
    ]
    df_out = pd.DataFrame(records)
    df_out = df_out[[c for c in output_cols if c in df_out.columns]].reset_index(drop=True)
    return df_out


def _get_bei_symbols() -> list:
    """Load BEI symbols from cached IDX list (around 500+ symbols)."""
    try:
        symbols = load_stock_list(BEI_STOCKS_FILE)
    except FileNotFoundError:
        return []

    # Keep order, remove duplicates/empty values.
    cleaned = [s for s in symbols if isinstance(s, str) and s.strip()]
    return list(dict.fromkeys(cleaned))


def _get_yahoo_symbols() -> list:
    """Load BEI symbols from Yahoo screener cache (around 800+ symbols)."""
    try:
        symbols = load_stock_list(YAHOO_STOCKS_FILE)
    except FileNotFoundError:
        return []

    cleaned = [s for s in symbols if isinstance(s, str) and s.strip()]
    return list(dict.fromkeys(cleaned))


def render_dashboard() -> None:
    """Render the main dashboard page."""
    st.title("📊 Screener MA Kuncup")
    st.markdown(
        "Deteksi pola **MA Kuncup / MA Ketat** secara otomatis di Bursa Efek Indonesia (BEI). "
        "Berdasarkan teknik **Pak T [@TradingDiary2](https://x.com/TradingDiary2)** "
        "yang dirangkum oleh **[@ikhwanuddin](https://x.com/ikhwanuddin)**."
    )
    st.divider()

    # --- Sidebar parameters ---
    with st.sidebar:
        st.markdown("### ⚙️ Parameter Screener")

        range_ticks = st.slider(
            "Range Ticks Threshold",
            min_value=1,
            max_value=20,
            value=6,
            step=1,
            help="Batas maksimum rentang MA dalam satuan tick BEI",
        )
        vol_pct = st.slider(
            "Volatilitas Threshold (%)",
            min_value=0.5,
            max_value=10.0,
            value=3.8,
            step=0.1,
            format="%.1f",
            help="Batas maksimum volatilitas harian rolling 10 hari (%)",
        )
        min_volume = st.slider(
            "Volume Minimum",
            min_value=0,
            max_value=10_000_000,
            value=1_000_000,
            step=100_000,
            format="%d",
            help="Volume minimum untuk sinyal valid",
        )

        data_source = st.selectbox(
            "Sumber Data",
            options=["Saham BEI (±500, cache IDX)", "Saham Yahoo (±800, cache yfinance)"],
            index=0,
        )

        # Dynamic button label based on selected data source
        if data_source == "Saham BEI (±500, cache IDX)":
            button_label = "🔄 Update saham BEI (500-an)"
        else:
            button_label = "🔄 Update saham Yahoo (800-an)"
        
        refresh_all_stocks = st.button(
            button_label,
            use_container_width=True,
        )

        show_signals_only = st.checkbox("Tampilkan hanya sinyal", value=False)

        run_button = st.button("🔍 Jalankan Screener", use_container_width=True, type="primary")

        st.divider()
        st.caption("ℹ️ Data diambil dari Yahoo Finance (yfinance).")

    if refresh_all_stocks:
        if data_source == "Saham BEI (±500, cache IDX)":
            with st.spinner("Memperbarui daftar saham BEI dari IDX API..."):
                try:
                    from screener.fetch_bei_stocks import fetch_all_bei_tickers
                    refreshed = fetch_all_bei_tickers(csv_path=BEI_STOCKS_FILE, update_csv=True)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Gagal update daftar saham dari IDX: {exc}")
                else:
                    st.success(f"Berhasil update {len(refreshed)} ticker ke bei_stocks.csv")
        else:
            with st.spinner("Memperbarui daftar saham BEI dari Yahoo..."):
                try:
                    refreshed = fetch_all_bei_tickers_from_yahoo(csv_path=YAHOO_STOCKS_FILE, update_csv=True)
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Gagal update daftar saham dari Yahoo: {exc}")
                else:
                    st.success(f"Berhasil update {len(refreshed)} ticker ke all_stocks.csv")

    # --- Load stock list ---
    if data_source == "Saham BEI (±500, cache IDX)":
        symbols = _get_bei_symbols()
        if not symbols:
            st.error(f"File bei_stocks.csv tidak ditemukan di: {BEI_STOCKS_FILE}")
            return
    else:
        symbols = _get_yahoo_symbols()
        if not symbols:
            st.error(f"File all_stocks.csv tidak ditemukan di: {YAHOO_STOCKS_FILE}")
            return

    # --- Run screener on button press ---
    if run_button:
        with st.spinner(f"Menjalankan screener untuk {len(symbols)} saham..."):
            results = cached_run_screener(
                tuple(symbols), range_ticks, vol_pct, min_volume
            )
        st.session_state["results"] = results
        st.session_state["scan_time"] = datetime.now().strftime("%H:%M:%S")
        st.session_state["symbols_scanned"] = len(symbols)

    # --- Display results ---
    results = st.session_state.get("results", pd.DataFrame())
    scan_time = st.session_state.get("scan_time", "-")
    symbols_scanned = st.session_state.get("symbols_scanned", 0)

    ma_tight_count = 0
    signal_count = 0
    if not results.empty:
        if "MA_Tight" in results.columns:
            ma_tight_count = int(results["MA_Tight"].sum())
        if "Signal" in results.columns:
            signal_count = int(results["Signal"].sum())

    render_metric_cards(
        total=symbols_scanned,
        ma_tight_count=ma_tight_count,
        signal_count=signal_count,
        timestamp=scan_time,
    )

    st.divider()

    if not results.empty:
        st.subheader("📋 Hasil Screener")

        # Download CSV button
        csv_data = results.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv_data,
            file_name=f"screener_ma_kuncup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
        )

        render_results_table(results, show_signals_only=show_signals_only)
    else:
        st.info("Klik **🔍 Jalankan Screener** di sidebar untuk memulai scan.")

    # Footer
    st.divider()
    st.caption(
        "⚠️ **Disclaimer**: Screener ini dibuat untuk tujuan edukasi dan riset. "
        "**Bukan merupakan rekomendasi investasi.** "
        "Keputusan beli/jual sepenuhnya tanggung jawab masing-masing investor."
    )
