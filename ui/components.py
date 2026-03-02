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
    """Apply green highlight to rows where Signal == True."""
    def highlight_signal(row):
        if row.get("Signal") is True or row.get("Signal") == 1:
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

    # Format numeric columns
    float_cols = ["Close", "MA3", "MA5", "MA10", "MA20", "MA50", "MA100", "Range_Ticks", "Vol_Pct"]
    for col in float_cols:
        if col in display_df.columns:
            display_df[col] = display_df[col].round(2)

    if "Volume" in display_df.columns:
        display_df["Volume"] = display_df["Volume"].apply(
            lambda v: f"{int(v):,}" if pd.notna(v) else "-"
        )

    styled = style_signal_rows(display_df)
    st.dataframe(styled, use_container_width=True, hide_index=True)


def render_price_chart(df: pd.DataFrame, ticker: str) -> None:
    """Render an interactive candlestick/line chart with MA overlay using Plotly."""
    if df.empty:
        st.warning(f"Tidak ada data untuk {ticker}.")
        return

    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        row_heights=[0.75, 0.25],
        vertical_spacing=0.05,
        subplot_titles=(f"Harga & Moving Average — {ticker}", "Volume"),
    )

    # Close price line
    fig.add_trace(
        go.Scatter(
            x=df.index, y=df["Close"],
            name="Close",
            line=dict(color="#ffffff", width=1.5),
        ),
        row=1, col=1,
    )

    # MA lines
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
                    line=dict(color=color, width=1),
                    opacity=0.8,
                ),
                row=1, col=1,
            )

    # Volume bars
    if "Volume" in df.columns:
        fig.add_trace(
            go.Bar(
                x=df.index, y=df["Volume"],
                name="Volume",
                marker_color="rgba(100, 150, 200, 0.6)",
            ),
            row=2, col=1,
        )

    fig.update_layout(
        template="plotly_dark",
        height=600,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis_rangeslider_visible=False,
        margin=dict(l=0, r=0, t=30, b=0),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.1)")

    st.plotly_chart(fig, use_container_width=True)


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
        title=f"Volume — {ticker}",
        height=200,
        margin=dict(l=0, r=0, t=30, b=0),
        showlegend=False,
    )
    st.plotly_chart(fig, use_container_width=True)
