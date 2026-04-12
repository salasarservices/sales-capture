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
/* ═══════════════════════════════════════════════════════════════════════════
   SALASAR SERVICES — SALES DASHBOARD
   UI Design: Metric-First Layout with Sidebar Filters
═══════════════════════════════════════════════════════════════════════════ */

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
    background: transparent !important;
    border: 0 !important;
    padding: 0 !important;
}

/* ── Data tables ──────────────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 0.5px solid #E5E7EB;
    border-radius: 8px;
}

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
    border-left-color: #185FA5;
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
    padding: 2.8rem 1rem 1rem !important;
    max-width: 100% !important;
    margin: 0 !important;
    position: relative;
    z-index: 2;
}

.login-page-bg {
    position: fixed;
    inset: 0;
    z-index: 0;
    background:
        radial-gradient(circle at 15% 20%, rgba(89, 214, 210, 0.38), transparent 32%),
        radial-gradient(circle at 75% 15%, rgba(114, 187, 239, 0.35), transparent 30%),
        linear-gradient(125deg, #34658e 0%, #6ea0c3 55%, #b2947f 100%);
    filter: saturate(112%);
}

.login-orb {
    position: fixed;
    border-radius: 50%;
    filter: blur(2px);
    z-index: 1;
    pointer-events: none;
}
.orb-one {
    width: 320px;
    height: 320px;
    left: 12%;
    top: 17%;
    background: rgba(67, 201, 211, 0.26);
}
.orb-two {
    width: 290px;
    height: 290px;
    right: 16%;
    bottom: 15%;
    background: rgba(156, 212, 255, 0.24);
}

[data-testid="stHorizontalBlock"] {
    align-items: flex-start !important;
    position: relative;
    z-index: 3;
}

[data-testid="stColumn"] { padding: 0 !important; }

[data-testid="stForm"] {
    background: rgba(201, 224, 240, 0.26) !important;
    border: 1px solid rgba(255, 255, 255, 0.26) !important;
    border-radius: 0 !important;
    padding: 0 1.35rem 1.35rem !important;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.14) !important;
    backdrop-filter: blur(9px);
    -webkit-backdrop-filter: blur(9px);
}

.stFormSubmitButton > button {
    background: #2f3d54 !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    border-radius: 0 !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.2px !important;
    padding: 0.64rem !important;
    width: 100% !important;
}
.stFormSubmitButton > button:hover { filter: brightness(1.06) !important; }

.stTextInput input {
    border-radius: 0 !important;
    border-color: rgba(255, 255, 255, 0.24) !important;
    background: rgba(238, 246, 252, 0.82) !important;
    font-size: 0.9rem !important;
    color: #1F2937 !important;
}
.stTextInput input:focus {
    border-color: rgba(94, 152, 201, 0.8) !important;
    box-shadow: 0 0 0 1px rgba(94, 152, 201, 0.35) !important;
}
label { font-size: 0.8rem !important; font-weight: 600 !important; color: #EBF2FA !important; }

.glass-login-card {
    margin: 0 auto;
    width: 100%;
    min-width: 320px;
    max-width: 390px;
    padding: 2rem 1.35rem 1rem;
    background: rgba(201, 224, 240, 0.26);
    border: 1px solid rgba(255, 255, 255, 0.26);
    border-bottom: 0;
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.14);
    backdrop-filter: blur(9px);
    -webkit-backdrop-filter: blur(9px);
}
.glass-login-logo {
    height: 56px;
    object-fit: contain;
    filter: brightness(0) invert(1) drop-shadow(0 2px 6px rgba(0,0,0,0.2));
    display: block;
    margin: 0 auto 1.6rem;
}
.glass-login-title {
    text-align: center;
    color: #F8FAFC !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    margin: 0 0 0.35rem !important;
}
.glass-login-subtitle {
    text-align: center;
    color: rgba(238, 248, 255, 0.87);
    font-size: 0.95rem;
    margin: 0 0 0.4rem;
}
.login-footnote {
    text-align: center;
    color: rgba(237, 248, 255, 0.82);
    font-size: 0.74rem;
    margin-top: 0.85rem;
}
</style>
"""


def inject_global_css():
    """Inject app-wide CSS. Call after set_page_config() on every authenticated page."""
    st.markdown(_CSS, unsafe_allow_html=True)
