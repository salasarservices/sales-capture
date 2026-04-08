"""
Salasar Services — Sales Dashboard
Entry point. Shows login form; authenticated users see the page navigation.
"""

import streamlit as st

st.set_page_config(
    page_title="Salasar Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.auth import login_form, logout, is_admin
from components.theme import apply_theme, render_hero

apply_theme()

# ---- Auth gate ----
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

# ---- Sidebar header ----
with st.sidebar:
    st.markdown(
        """
        <div style='padding: 0.5rem 0 1rem 0;'>
            <h2 style='color:#1E3A5F; margin:0;'>Salasar Services</h2>
            <p style='color:#64748B; font-size:0.85rem; margin:0;'>
            <h2 style='margin:0;'>Salasar Services</h2>
            <p style='font-size:0.85rem; margin:0; opacity:0.9;'>
                Ahmedabad Branch &nbsp;|&nbsp; FY 2025-26
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.divider()
    role_label = "Admin" if is_admin() else "Viewer"
    st.caption(f"Signed in as **{st.session_state.username}** ({role_label})")
    if st.button("Sign Out", use_container_width=True):
        logout()

# ---- Home page content ----
st.title("Sales Dashboard — Ahmedabad FY 2025-26")
render_hero(
    "Sales Dashboard — Ahmedabad FY 2025-26",
    "A unified view of conversion ratio, sales capture, monthly performance, and funnel drop-off.",
)

st.markdown(
    """
    Use the **sidebar pages** to navigate between dashboard views:

    | Page | Description |
    |---|---|
    | 📊 Summary: Conversion Ratio | Per CRE/RM breakdown by Fresh / Renewal / Expanded |
    | 📈 Summary: Sales Capture | Per CRE/RM totals, premium, and conversion |
    | 📅 Business Conversion Ratio | Monthly enquiry count and conversion rate |
    | 🔍 Sales Funnel | Funnel visualisation + filterable enquiry detail |
    """
)
