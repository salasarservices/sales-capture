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
_CSS = ""  # All custom CSS removed — pure native Streamlit UI


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
    """No-op: all custom CSS removed in favour of native Streamlit UI."""
    pass