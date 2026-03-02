"""Entry point for the Screener MA Kuncup Streamlit app."""

import streamlit as st

st.set_page_config(
    page_title="Screener MA Kuncup",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject custom CSS
try:
    from ui.styles import inject_custom_css
    inject_custom_css(st)
except Exception:
    pass  # Fallback gracefully if styles cannot be loaded

# Navigation using tabs
tab1, tab2, tab3 = st.tabs(["🏠 Dashboard", "📈 Detail Saham", "📅 Riwayat"])

with tab1:
    from ui.pages.dashboard import render_dashboard
    render_dashboard()

with tab2:
    from ui.pages.stock_detail import render_stock_detail
    render_stock_detail()

with tab3:
    from ui.pages.history import render_history
    render_history()
