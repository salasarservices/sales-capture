"""
Salasar Services — Sales Dashboard
Entry point with page routing based on sidebar navigation.
"""

import streamlit as st
import st_tailwind as tw

st.set_page_config(
    page_title="Salasar Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Tailwind CSS Play CDN globally — must be called right after set_page_config.
# All custom HTML components (KPI cards, tables, sidebar cards) use Tailwind utility
# classes. A minimal _STREAMLIT_OVERRIDES block handles Streamlit-internal selectors
# that Tailwind cannot reach ([data-testid="stSidebar"], .stPlotlyChart, etc.).
tw.initialize_tailwind()

from utils.styles import inject_global_css
from utils.auth import login_form, is_admin

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

inject_global_css()

# ── Import sidebar ───────────────────────────────────────────────────────────
from components.sidebar import render_sidebar, get_current_page

# Render sidebar
render_sidebar()

# ── Page routing based on sidebar selection ─────────────────────────────────
current_page = get_current_page()

if current_page == "Business Conversion Ratio":
    from pages.business_conversion import render_page
    render_page()
elif current_page == "Sales Capture Summary":
    from pages.sales_capture import render_page
    render_page()
elif current_page == "Conversion Ratio Summary":
    from pages.conversion_ratio import render_page
    render_page()
elif current_page == "Master Data (From April 25 to March 26)":
    from pages.master_data import render_page
    render_page()
else:
    # Default to Business Conversion Ratio
    from pages.business_conversion import render_page
    render_page()