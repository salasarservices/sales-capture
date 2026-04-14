"""
Global CSS injection and brand color constants for Salasar Sales Dashboard.
Based on UI-DESIGN-INSTRUCTION.md specifications.
"""

import streamlit as st

# ── Brand Color Palette ──────────────────────────────────────────────────────
COLORS = {
    # Primary brand
    "navy": "#042C53",
    "navy_med": "#185FA5",
    "navy_lt": "#E6F1FB",
    "navy_border": "#B5D4F4",
    "navy_text": "#0C447C",
    "navy_sub": "#378ADD",
    
    # Success / Growth
    "green": "#1D9E75",
    "green_lt": "#EAF3DE",
    "green_label": "#3B6D11",
    "green_value": "#27500A",
    
    # Revenue / Currency
    "amber": "#EF9F27",
    "amber_lt": "#FAEEDA",
    "amber_label": "#854F0B",
    "amber_value": "#633806",
    
    # Neutral surfaces
    "bg": "#F8F9FA",
    "surface": "#EFF2F7",
    "card": "#FFFFFF",
    "border": "#E5E7EB",
    
    # Text
    "text": "#1A1F36",
    "text_secondary": "#6B7280",
    "text_tertiary": "#9CA3AF",
    "negative": "#A32D2D",
}

# Chart palette
CHART = {
    "fresh": "#185FA5",
    "renewal": "#1D9E75",
    "expanded": "#EF9F27",
    "blue": "#185FA5",
    "green": "#1D9E75",
    "amber": "#EF9F27",
}

# ─────────────────────────────────────────────────────────────────────────────
#  GLOBAL CSS (injected on every authenticated page)
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700;800&display=swap');

/* ═══════════════════════════════════════════════════════════════════════════
   SALASAR SERVICES — SALES DASHBOARD
   UI Design: Metric-First Layout with Sidebar Filters
═══════════════════════════════════════════════════════════════════════════ */

html, body, [class*="css"], .stApp, .stMarkdown, .stButton > button, .stTextInput input {
    font-family: 'Roboto', sans-serif !important;
}

/* ── Chrome off ──────────────────────────────────────────────────────────── */
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Page background ─────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] > section.main { background-color: #F8F9FA; }
.main .block-container { padding-top: 0.5rem; padding-bottom: 3rem; max-width: 100%; }

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 0.5px solid #E5E7EB !important;
}
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small,
[data-testid="stSidebar"] .stRadio label {
    color: #6B7280 !important;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #1A1F36 !important; }
[data-testid="stSidebar"] hr { border-color: #E5E7EB !important; }

/* ── Sidebar nav styling ──────────────────────────────────────────────────── */
[data-testid="stSidebar"] .stRadio > label {
    padding: 6px 10px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s ease;
}
[data-testid="stSidebar"] .stRadio > label:hover {
    background: #EFF2F7;
    color: #1A1F36;
}
[data-testid="stSidebar"] .stRadio > label:has(input:checked) {
    background: #E6F1FB;
    color: #185FA5;
    font-weight: 500;
    border-left: 3px solid #185FA5;
}

/* ── Sidebar button ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: #EFF2F7 !important;
    color: #1A1F36 !important;
    border: 0.5px solid #E5E7EB !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #E6F1FB !important;
}

/* ── Typography ──────────────────────────────────────────────────────────── */
h1, h2, h3 { color: #1A1F36 !important; font-weight: 500 !important; }
h1 { font-size: 18px !important; }
h2 { font-size: 14px !important; }
hr { border-color: #E5E7EB !important; margin: 0.75rem 0 !important; }

/* ── KPI Cards ─────────────────────────────────────────────────────────────── */
[data-testid="metric-container"] {
    background: #EFF2F7;
    border-radius: 8px;
    padding: 12px;
    border: 0.5px solid #E5E7EB;
}

/* KPI tint backgrounds */
.kpi-blue { background: #E6F1FB !important; }
.kpi-green { background: #EAF3DE !important; }
.kpi-amber { background: #FAEEDA !important; }

[data-testid="stMetricLabel"] p { 
    font-size: 12px !important; 
    font-weight: 400 !important; 
    color: #6B7280 !important; 
}
[data-testid="stMetricValue"] { 
    font-size: 24px !important; 
    font-weight: 500 !important; 
    color: #1A1F36 !important; 
}

.kpi-card {
    border-radius: 14px;
    border: 1px solid #E2E8F0;
    background: #FFFFFF;
    box-shadow: 0 8px 16px rgba(15, 23, 42, 0.06);
    padding: 0.85rem 0.9rem;
    min-height: 134px;
}
.kpi-tone-blue { border-top: 4px solid #3B82F6; }
.kpi-tone-green { border-top: 4px solid #10B981; }
.kpi-tone-amber { border-top: 4px solid #F59E0B; }
.kpi-head { display: flex; align-items: center; justify-content: space-between; gap: 0.45rem; }
.kpi-label { font-size: 0.74rem; color: #334155; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em; }
.kpi-pill {
    font-size: 0.65rem;
    border-radius: 999px;
    padding: 0.16rem 0.45rem;
    color: #334155;
    background: #E2E8F0;
    font-weight: 700;
}
.kpi-value { font-size: 1.65rem; font-weight: 800; color: #0F172A; line-height: 1.12; margin-top: 0.45rem; }
.kpi-sub { font-size: 0.75rem; color: #64748B; margin-top: 0.15rem; }
.kpi-delta {
    margin-top: 0.55rem;
    width: fit-content;
    border-radius: 999px;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.14rem 0.45rem;
}
.kpi-delta-up { background: #DCFCE7; color: #166534; }
.kpi-delta-down { background: #FEE2E2; color: #991B1B; }

/* ── Section heading ──────────────────────────────────────────────────────── */
.section-heading {
    font-size: 14px;
    font-weight: 500;
    color: #1A1F36;
    border-left: 3px solid #185FA5;
    padding-left: 8px;
    margin: 0.5rem 0 0.75rem 0;
}
.page-subtitle { font-size: 13px; color: #6B7280; margin: -0.5rem 0 1rem 0; }

/* ── Chart container ──────────────────────────────────────────────────────── */
.stPlotlyChart {
    background: #1F1D2E !important;
    border: 0.5px solid #393552;
    border-radius: 8px;
    padding: 14px !important;
}

/* ── Data tables ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 0.5px solid #E5E7EB;
    border-radius: 8px;
}

.dash-table-wrapper {
    border: 1px solid #D8E3F2;
    border-radius: 14px;
    overflow: auto;
    background: #FFFFFF;
    box-shadow: 0 10px 26px rgba(15, 23, 42, 0.06);
}

.dash-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 0.82rem;
}

.dash-table thead th {
    position: sticky;
    top: 0;
    z-index: 1;
    background: linear-gradient(180deg, #EAF2FF 0%, #E2ECFB 100%);
    color: #0F3B67;
    text-transform: uppercase;
    font-weight: 800;
    letter-spacing: 0.04em;
    padding: 0.62rem 0.56rem;
    border-bottom: 1px solid #CFE0F5;
    white-space: nowrap;
}

.dash-table tbody td {
    border-bottom: 1px solid #EDF2F7;
    padding: 0.56rem;
    color: #1E293B;
}

.dash-table tbody tr:nth-child(even) td { background: #FAFCFF; }
.dash-table tbody tr:hover td { background: #EEF6FF; }
.dash-table-total td {
    font-weight: 800;
    background: #E8F1FF !important;
    color: #0E4170;
}
.dash-table-red td { background: #FFF1F2 !important; }
.dash-table-amber td { background: #FFF8EC !important; }

.badge-yes,
.badge-no {
    display: inline-flex;
    align-items: center;
    border-radius: 999px;
    padding: 0.16rem 0.5rem;
    font-size: 0.72rem;
    font-weight: 700;
}
.badge-yes {
    color: #065F46;
    background: #D1FAE5;
}
.badge-no {
    color: #991B1B;
    background: #FEE2E2;
}

.enquiry-table thead th { font-size: 0.74rem; }
.enquiry-table tbody td { font-size: 0.74rem; }

/* ── Form elements ───────────────────────────────────────────────────────── */
.stSelectbox > div > div,
.stMultiselect > div > div {
    border-color: #E5E7EB !important;
}
.stTextInput input {
    border-color: #E5E7EB !important;
}

/* ── Buttons ──────────────────────────────────────────────────────────────── */
.stButton > button {
    border-radius: 8px !important;
}

/* ── Caption text ────────────────────────────────────────────────────────── */
.stCaption p,
[data-testid="stCaptionContainer"] p { 
    color: #9CA3AF !important; 
    font-size: 11px !important; 
}

/* ── Nav cards (home page) ───────────────────────────────────────────────── */
.nav-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 1rem; }
.nav-card {
    background: #FFFFFF;
    padding: 1.2rem 1.4rem;
    border: 0.5px solid #E5E7EB;
    border-left: 4px solid #185FA5;
    transition: all 0.18s ease;
    cursor: default;
}
.nav-card:hover { 
    box-shadow: 0 4px 18px rgba(24, 95, 165, 0.14); 
    border-left-color: #EF9F27; 
    transform: translateX(3px); 
}
.nav-card-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; }
.nav-card-icon   { font-size: 1.15rem; }
.nav-card-title  { font-size: 0.94rem; font-weight: 500; color: #185FA5; margin: 0; }
.nav-card-desc   { font-size: 0.82rem; color: #6B7280; line-height: 1.45; margin: 0; }
</style>
"""


def inject_login_css():
    """Inject login-page-only CSS (hides sidebar, split-column layout)."""
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)


# Login page CSS (split layout)
_LOGIN_CSS = """
<style>
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
    width: 0 !important;
}

.main { margin-left: 0 !important; }
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
    align-items: stretch !important;
}
[data-testid="stColumn"] { padding: 0 !important; }

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child > div > div {
    background: linear-gradient(150deg, #042C53 0%, #185FA5 52%, #2D5FA8 100%) !important;
    min-height: 100vh !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child > div:first-child {
    padding: 3rem 2.75rem !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > div > div {
    background: #EFF2F7 !important;
    min-height: 100vh !important;
}

[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"],
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"] > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"] > div > div {
    background: transparent !important;
    min-height: unset !important;
}

[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E5E7EB !important;
    border-radius: 8px !important;
    padding: 2rem 1.8rem 1.5rem !important;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08) !important;
    width: 100% !important;
}

.stFormSubmitButton > button {
    background: linear-gradient(90deg, #185FA5 0%, #2D5FA8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1.2px !important;
    padding: 0.75rem !important;
    width: 100% !important;
    text-transform: uppercase !important;
}
.stFormSubmitButton > button:hover { filter: brightness(0.97) !important; }

.stTextInput input {
    border-radius: 8px !important;
    border-color: #E5E7EB !important;
    background: #FAFBFC !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus {
    border-color: #185FA5 !important;
    box-shadow: 0 0 0 2px rgba(24, 95, 165, 0.10) !important;
}
label { font-size: 0.82rem !important; font-weight: 600 !important; color: #6B7280 !important; }

.login-brand-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-height: 100vh;
    padding: 3rem 2.75rem;
    box-sizing: border-box;
}
.login-brand-logo {
    height: 42px;
    object-fit: contain;
    filter: brightness(0) invert(1);
    opacity: 0.88;
    display: block;
    margin-bottom: 2.25rem;
}
.login-brand-heading {
    color: #FFFFFF !important;
    font-size: 2.4rem !important;
    font-weight: 800 !important;
    line-height: 1.18 !important;
    margin: 0 0 0.75rem !important;
    letter-spacing: -0.5px !important;
}
.login-brand-sub {
    color: rgba(255,255,255,0.52);
    font-size: 0.88rem;
    margin: 0;
    line-height: 1.5;
}
</style>
"""


def inject_global_css():
    """Inject app-wide CSS. Call after set_page_config() on every authenticated page."""
    st.markdown(_CSS, unsafe_allow_html=True)
