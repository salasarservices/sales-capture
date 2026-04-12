"""
Salasar Services — Sales Dashboard
Entry point: auth gate + home page overview.
"""

import streamlit as st

st.set_page_config(
    page_title="Salasar Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_global_css
from utils.auth import login_form, is_admin, render_sidebar_branding

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

inject_global_css()
render_sidebar_branding()

# ── Home page ─────────────────────────────────────────────────────────────────
import datetime

today      = datetime.date.today().strftime("%d %b %Y")
role_label = "Admin" if is_admin() else "Viewer"
username   = st.session_state.get("username", "Unknown")

st.markdown(
    f"""
    <div class="welcome-banner">
        <div>
            <h2>Welcome back, {username}!</h2>
            <p>Ahmedabad Branch &nbsp;·&nbsp; FY 2025-26 &nbsp;·&nbsp; {today}</p>
        </div>
        <div class="welcome-badge">🔐 {role_label} Access</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Live KPI summary ──────────────────────────────────────────────────────────
from database.connection import get_db
from database.queries import fetch_kpis
from components.kpi_cards import render_kpi_row

db = get_db()
with st.spinner("Loading summary…"):
    kpis = fetch_kpis(db)

render_kpi_row(kpis)
st.markdown("<div style='height:0.75rem'></div>", unsafe_allow_html=True)

# ── Navigation cards ──────────────────────────────────────────────────────────
st.markdown('<p class="section-heading">Dashboard Sections</p>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="nav-grid">
        <div class="nav-card">
            <div class="nav-card-header">
                <span class="nav-card-icon">📊</span>
                <span class="nav-card-title">Summary: Conversion Ratio</span>
            </div>
            <p class="nav-card-desc">
                Per CRE/RM breakdown by Fresh, Renewal &amp; Expanded business —
                stacked bar and grouped proposal-type charts.
            </p>
        </div>
        <div class="nav-card">
            <div class="nav-card-header">
                <span class="nav-card-icon">📈</span>
                <span class="nav-card-title">Summary: Sales Capture</span>
            </div>
            <p class="nav-card-desc">
                Enquiry volume and premium conversion per CRE/RM —
                horizontal bar, donut share chart, and summary table.
            </p>
        </div>
        <div class="nav-card">
            <div class="nav-card-header">
                <span class="nav-card-icon">📅</span>
                <span class="nav-card-title">Business Conversion Ratio</span>
            </div>
            <p class="nav-card-desc">
                Month-by-month enquiry volume and conversion rate trend —
                dual-axis chart with annual average reference line.
            </p>
        </div>
        <div class="nav-card">
            <div class="nav-card-header">
                <span class="nav-card-icon">🔍</span>
                <span class="nav-card-title">Sales Funnel &amp; Enquiry Capture</span>
            </div>
            <p class="nav-card-desc">
                Full pipeline funnel with filterable, searchable enquiry detail —
                filter by month, CRE/RM, proposal type, product, or company.
            </p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)