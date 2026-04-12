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
from utils.auth import login_form, is_admin

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

inject_global_css()

# ── Import sidebar and header ────────────────────────────────────────────────
from components.sidebar import render_sidebar, render_header, get_filtered_data

# Render sidebar
render_sidebar()

# Render header
render_header()

# ── Home page ─────────────────────────────────────────────────────────────────
import datetime

today = datetime.date.today().strftime("%d %b %Y")
branch = st.session_state.get("branch", "Ahmedabad")
fy = st.session_state.get("fy", "2025-26")
role_label = "Admin" if is_admin() else "Viewer"
username = st.session_state.get("username", "Unknown")

st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, #042C53 0%, #185FA5 100%);
        padding: 1.4rem 2rem;
        color: white;
        margin-bottom: 1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
    ">
        <div>
            <h2 style="color: white; margin: 0 0 0.2rem; font-size: 1.25rem;">
                Welcome back, {username}!
            </h2>
            <p style="color: rgba(255,255,255,0.70); margin: 0; font-size: 0.87rem;">
                {branch} Branch · FY {fy} · {today}
            </p>
        </div>
        <div style="
            background: rgba(255,255,255,0.14);
            border: 1px solid rgba(255,255,255,0.22);
            padding: 0.28rem 0.85rem;
            font-size: 0.80rem;
            font-weight: 600;
            color: rgba(255,255,255,0.95);
        ">
            🔐 {role_label} Access
        </div>
    </div>
""", unsafe_allow_html=True)

# ── Live KPI summary ──────────────────────────────────────────────────────────
from database.connection import get_db
from database.queries import fetch_kpis
from components.kpi_cards import render_kpi_row

db = get_db()
with st.spinner("Loading summary…"):
    kpis = fetch_kpis(db, fy=st.session_state.get("fy", "2025-26"), branch=st.session_state.get("branch", "Ahmedabad"))

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