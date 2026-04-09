"""
Global CSS injection and brand color constants for Salasar Sales Dashboard.
  · inject_login_css()   — call in login_form() only (hides sidebar, split layout)
  · inject_global_css()  — call on every authenticated page
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
}

# Chart palette (used by components/charts.py)
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

# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN-PAGE CSS  (injected only on the unauthenticated login screen)
# ─────────────────────────────────────────────────────────────────────────────
_LOGIN_CSS = """
<style>
/* ── chrome off ── */
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── hide sidebar ── */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] {
    display: none !important;
    width: 0 !important;
}

/* ── full-width, no padding ── */
.main { margin-left: 0 !important; }
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
    margin: 0 !important;
}

/* ── zero gap between the two split columns ── */
[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
    padding: 0 !important;
    align-items: stretch !important;
}
[data-testid="stColumn"] { padding: 0 !important; }

/* ── LEFT column: navy gradient brand panel ──
   Multi-selector covers all Streamlit DOM depths (div:first-child, div > div, etc.)
   so the background applies regardless of Streamlit Cloud version. */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child > div > div {
    background: linear-gradient(150deg, #0C1E3D 0%, #1B3A6B 52%, #1F4F8A 100%) !important;
    min-height: 100vh !important;
}
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:first-child > div:first-child {
    padding: 3rem 2.75rem !important;
}

/* ── RIGHT column: light gray form panel ── */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child > div > div {
    background: #EEF2F7 !important;
    min-height: 100vh !important;
}

/* Nested inner columns (form centering) must NOT inherit the bg */
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"],
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"] > div,
[data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:last-child
  [data-testid="stHorizontalBlock"] [data-testid="stColumn"] > div > div {
    background: transparent !important;
    min-height: unset !important;
}

/* ── Login form card ── */
[data-testid="stForm"] {
    background: #FFFFFF !important;
    border: 1px solid #E2E8F0 !important;
    border-radius: 0 !important;
    padding: 2rem 1.8rem 1.5rem !important;
    box-shadow: 0 10px 28px rgba(15, 23, 42, 0.08) !important;
    width: 100% !important;
}

/* ── Submit button ── */
.stFormSubmitButton > button {
    background: linear-gradient(90deg, #356CF3 0%, #5B87F8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 1.2px !important;
    padding: 0.75rem !important;
    transition: background 0.18s !important;
    width: 100% !important;
    text-transform: uppercase !important;
}
.stFormSubmitButton > button:hover { filter: brightness(0.97) !important; }

/* ── Inputs ── */
.stTextInput input {
    border-radius: 0 !important;
    border-color: #C8D3E2 !important;
    background: #FAFBFC !important;
    font-size: 0.9rem !important;
}
.stTextInput input:focus {
    border-color: #1B3A6B !important;
    box-shadow: 0 0 0 2px rgba(27,58,107,0.10) !important;
}
label { font-size: 0.82rem !important; font-weight: 600 !important; color: #475569 !important; }

/* ── LEFT brand card — vertically centered, no excess height ── */
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

# ─────────────────────────────────────────────────────────────────────────────
#  MAIN APP CSS  (injected on every authenticated page)
# ─────────────────────────────────────────────────────────────────────────────
_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   SALASAR SERVICES — SALES DASHBOARD
   Brand: Navy #1B3A6B · Gold #C8860A · BG #F0F4F8
═══════════════════════════════════════════════════════════════════════════ */

/* ── Chrome off ──────────────────────────────────────────────────────────── */
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Page background ─────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] > section.main { background-color: #F0F4F8; }
.main .block-container { padding-top: 1.5rem; padding-bottom: 3rem; max-width: 100%; }

/* ── REMOVE ROUNDED CORNERS (flat/Material style) ─────────────────────────── */
.stPlotlyChart,
[data-testid="stDataFrame"],
[data-testid="stExpander"],
[data-testid="stMetric"],
[data-testid="stForm"],
.stFormSubmitButton > button,
.stButton > button,
[data-testid="stDownloadButton"] > button,
.stTextInput input,
[data-baseweb="input"] > div,
[data-baseweb="select"] > div:first-child,
[data-baseweb="tag"],
[data-testid="stAlert"] {
    border-radius: 0 !important;
}

/* ── Sidebar ─────────────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #0F2547 0%, #1B3A6B 55%, #1E4080 100%) !important;
    border-right: none !important;
    box-shadow: 2px 0 14px rgba(0,0,0,0.18) !important;
}
[data-testid="stSidebar"] > div:first-child { background: transparent !important; }
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] small { color: rgba(255,255,255,0.68) !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #FFFFFF !important; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.10) !important; }

/* Sidebar nav links */
[data-testid="stSidebarNavLink"] {
    border-radius: 0 !important;
    margin: 1px 0 !important;
    border-left: 3px solid transparent !important;
    transition: all 0.13s ease !important;
}
[data-testid="stSidebarNavLink"]:hover { background: rgba(255,255,255,0.07) !important; }
[data-testid="stSidebarNavLink"][aria-selected="true"] {
    background: rgba(200,134,10,0.20) !important;
    border-left-color: #C8860A !important;
}
[data-testid="stSidebarNavLink"] span,
[data-testid="stSidebarNavLink"] p { color: rgba(255,255,255,0.85) !important; font-weight: 500 !important; }
[data-testid="stSidebarNavLink"][aria-selected="true"] span,
[data-testid="stSidebarNavLink"][aria-selected="true"] p { color: #FFFFFF !important; font-weight: 600 !important; }

/* Sidebar sign-out button */
[data-testid="stSidebar"] .stButton > button {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.80) !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 0 !important;
    font-size: 0.84rem !important;
    font-weight: 500 !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.13) !important;
    color: #FFFFFF !important;
}

/* ── Typography ──────────────────────────────────────────────────────────── */
h1 { color: #1B3A6B !important; font-weight: 700 !important; letter-spacing: -0.4px !important; font-size: 1.6rem !important; }
h2 { color: #1E293B !important; font-weight: 600 !important; font-size: 1.2rem !important; }
h3 { color: #1E293B !important; font-weight: 600 !important; font-size: 1.05rem !important; }
hr { border-color: #E2E8F0 !important; margin: 0.75rem 0 !important; }

/* ── KPI Cards — Material Django style (solid colour block + content) ─────── */
.kpi-card {
    background: #FFFFFF;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    display: flex;
    align-items: stretch;
    min-height: 88px;
    overflow: hidden;
    border: none;
}
.kpi-icon-block {
    width: 76px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.85rem;
    flex-shrink: 0;
}
.kpi-card.navy   .kpi-icon-block { background: #1B3A6B; }
.kpi-card.gold   .kpi-icon-block { background: #C8860A; }
.kpi-card.green  .kpi-icon-block { background: #15803D; }
.kpi-card.blue   .kpi-icon-block { background: #2563EB; }
.kpi-card.purple .kpi-icon-block { background: #7C3AED; }
.kpi-card.teal   .kpi-icon-block { background: #0D9488; }
.kpi-card.red    .kpi-icon-block { background: #B91C1C; }

.kpi-content {
    padding: 0.85rem 1rem;
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    min-width: 0;
}
.kpi-label {
    font-size: 0.67rem;
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
    font-size: 1.4rem;
    font-weight: 700;
    color: #1E293B;
    line-height: 1.1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Welcome banner ──────────────────────────────────────────────────────── */
.welcome-banner {
    background: linear-gradient(135deg, #1B3A6B 0%, #2D5FA8 100%);
    padding: 1.4rem 2rem;
    color: white;
    margin-bottom: 1.25rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 1rem;
}
.welcome-banner h2  { color: #FFFFFF !important; font-size: 1.25rem !important; margin: 0 0 0.2rem !important; font-weight: 700 !important; }
.welcome-banner p   { color: rgba(255,255,255,0.70); margin: 0; font-size: 0.87rem; }
.welcome-badge {
    background: rgba(255,255,255,0.14);
    border: 1px solid rgba(255,255,255,0.22);
    padding: 0.28rem 0.85rem;
    font-size: 0.80rem;
    font-weight: 600;
    color: rgba(255,255,255,0.95);
    white-space: nowrap;
}

/* ── Nav cards (home page) ───────────────────────────────────────────────── */
.nav-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem; margin-top: 1rem; }
.nav-card {
    background: #FFFFFF;
    padding: 1.2rem 1.4rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.07);
    border-left: 4px solid #1B3A6B;
    transition: all 0.18s ease;
    cursor: default;
}
.nav-card:hover { box-shadow: 0 4px 18px rgba(27,58,107,0.14); border-left-color: #C8860A; transform: translateX(3px); }
.nav-card-header { display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.35rem; }
.nav-card-icon   { font-size: 1.15rem; }
.nav-card-title  { font-size: 0.94rem; font-weight: 600; color: #1B3A6B; margin: 0; }
.nav-card-desc   { font-size: 0.82rem; color: #64748B; line-height: 1.45; margin: 0; }

/* ── Section heading ─────────────────────────────────────────────────────── */
.section-heading {
    font-size: 0.95rem;
    font-weight: 600;
    color: #1E293B;
    border-left: 3px solid #C8860A;
    padding-left: 0.65rem;
    margin: 0.5rem 0 0.75rem 0;
    line-height: 1.3;
}
.page-subtitle { font-size: 0.84rem; color: #64748B; margin: -0.55rem 0 1rem 0; }

/* ── HTML Dashboard Tables ───────────────────────────────────────────────── */
.dash-table-wrapper {
    overflow-y: auto;
    overflow-x: hidden;
    margin-bottom: 1rem;
    border: 1px solid #DDE3EC;
}
.dash-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 0.80rem;
    table-layout: fixed;
}
.dash-table thead th {
    background: #1B3A6B;
    color: #FFFFFF;
    font-weight: 700;
    text-transform: uppercase;
    font-size: 0.67rem;
    letter-spacing: 0.5px;
    padding: 0.6rem 0.75rem;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    position: sticky;
    top: 0;
    z-index: 10;
    border-right: 1px solid rgba(255,255,255,0.10);
}
.dash-table tbody tr { border-bottom: 1px solid #F1F5F9; }
.dash-table tbody tr:nth-child(even) td { background: #F8FAFC; }
.dash-table tbody tr:hover td { background: #EEF2FB !important; }
.dash-table tbody td {
    padding: 0.48rem 0.75rem;
    color: #1E293B;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    border-right: 1px solid #F1F5F9;
}
.dash-table-total td {
    background: #E8EFFA !important;
    font-weight: 700 !important;
    color: #1B3A6B !important;
    border-top: 2px solid #C8860A !important;
}
.dash-table-red   td { background: #FEF2F2 !important; }
.dash-table-amber td { background: #FFFBEB !important; }

/* Enquiry table — smaller font for dense layout */
.dash-table.enquiry-table { font-size: 0.75rem; }
.dash-table.enquiry-table thead th { font-size: 0.63rem; padding: 0.5rem 0.5rem; }
.dash-table.enquiry-table tbody td  { padding: 0.42rem 0.5rem; }
.badge-yes { color: #15803D; font-weight: 700; }
.badge-no  { color: #B91C1C; font-weight: 700; }

/* ── Plotly chart card ───────────────────────────────────────────────────── */
.stPlotlyChart {
    background: #FFFFFF !important;
    box-shadow: 0 1px 6px rgba(0,0,0,0.07) !important;
    padding: 0.25rem !important;
    border: 1px solid #E8EDF4 !important;
}

/* ── Native st.metric ────────────────────────────────────────────────────── */
[data-testid="stMetric"] {
    background: #FFFFFF !important;
    padding: 1rem 1.2rem !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #E8EDF4 !important;
}
[data-testid="stMetricLabel"] p { font-size: 0.70rem !important; font-weight: 700 !important; color: #94A3B8 !important; text-transform: uppercase !important; letter-spacing: 0.5px !important; }
[data-testid="stMetricValue"]   { font-size: 1.45rem !important; font-weight: 700 !important; color: #1E293B !important; }

/* ── Filter expander ─────────────────────────────────────────────────────── */
[data-testid="stExpander"] {
    background: #FFFFFF !important;
    border: 1px solid #DDE3EC !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04) !important;
    margin-bottom: 1rem !important;
}
[data-testid="stExpander"] summary { font-weight: 600 !important; color: #1B3A6B !important; }

/* ── DataFrame ───────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    border: 1px solid #DDE3EC !important;
}

/* ── Multiselect tags ────────────────────────────────────────────────────── */
[data-baseweb="tag"] { background-color: #EEF2FB !important; color: #1B3A6B !important; border: none !important; }

/* ── Download button ─────────────────────────────────────────────────────── */
[data-testid="stDownloadButton"] > button {
    background: #F0FDF4 !important;
    color: #15803D !important;
    border: 1px solid #86EFAC !important;
    font-weight: 600 !important;
}
[data-testid="stDownloadButton"] > button:hover { background: #DCFCE7 !important; }

/* ── Form submit (main pages) ────────────────────────────────────────────── */
.stFormSubmitButton > button {
    background: linear-gradient(135deg, #1B3A6B 0%, #2D5FA8 100%) !important;
    color: #FFFFFF !important;
    border: none !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.5px !important;
}
.stFormSubmitButton > button:hover { box-shadow: 0 4px 16px rgba(27,58,107,0.35) !important; }

/* ── Text inputs (main pages) ────────────────────────────────────────────── */
.stTextInput input { border-color: #C8D3E2 !important; }
.stTextInput input:focus { border-color: #1B3A6B !important; box-shadow: 0 0 0 2px rgba(27,58,107,0.10) !important; }

/* ── Captions ────────────────────────────────────────────────────────────── */
.stCaption p,
[data-testid="stCaptionContainer"] p { color: #94A3B8 !important; font-size: 0.79rem !important; }
</style>
"""


def inject_login_css():
    """Inject login-page-only CSS (hides sidebar, split-column layout)."""
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)


def inject_global_css():
    """Inject app-wide CSS. Call after set_page_config() on every authenticated page."""
    st.markdown(_CSS, unsafe_allow_html=True)
