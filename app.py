"""
Salasar Services — Sales Dashboard
Entry point with page routing based on sidebar navigation.
"""

import streamlit as st

st.set_page_config(
    page_title="Salasar Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_global_css
from utils.auth import login_form, is_admin
from utils.tailwind import initialize_tailwind

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

inject_global_css()
initialize_tailwind()

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
elif current_page == "Master Data":
    from pages.master_data import render_page
    render_page()
else:
    # Default to Business Conversion Ratio
    from pages.business_conversion import render_page
    render_page()
