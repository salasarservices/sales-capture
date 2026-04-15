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
@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');

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

/* ── Sidebar — dark theme ────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.35) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 0 !important;
}

/* ── Hide Streamlit chrome inside sidebar ────────────────────────────────── */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] nav { display: none !important; }

/* ── Fix sidebar (hide collapse toggle) ─────────────────────────────────── */
[data-testid="collapsedControl"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ── Radio: off-screen but clickable via JS ──────────────────────────────── */
[data-testid="stSidebar"] .stRadio {
    position: absolute !important;
    left: -9999px !important;
    top: -9999px !important;
    opacity: 0 !important;
}

/* ── Sidebar logo ─────────────────────────────────────────────────────────── */
.sb-logo {
    text-align: center;
    padding: 28px 20px 22px;
}
.sb-logo img {
    height: 42px;
    filter: brightness(0) invert(1);
    opacity: 0.92;
}
.sb-divider {
    border: none;
    border-top: 1px solid rgba(255,255,255,0.08);
    margin: 0 0 8px 0;
}

/* ── Nav list ─────────────────────────────────────────────────────────────── */
.sb-nav-list { padding: 8px; }
.sb-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 11px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
    color: #94a3b8;
    font-size: 11px;
    font-weight: 700;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 2px;
    user-select: none;
    -webkit-user-select: none;
    text-decoration: none;
}
.sb-nav-item:hover { background: rgba(255,255,255,0.07); color: #e2e8f0; }
.sb-nav-item.active { background: #1e40af; color: #ffffff; }
.sb-nav-item.active:hover { background: #1d4ed8; }
.sb-nav-item .material-icons-round {
    font-size: 20px;
    flex-shrink: 0;
    line-height: 1;
}
.sb-nav-label { flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sb-pill {
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.2px;
    background: rgba(255,255,255,0.13);
    color: #cbd5e1;
    white-space: nowrap;
    flex-shrink: 0;
    text-transform: none;
}
.sb-nav-item.active .sb-pill { background: rgba(255,255,255,0.22); color: #dbeafe; }

/* ── Sidebar sign-out button ─────────────────────────────────────────────── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.14) !important;
    border-radius: 8px !important;
    color: rgba(255,255,255,0.55) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.1px !important;
    transition: all 0.2s ease !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255,255,255,0.07) !important;
    border-color: rgba(255,255,255,0.25) !important;
    color: rgba(255,255,255,0.85) !important;
}

/* ── Typography ──────────────────────────────────────────────────────────── */
h1, h2, h3 { color: #1A1F36 !important; font-weight: 500 !important; }
h1 { font-size: 18px !important; }
h2 { font-size: 14px !important; }
hr { border-color: #E5E7EB !important; margin: 0.75rem 0 !important; }

/* ── Section heading ──────────────────────────────────────────────────────── */
.section-heading {
    font-size: 13px;
    font-weight: 600;
    color: #1A1F36;
    border-left: 3px solid #185FA5;
    padding-left: 10px;
    margin: 0.75rem 0 0.6rem 0;
    display: block;
}
.page-subtitle { font-size: 13px; color: #6B7280; margin: -0.5rem 0 1rem 0; }

/* ══════════════════════════════════════════════════════════════════════════
   PRELINE-STYLE KPI STAT CARDS
══════════════════════════════════════════════════════════════════════════ */
.hs-kpi-grid {
    display: grid;
    gap: 12px;
    margin: 0.5rem 0 0.75rem;
}
.hs-kpi-grid-5 { grid-template-columns: repeat(5, 1fr); }
.hs-kpi-grid-3 { grid-template-columns: repeat(3, 1fr); }

.hs-kpi-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 16px 18px 14px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    position: relative;
    overflow: hidden;
}
.hs-kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 12px 12px 0 0;
}
.hs-kpi-blue::after  { background: #185FA5; }
.hs-kpi-green::after { background: #1D9E75; }
.hs-kpi-amber::after { background: #EF9F27; }

.hs-kpi-header {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    margin-bottom: 10px;
}
.hs-kpi-label {
    font-size: 10.5px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    font-weight: 700;
    color: #6b7280;
    line-height: 1.4;
    margin: 0;
}
.hs-kpi-icon {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 15px;
    flex-shrink: 0;
    line-height: 1;
}
.hs-kpi-icon-blue  { background: #E6F1FB; }
.hs-kpi-icon-green { background: #EAF3DE; }
.hs-kpi-icon-amber { background: #FAEEDA; }

.hs-kpi-value {
    font-size: 1.45rem;
    font-weight: 600;
    line-height: 1.1;
    margin: 0;
}
.hs-kpi-blue  .hs-kpi-value { color: #0C447C; }
.hs-kpi-green .hs-kpi-value { color: #27500A; }
.hs-kpi-amber .hs-kpi-value { color: #633806; }

/* ══════════════════════════════════════════════════════════════════════════
   PRELINE-STYLE DATA TABLES
══════════════════════════════════════════════════════════════════════════ */
.hs-table-wrap {
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    overflow: hidden;
    background: #ffffff;
}
.hs-table-scroll {
    overflow: auto;
}
.hs-table-scroll::-webkit-scrollbar { width: 5px; height: 5px; }
.hs-table-scroll::-webkit-scrollbar-track { background: #f9fafb; }
.hs-table-scroll::-webkit-scrollbar-thumb { background: #d1d5db; border-radius: 10px; }

.hs-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12.5px;
    background: #ffffff;
}
.hs-table thead {
    position: sticky;
    top: 0;
    z-index: 2;
}
.hs-table thead tr { background: #f9fafb; }
.hs-table thead th {
    padding: 10px 14px;
    text-align: left;
    font-size: 10.5px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6b7280;
    white-space: nowrap;
    border-bottom: 1.5px solid #e5e7eb;
}
.hs-table tbody tr {
    border-bottom: 1px solid #f3f4f6;
    transition: background 0.1s ease;
}
.hs-table tbody tr:last-child { border-bottom: none; }
.hs-table tbody tr:hover td { background: #f9fafb !important; }
.hs-table tbody td {
    padding: 9px 14px;
    color: #374151;
    white-space: nowrap;
}

/* Row state classes */
.hs-row-total td {
    background: #f1f5f9 !important;
    font-weight: 700;
    color: #1a1f36 !important;
    border-top: 1.5px solid #dde3ea !important;
}
.hs-row-red   td { background: #fff1f2 !important; color: #9b1c1c !important; }
.hs-row-amber td { background: #fffbeb !important; color: #92400e !important; }

/* Yes / No badges in enquiry table */
.badge-yes { color: #065f46; font-weight: 600; font-size: 11px; }
.badge-no  { color: #991b1b; font-weight: 600; font-size: 11px; }

/* ══════════════════════════════════════════════════════════════════════════
   PRELINE-STYLE DROP-OFF CARDS
══════════════════════════════════════════════════════════════════════════ */
.hs-dropoff-stack {
    display: flex;
    flex-direction: column;
    gap: 12px;
    margin-top: 6px;
}
.hs-dropoff-card {
    background: #ffffff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 14px 18px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    position: relative;
    overflow: hidden;
}
.hs-dropoff-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; bottom: 0;
    width: 4px;
    border-radius: 12px 0 0 12px;
}
.hs-dropoff-red::before   { background: #B91C1C; }
.hs-dropoff-amber::before { background: #D97706; }
.hs-dropoff-tag {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}
.hs-dropoff-red   .hs-dropoff-tag { color: #B91C1C; }
.hs-dropoff-amber .hs-dropoff-tag { color: #D97706; }
.hs-dropoff-value {
    font-size: 1.4rem;
    font-weight: 700;
    color: #1E293B;
    line-height: 1.1;
}
.hs-dropoff-pct {
    font-size: 0.88rem;
    margin-left: 4px;
}
.hs-dropoff-red   .hs-dropoff-pct { color: #B91C1C; }
.hs-dropoff-amber .hs-dropoff-pct { color: #D97706; }
.hs-dropoff-sub {
    font-size: 12px;
    color: #64748B;
    margin-top: 3px;
}

/* ── Chart container ──────────────────────────────────────────────────────── */
.stPlotlyChart {
    background: #FFFFFF !important;
    border: 0.5px solid #E5E7EB;
    border-radius: 8px;
    padding: 14px !important;
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