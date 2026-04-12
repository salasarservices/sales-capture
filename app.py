"""
Salasar Services — Sales Dashboard
Entry point: auth gate + home page overview.
Based on UI-DESIGN-INSTRUCTION.md
"""

import streamlit as st

st.set_page_config(
    page_title="Salasar Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.styles import inject_global_css
from utils.auth import login_form

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

inject_global_css()

# ── Import sidebar and header ────────────────────────────────────────────────
from components.sidebar import render_sidebar, render_header, get_active_filters

# Render sidebar
render_sidebar()

# Render header
render_header()

# ── Home page ─────────────────────────────────────────────────────────────────
st.markdown('<p class="section-heading">Dashboard Overview</p>', unsafe_allow_html=True)
st.caption("Use the sidebar filters to refresh KPI and page-level modules instantly.")

# ── Live KPI summary ──────────────────────────────────────────────────────────
from database.connection import get_db
from database.queries import fetch_kpis
from components.kpi_cards import render_kpi_row

db = get_db()
with st.spinner("Loading summary…"):
    filters = get_active_filters()
    month_map = {"Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12, "Jan": 1, "Feb": 2, "Mar": 3}
    month_ints = [month_map[m] for m in filters["months"]]
    kpis = fetch_kpis(
        db,
        fy=filters["fy"],
        branch=filters["branch"],
        cre_rms=filters["cre_rms"],
        proposal_types=filters["proposal_types"],
        requirements=filters["requirements"],
        months=month_ints,
    )

render_kpi_row(kpis)

st.markdown("<div style='height: 1rem'></div>", unsafe_allow_html=True)

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
