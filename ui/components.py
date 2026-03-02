"""Reusable UI components for Screener MA Kuncup."""

import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


def render_metric_cards(total: int, ma_tight_count: int, signal_count: int, timestamp: str) -> None:
    """Render summary metric cards in a 4-column layout."""
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="📋 Total Saham Di-scan", value=total)
    with col2:
        st.metric(label="🔗 MA Tight", value=ma_tight_count)
    with col3:
        st.metric(label="🚀 Sinyal Siap Entry", value=signal_count)
    with col4:
        st.metric(label="🕒 Waktu Scan", value=timestamp)


def style_signal_rows(df: pd.DataFrame) -> "pd.io.formats.style.Styler":
    """Apply green highlight to rows where Signal == True/✅."""

    def highlight_signal(row):
        signal_value = row.get("Signal")
        if signal_value is True or signal_value == 1 or signal_value == "✅":
            return ["background-color: rgba(0, 200, 100, 0.15); color: #00c864"] * len(row)
        return [""] * len(row)

    return df.style.apply(highlight_signal, axis=1)


def render_results_table(df: pd.DataFrame, show_signals_only: bool = False) -> None:
    """Render the screener results table with optional signal filtering."""
    if df.empty:
        st.info("Belum ada data. Klik 'Jalankan Screener' untuk memulai.")
        return

    display_df = df.copy()
    if show_signals_only:
        display_df = display_df[display_df["Signal"].eq(True)]
        if display_df.empty:
            st.info("Tidak ada saham dengan sinyal MA Kuncup saat ini.")
            return

    preferred_order = [
        "Ticker",
        "Close",
        "MA3",
        "MA5",
        "MA10",
        "MA20",
        "MA50",
        "MA100",
        "Range_Ticks",
        "Vol_Pct",
        "Volume",
        "MA_Tight",
        "Signal",
    ]
    display_df = display_df[[c for c in preferred_order if c in display_df.columns]]

    if {"Signal", "MA_Tight", "Range_Ticks", "Vol_Pct"}.issubset(display_df.columns):
        display_df = display_df.sort_values(
            by=["Signal", "MA_Tight", "Range_Ticks", "Vol_Pct"],
            ascending=[False, False, True, True],
        )

    for col in ["Signal", "MA_Tight"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].map(lambda v: "✅" if bool(v) else "❌")

    styled = style_signal_rows(display_df).format(
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

    st.dataframe(styled, width="stretch", hide_index=True)


def render_price_chart(df: pd.DataFrame, ticker: str) -> None:
    """Render TradingView-like chart: OHLC candlestick + MA overlays + Volume MA20."""
    if df.empty:
        st.warning(f"Tidak ada data untuk {ticker}.")
        return

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.70, 0.30],
        vertical_spacing=0.03,
    )

    # Price as candlestick OHLC (fallback to Close line if OHLC is unavailable)
    ohlc_cols = {"Open", "High", "Low", "Close"}
    if ohlc_cols.issubset(df.columns):
        fig.add_trace(
            go.Candlestick(
                x=df.index,
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
                name="OHLC",
                increasing=dict(
                    line=dict(color="#089981", width=1.5),
                    fillcolor="#089981"
                ),
                decreasing=dict(
                    line=dict(color="#F23645", width=1.5),
                    fillcolor="#F23645"
                ),
                whiskerwidth=0.8,
                line=dict(width=1.2),
                hovertemplate=(
                    "<b>%{x|%d-%m-%Y}</b><br>"
                    "Open: %{open:,.2f}<br>"
                    "High: %{high:,.2f}<br>"
                    "Low: %{low:,.2f}<br>"
                    "Close: %{close:,.2f}"
                    "<extra></extra>"
                ),
            ),
            row=1,
            col=1,
        )
    elif "Close" in df.columns:
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=df["Close"],
                name="Close",
                line=dict(color="#ffffff", width=2),
                hovertemplate="<b>%{x|%d-%m-%Y}</b><br>Close: %{y:,.2f}<extra></extra>",
            ),
            row=1,
            col=1,
        )

    # MA lines - all visible by default
    ma_colors = {
        "MA3": "#ff6b6b",
        "MA5": "#ffa500",
        "MA10": "#ffd700",
        "MA20": "#7fff00",
        "MA50": "#00bfff",
        "MA100": "#da70d6",
    }
    for ma_col, color in ma_colors.items():
        if ma_col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df.index, y=df[ma_col],
                    name=ma_col,
                    line=dict(color=color, width=1.5),
                    opacity=0.9,
                    hovertemplate=f"{ma_col}: %{{y:,.2f}}<extra></extra>",
                ),
                row=1, col=1,
            )

    # Volume bars + MA20
    if "Volume" in df.columns:
        if {"Open", "Close"}.issubset(df.columns):
            volume_colors = [
                "rgba(38, 166, 154, 0.6)" if close_val >= open_val else "rgba(239, 83, 80, 0.6)"
                for open_val, close_val in zip(df["Open"], df["Close"])
            ]
        else:
            volume_colors = "rgba(100, 150, 200, 0.5)"

        fig.add_trace(
            go.Bar(
                x=df.index, y=df["Volume"],
                name="Volume",
                marker_color=volume_colors,
                hovertemplate="Volume: %{y:,.0f}<extra></extra>",
            ),
            row=2, col=1,
        )

        volume_ma20 = df["Volume"].rolling(window=20, min_periods=1).mean()
        fig.add_trace(
            go.Scatter(
                x=df.index,
                y=volume_ma20,
                name="Vol MA20",
                line=dict(color="#ffd700", width=1.5),
                hovertemplate="Vol MA20: %{y:,.0f}<extra></extra>",
            ),
            row=2,
            col=1,
        )

    fig.update_layout(
        template="plotly_dark",
        height=650,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(0,0,0,0.7)",
            bordercolor="rgba(255,255,255,0.3)",
            borderwidth=1,
            font=dict(size=10),
            itemclick="toggle",
            itemdoubleclick="toggleothers",
            itemsizing="constant",
        ),
        xaxis_rangeslider_visible=False,
        margin=dict(l=10, r=10, t=10, b=10),
        hovermode="x unified",
        hoverlabel=dict(namelength=-1),
    )
    fig.update_xaxes(
        showgrid=True,
        gridcolor="rgba(255,255,255,0.08)",
        showspikes=True,
        spikemode="across",
        spikesnap="cursor",
        spikecolor="rgba(255,255,255,0.3)",
        spikethickness=1,
    )
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.08)")

    st.plotly_chart(fig, width='stretch')


def render_volume_chart(df: pd.DataFrame, ticker: str) -> None:
    """Render a standalone volume bar chart using Plotly."""
    if df.empty or "Volume" not in df.columns:
        return

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df.index, y=df["Volume"],
            name="Volume",
            marker_color="rgba(100, 150, 200, 0.7)",
        )
    )
    fig.update_layout(
        template="plotly_dark",
        height=200,
        margin=dict(l=0, r=0, t=10, b=0),
        showlegend=False,
    )
    st.plotly_chart(fig, width='stretch')
