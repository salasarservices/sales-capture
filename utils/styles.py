"""
Brand color palette and minimal Streamlit-internal CSS overrides.

Tailwind CSS is loaded globally via st_tailwind.initialize_tailwind() in app.py.
All custom component HTML (KPI cards, tables, sidebar cards, drop-off cards) uses
Tailwind utility classes directly.  This file only contains:

  1. COLORS / CHART  — brand palette constants (consumed by charts.py and pages)
  2. _STREAMLIT_OVERRIDES — a small <style> block for selectors Tailwind cannot
     reach ([data-testid="..."], pseudo-elements, ::webkit-scrollbar, child
     combinators like .tw-row-total td, etc.)
  3. _LOGIN_CSS — login-page overrides that target Streamlit form/input widgets
"""

import streamlit as st

# ── Brand Color Palette ──────────────────────────────────────────────────────
COLORS = {
    # Primary brand
    "navy":        "#042C53",
    "navy_med":    "#185FA5",
    "navy_lt":     "#E6F1FB",
    "navy_border": "#B5D4F4",
    "navy_text":   "#0C447C",
    "navy_sub":    "#378ADD",

    # Success / Growth
    "green":       "#1D9E75",
    "green_lt":    "#EAF3DE",
    "green_label": "#3B6D11",
    "green_value": "#27500A",

    # Revenue / Currency
    "amber":       "#EF9F27",
    "amber_lt":    "#FAEEDA",
    "amber_label": "#854F0B",
    "amber_value": "#633806",

    # Neutral surfaces
    "bg":      "#F8F9FA",
    "surface": "#EFF2F7",
    "card":    "#FFFFFF",
    "border":  "#E5E7EB",

    # Text
    "text":           "#1A1F36",
    "text_secondary":  "#6B7280",
    "text_tertiary":   "#9CA3AF",
    "negative":        "#A32D2D",
}

# Chart palette (consumed by components/charts.py)
CHART = {
    "fresh":   "#185FA5",
    "renewal": "#1D9E75",
    "expanded":"#EF9F27",
    "blue":    "#185FA5",
    "green":   "#1D9E75",
    "amber":   "#EF9F27",
}

# ─────────────────────────────────────────────────────────────────────────────
# MINIMAL STREAMLIT OVERRIDES
# Only patterns Tailwind utility classes genuinely cannot express:
#   • Streamlit internal [data-testid] / component selectors
#   • Pseudo-element ::before / ::after with dynamic content
#   • ::-webkit-scrollbar (browser vendor prefix)
#   • Child combinators (.tw-row-total td) for dynamic table-row states
#   • :hover on <td> inside arbitrary parent (too verbose in Tailwind)
# ─────────────────────────────────────────────────────────────────────────────
_STREAMLIT_OVERRIDES = """
<style>
/* ── Hide Streamlit chrome ─────────────────────────────────────────────────── */
#MainMenu, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] { display: none !important; }

/* ── Page background ───────────────────────────────────────────────────────── */
[data-testid="stAppViewContainer"] > section.main { background-color: #F8F9FA; }
.main .block-container { padding-top: 0.5rem; padding-bottom: 3rem; max-width: 100%; }

/* ── Plotly chart wrapper ──────────────────────────────────────────────────── */
.stPlotlyChart {
    background: #FFFFFF !important;
    border: 0.5px solid #E5E7EB;
    border-radius: 8px;
    padding: 14px !important;
}

/* ── Native st.dataframe ───────────────────────────────────────────────────── */
[data-testid="stDataFrame"] {
    border: 0.5px solid #E5E7EB;
    border-radius: 8px;
}

/* ── Form / select / multiselect border colour ─────────────────────────────── */
.stSelectbox > div > div,
.stMultiselect > div > div { border-color: #E5E7EB !important; }
.stTextInput input          { border-color: #E5E7EB !important; }
.stButton > button          { border-radius: 8px !important; }

/* ── Typography ────────────────────────────────────────────────────────────── */
h1, h2, h3 { color: #1A1F36 !important; font-weight: 500 !important; }
h1 { font-size: 18px !important; }
h2 { font-size: 14px !important; }
hr { border-color: #E5E7EB !important; margin: 0.75rem 0 !important; }

/* ── Caption ───────────────────────────────────────────────────────────────── */
.stCaption p,
[data-testid="stCaptionContainer"] p {
    color: #9CA3AF !important;
    font-size: 11px !important;
}

/* ── Custom scrollbar (vendor-prefixed — not expressible in Tailwind) ──────── */
.tw-scroll::-webkit-scrollbar        { width: 5px; height: 5px; }
.tw-scroll::-webkit-scrollbar-track  { background: #f9fafb; }
.tw-scroll::-webkit-scrollbar-thumb  { background: #d1d5db; border-radius: 10px; }

/* ── Table row states (child combinator — Tailwind would require [&>td] JIT) ─ */
.tw-row-total td {
    background: #f1f5f9 !important;
    font-weight: 700;
    color: #1a1f36 !important;
    border-top: 1.5px solid #dde3ea !important;
}
.tw-row-red   td { background: #fff1f2 !important; color: #9b1c1c !important; }
.tw-row-amber td { background: #fffbeb !important; color: #92400e !important; }

/* ── Yes / No badges (reused across table cells) ───────────────────────────── */
.tw-badge-yes { color: #065f46; font-weight: 600; font-size: 11px; }
.tw-badge-no  { color: #991b1b; font-weight: 600; font-size: 11px; }
</style>
"""

# ─────────────────────────────────────────────────────────────────────────────
# LOGIN PAGE OVERRIDES
# Targets Streamlit form / input / submit-button internals.
# The gradient background (.stApp) and glassmorphism card ([data-testid="stForm"])
# cannot be achieved with Tailwind utility classes alone.
# ─────────────────────────────────────────────────────────────────────────────
_LOGIN_CSS = """
<style>
/* ── Hide sidebar on login ──────────────────────────────────────────────────── */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ── Full-screen gradient background ────────────────────────────────────────── */
.stApp {
    background: linear-gradient(135deg,
        #5CC8BE 0%,
        #6BAABF 25%,
        #8A9EBB 50%,
        #A89080 75%,
        #C8956A 100%) !important;
}

.main .block-container {
    padding-top: 8vh !important;
    padding-bottom: 4vh !important;
    max-width: 100% !important;
}

/* ── Glassmorphism card (the Streamlit <form> element) ──────────────────────── */
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.14) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 20px !important;
    padding: 44px 40px 36px !important;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.22) !important;
}
[data-testid="stForm"] label { display: none !important; }
[data-testid="stForm"] .stTextInput { margin-bottom: 12px; }

/* ── Input fields ────────────────────────────────────────────────────────────── */
[data-testid="stForm"] .stTextInput > div > div > input {
    background: rgba(240, 244, 248, 0.92) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 10px !important;
    color: #1A1F36 !important;
    padding: 14px 16px !important;
    font-size: 14px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}
[data-testid="stForm"] .stTextInput > div > div > input::placeholder {
    color: #9AA3AF !important;
}
[data-testid="stForm"] .stTextInput > div > div > input:focus {
    border-color: rgba(255, 255, 255, 0.7) !important;
    background: rgba(255, 255, 255, 0.98) !important;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2) !important;
}

/* ── Sign In button ──────────────────────────────────────────────────────────── */
[data-testid="stFormSubmitButton"] > button {
    background: #2C3344 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 15px !important;
    width: 100% !important;
    margin-top: 6px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    letter-spacing: 0.3px;
    transition: all 0.25s ease;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: #1E2535 !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.3);
}
</style>
"""


def inject_global_css() -> None:
    """Inject minimal Streamlit-internal CSS overrides.

    Tailwind CSS is loaded globally via tw.initialize_tailwind() in app.py.
    This only covers selectors Tailwind cannot reach.
    """
    st.markdown(_STREAMLIT_OVERRIDES, unsafe_allow_html=True)


def inject_login_css() -> None:
    """Inject login-page-only CSS (gradient bg, glassmorphism form, input styles)."""
    st.markdown(_LOGIN_CSS, unsafe_allow_html=True)
