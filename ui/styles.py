"""Custom CSS styles for Screener MA Kuncup UI."""


CUSTOM_CSS = """
<style>
/* Metric cards */
.metric-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8e 100%);
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    margin-bottom: 10px;
}

.metric-card h3 {
    color: #a8c6e8;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.metric-card .value {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    line-height: 1;
}

.metric-card .subtext {
    color: #7aa8d0;
    font-size: 0.75rem;
    margin-top: 6px;
}

/* Signal row highlighting in dataframe */
.signal-true {
    background-color: rgba(0, 200, 100, 0.15) !important;
    color: #00c864 !important;
}

/* Sidebar styling */
.sidebar-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: #a8c6e8;
    padding: 10px 0;
    border-bottom: 1px solid rgba(255,255,255,0.1);
    margin-bottom: 15px;
}

/* Footer disclaimer */
.footer-disclaimer {
    text-align: center;
    color: #666;
    font-size: 0.75rem;
    padding: 10px;
    border-top: 1px solid rgba(255,255,255,0.1);
    margin-top: 20px;
}

/* Status badges */
.badge-true {
    background-color: rgba(0, 200, 100, 0.2);
    color: #00c864;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
}

.badge-false {
    background-color: rgba(200, 50, 50, 0.2);
    color: #ff4444;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 0.8rem;
    font-weight: 600;
}

/* Responsive adjustments */
@media (max-width: 768px) {
    .metric-card .value {
        font-size: 1.5rem;
    }
}
</style>
"""


def inject_custom_css(st) -> None:
    """Inject custom CSS into the Streamlit app."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
