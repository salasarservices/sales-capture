"""
Global CSS injection and brand color constants for Salasar Sales Dashboard.
Call inject_global_css() at the top of every page after set_page_config().
"""

import streamlit as st

# ── Brand Color Palette ──────────────────────────────────────────────────────
COLORS = {
    "navy":       "#1B3A6B",
    "navy_dk":    "#0F2547",
    "navy_lt":    "#2D5FA8",
    "gold":       "#C8860A",
    "gold_lt":    "#FDF7ED",
    "green":      "#15803D",
    "green_lt":   "#ECFDF5",
    "red":        "#B91C1C",
    "red_lt":     "#FEF2F2",
    "amber":      "#D97706",
    "amber_lt":   "#FFFBEB",
    "blue":       "#2563EB",
    "blue_lt":    "#EFF6FF",
    "purple":     "#7C3AED",
    "purple_lt":  "#F5F3FF",
    "bg":         "#F0F4F8",
    "card":       "#FFFFFF",
    "text":       "#1E293B",
    "muted":      "#64748B",
    "border":     "#E2E8F0",
    "border_lt":  "#F1F5F9",
}

# Plotly chart palette (used by components/charts.py)
CHART = {
    "converted":     "#15803D",
    "not_converted": "#B91C1C",
    "navy":          "#1B3A6B",
    "gold":          "#C8860A",
    "blue":          "#2563EB",
    "purple":        "#7C3AED",
    "amber":         "#D97706",
    "teal":          "#0D9488",
}

_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   SALASAR SERVICES — SALES DASHBOARD  |  Global UI Styles
   Brand: Navy #1B3A6B  ·  Gold #C8860A  ·  Background #F0F4F8
═══════════════════════════════════════════════════════════════════════════ */

/* ── Hide Streamlit chrome ────────────────────────────────────────────────── */
#MainMenu,
footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* ── Page background ──────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] > section.main {
    background-color: #F0F4F8;
}
.main .block-container {
    padding-top: 1.75rem;
    padding-bottom: 3rem;
    max-width: 100%;
}

/* ── Sidebar ──────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0F2547 0%, #1B3A6B 55%, #1E4080 100%) !important;
    border-right: none !important;
    box-shadow: 2px 0 12px rgba(0, 0, 0, 0.15) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* Sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span:not([data-testid="stSidebarNavLinkText"]),
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small {
    color: rgba(255, 255, 255, 0.72) !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFFFFF !important;
}

/* Sidebar divider */
[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.12) !important;
    margin: 0.6rem 0 !important;
}

/* Sidebar nav links */
[data-testid="stSidebarNavLink"] {
    border-radius: 8px !important;
    margin: 2px 8px !important;
    padding: 0.45rem 0.75rem !important;
    transition: all 0.15s ease !important;
    border-left: 3px solid transparent !important;
}
[data-testid="stSidebarNavLink"]:hover {
    background: rgba(255, 255, 255, 0.09) !important;
}
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: rgba(200, 134, 10, 0.22) !important;
    border-left-color: #C8860A !important;
}
[data-testid="stSidebarNavLink"] span,
[data-testid="stSidebarNavLink"] p {
    color: rgba(255, 255, 255, 0.88) !important;
    font-weight: 500 !important;
}
[data-testid="stSidebarNavLink"][aria-selected="true"] span,
[data-testid="stSidebarNavLink"][aria-selected="true"] p {
    color: #FFFFFF !important;
    font-weight: 600 !important;
}

/* Sidebar sign-out button */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255, 255, 255, 0.07) !important;
    color: rgba(255, 255, 255, 0.82) !important;
    border: 1px solid rgba(255, 255, 255, 0.16) !important;
    border-radius: 8px !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.14) !important;
    color: #FFFFFF !important;
    border-color: rgba(255, 255, 255, 0.3) !important;
}

/* ── Typography ───────────────────────────────────────────────────────────── */
h1 {
    color: #1B3A6B !important;
    font-weight: 700 !important;
    letter-spacing: -0.4px !important;
    font-size: 1.65rem !important;
}
h2 {
    color: #1E293B !important;
    font-weight: 600 !important;
    font-size: 1.25rem !important;
}
h3 {
    color: #1E293B !important;
    font-weight: 600 !important;
    font-size: 1.05rem !important;
}

/* ── Dividers ─────────────────────────────────────────────────────────────── */
hr {
    border-color: #E2E8F0 !important;
    margin: 0.75rem 0 !important;
}

/* ── KPI Cards ────────────────────────────────────────────────────────────── */
.kpi-card {
    background: #FFFFFF;
    border-radius: 14px;
    padding: 1.1rem 1.2rem;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.07), 0 0 0 1px rgba(0, 0, 0, 0.03);
    display: flex;
    align-items: center;
    gap: 0.85rem;
    min-height: 82px;
    position: relative;
    overflow: hidden;
    border-top: 3px solid transparent;
}
.kpi-card.navy   { border-top-color: #1B3A6B; }
.kpi-card.gold   { border-top-color: #C8860A; }
.kpi-card.green  { border-top-color: #15803D; }
.kpi-card.blue   { border-top-color: #2563EB; }
.kpi-card.purple { border-top-color: #7C3AED; }
.kpi-card.red    { border-top-color: #B91C1C; }
.kpi-card.teal   { border-top-color: #0D9488; }

.kpi-icon {
    font-size: 1.55rem;
    width: 46px;
    height: 46px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    flex-shrink: 0;
}
.kpi-card.navy   .kpi-icon { background: #EEF2FB; }
.kpi-card.gold   .kpi-icon { background: #FDF7ED; }
.kpi-card.green  .kpi-icon { background: #ECFDF5; }
.kpi-card.blue   .kpi-icon { background: #EFF6FF; }
.kpi-card.purple .kpi-icon { background: #F5F3FF; }
.kpi-card.red    .kpi-icon { background: #FEF2F2; }
.kpi-card.teal   .kpi-icon { background: #F0FDFA; }

.kpi-content { flex: 1; min-width: 0; }

.kpi-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #94A3B8;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 0.3rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.kpi-value {
    font-size: 1.45rem;
    font-weight: 700;
    color: #1E293B;
    line-height: 1.15;
    letter-spacing: -0.4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Home-page nav cards ──────────────────────────────────────────────────── */
.nav-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.75rem;
    margin-top: 1rem;
}
.nav-card {
    background: #FFFFFF;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
    border-left: 4px solid #1B3A6B;
    transition: all 0.2s ease;
    cursor: default;
}
.nav-card:hover {
    box-shadow: 0 4px 16px rgba(27, 58, 107, 0.14);
    border-left-color: #C8860A;
    transform: translateX(3px);
}
.nav-card-header {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 0.35rem;
}
.nav-card-icon { font-size: 1.2rem; }
.nav-card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: #1B3A6B;
    margin: 0;
}
.nav-card-desc {
    font-size: 0.82rem;
    color: #64748B;
    line-height: 1.45;
    margin: 0;
}

/* ── Form Submit Button ───────────────────────────────────────────────────── */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #1B3A6B 0%, #2D5FA8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.65rem 1.5rem !important;
    transition: all 0.2s ease !important;
    width: 100% !important;
}
.stFormSubmitButton > button:hover {
    box-shadow: 0 4px 16px rgba(27, 58, 107, 0.38) !important;
    transform: translateY(-1px) !important;
}

/* ── Login form card ──────────────────────────────────────────────────────── */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border-radius: 16px !important;
    padding: 1.75rem !important;
    box-shadow: 0 6px 28px rgba(0, 0, 0, 0.10) !important;
    border: 1px solid #E2E8F0 !important;
}

/* ── Download / Export button ─────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: #F0FDF4 !important;
    color: #15803D !important;
    border: 1px solid #86EFAC !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    transition: all 0.15s ease !important;
}
[data-testid="stDownloadButton"] > button:hover {
    background: #DCFCE7 !important;
    border-color: #4ADE80 !important;
}

/* ── Pagination / generic buttons ─────────────────────────────────────────── */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 500 !important;
    transition: all 0.15s ease !important;
}

/* ── Filter expander panel ────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    margin-bottom: 1rem !important;
}
[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #1B3A6B !important;
}

/* ── DataFrames ───────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border-radius: 10px !important;
    overflow: hidden !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    border: 1px solid #E2E8F0 !important;
}

/* ── Native st.metric cards ───────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    border-radius: 10px !important;
    padding: 1rem 1.25rem !important;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06) !important;
    border: 1px solid #F1F5F9 !important;
}
[data-testid="stMetricLabel"] p {
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    color: #94A3B8 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.5px !important;
}
[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-weight: 700 !important;
    color: #1E293B !important;
}

/* ── Plotly chart wrapper ─────────────────────────────────────────────────── */
.stPlotlyChart {
    background: #FFFFFF !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06) !important;
    padding: 0.4rem !important;
    border: 1px solid #F1F5F9 !important;
}

/* ── Multiselect tags ─────────────────────────────────────────────────────── */
[data-baseweb="tag"] {
    background-color: #EEF2FB !important;
    color: #1B3A6B !important;
    border: none !important;
    border-radius: 6px !important;
}

/* ── Text inputs ──────────────────────────────────────────────────────────── */
.stTextInput input {
    border-radius: 8px !important;
    border-color: #CBD5E1 !important;
    transition: all 0.15s ease !important;
}
.stTextInput input:focus {
    border-color: #1B3A6B !important;
    box-shadow: 0 0 0 2px rgba(27, 58, 107, 0.12) !important;
}

/* ── Captions ─────────────────────────────────────────────────────────────── */
.stCaption p,
[data-testid="stCaptionContainer"] p {
    color: #94A3B8 !important;
    font-size: 0.80rem !important;
}

/* ── Alerts ───────────────────────────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* ── Section heading row ──────────────────────────────────────────────────── */
.section-heading {
    font-size: 1rem;
    font-weight: 600;
    color: #1E293B;
    border-left: 3px solid #C8860A;
    padding-left: 0.65rem;
    margin: 0.5rem 0 0.75rem 0;
    line-height: 1.3;
}

/* ── Welcome banner (home page) ───────────────────────────────────────────── */
.welcome-banner {
    background: linear-gradient(135deg, #1B3A6B 0%, #2D5FA8 100%);
    border-radius: 14px;
    padding: 1.5rem 2rem;
    color: white;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}
.welcome-banner h2 {
    color: #FFFFFF !important;
    font-size: 1.3rem !important;
    margin: 0 0 0.2rem 0 !important;
    font-weight: 700 !important;
}
.welcome-banner p {
    color: rgba(255, 255, 255, 0.72);
    margin: 0;
    font-size: 0.88rem;
}
.welcome-badge {
    background: rgba(255, 255, 255, 0.15);
    border: 1px solid rgba(255, 255, 255, 0.25);
    border-radius: 999px;
    padding: 0.3rem 0.9rem;
    font-size: 0.82rem;
    font-weight: 600;
    color: rgba(255, 255, 255, 0.95);
    white-space: nowrap;
}

/* ── Page sub-title caption ───────────────────────────────────────────────── */
.page-subtitle {
    font-size: 0.85rem;
    color: #64748B;
    margin: -0.6rem 0 1rem 0;
}
</style>
"""


def inject_global_css():
    """Inject dashboard-wide custom CSS. Call once per page, after set_page_config()."""
    st.markdown(_CSS, unsafe_allow_html=True)
