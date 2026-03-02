"""Entry point for the Screener MA Kuncup Streamlit app."""

import streamlit as st

st.set_page_config(
    page_title="Screener MA Kuncup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from ui.styles import inject_custom_css

inject_custom_css(st)

# Navigation
page = st.sidebar.radio(
    "Navigasi",
    ["🏠 Dashboard", "📈 Detail Saham", "📅 Riwayat"],
)

if page == "🏠 Dashboard":
    from ui.pages.dashboard import render_dashboard
    render_dashboard()
elif page == "📈 Detail Saham":
    from ui.pages.stock_detail import render_stock_detail
    render_stock_detail()
elif page == "📅 Riwayat":
    from ui.pages.history import render_history
    render_history()
