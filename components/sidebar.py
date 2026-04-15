"""
Sidebar component — dark admin-panel style with Material Icons Round.
Navigation uses a hidden Streamlit radio for state/routing, while users
interact with custom icon+label nav items.
"""

import streamlit as st


NAV_ITEMS = [
    {
        "key": "Business Conversion Ratio",
        "label": "Business Conversion",
        "icon": "query_stats",
    },
    {
        "key": "Sales Capture Summary",
        "label": "Sales Capture",
        "icon": "description",
    },
    {
        "key": "Conversion Ratio Summary",
        "label": "Conversion Ratio",
        "icon": "bar_chart",
    },
    {
        "key": "Master Data (From April 25 to March 26)",
        "label": "Master Data",
        "icon": "storage",
    },
]


_SIDEBAR_CSS = """
<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');

/* Hide Streamlit auto page-nav */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] nav {
    display: none !important;
}

/* ── Fixed, dark sidebar base ── */
[data-testid="stSidebar"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 17.5rem !important;
    min-width: 17.5rem !important;
    max-width: 17.5rem !important;
    height: 100vh !important;
    z-index: 100 !important;
    background: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35) !important;
}

/* Sidebar inner content scroll */
section[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 0 !important;
    height: 100vh !important;
    overflow-y: auto !important;
}

/* ── Shift main content so fixed sidebar does not overlap visuals ── */
[data-testid="stAppViewContainer"] section.main {
    margin-left: 17.5rem !important;
}
[data-testid="stAppViewContainer"] .main .block-container {
    max-width: 100% !important;
}

/* Logo */
.sb-logo {
    text-align: center;
    padding: 28px 20px 22px;
}
.sb-logo img {
    height: 42px;
    filter: brightness(0) invert(1);
    opacity: 0.92;
}

/* Divider */
.sb-divider {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin: 0 0 8px 0;
}

/* ── Sidebar radio nav restyle (icon + uppercase labels) ── */
[data-testid="stSidebar"] .stRadio {
    padding: 6px 8px 4px !important;
}
[data-testid="stSidebar"] .stRadio > div {
    gap: 6px !important;
}
[data-testid="stSidebar"] .stRadio label {
    margin: 0 !important;
    padding: 12px 14px !important;
    border-radius: 8px !important;
    color: #94a3b8 !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px !important;
    text-transform: uppercase !important;
    background: transparent !important;
    transition: background 0.15s ease, color 0.15s ease !important;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked) {
    background: #1e40af !important;
    color: #ffffff !important;
}
[data-testid="stSidebar"] .stRadio label:has(input:checked):hover {
    background: #1d4ed8 !important;
}
[data-testid="stSidebar"] .stRadio input[type="radio"] {
    display: none !important;
}

/* ── Sidebar section label (optional) ── */
.sb-section-label {
    padding: 14px 22px 6px;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: rgba(255, 255, 255, 0.28);
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* ── Bottom sign-out button ── */
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: 8px !important;
    color: rgba(255, 255, 255, 0.55) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.1px !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    gap: 8px !important;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    color: rgba(255, 255, 255, 0.85) !important;
}

[data-testid="stSidebar"] .stButton > button:active {
    background: rgba(255, 255, 255, 0.12) !important;
}
</style>
"""


def render_sidebar():
    """Render the dark admin-panel sidebar."""

    # Inject CSS in app DOM.
    st.markdown(_SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown(
            """
            <div class="sb-logo">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
            </div>
            <hr class="sb-divider">
            """,
            unsafe_allow_html=True,
        )

        # State init
        if "current_page" not in st.session_state:
            st.session_state.current_page = NAV_ITEMS[0]["key"]

        current_page = st.session_state.get("current_page", NAV_ITEMS[0]["key"])
        page_keys = [item["key"] for item in NAV_ITEMS]

        label_map = {
            "Business Conversion Ratio": "📈  BUSINESS CONVERSION",
            "Sales Capture Summary": "📄  SALES CAPTURE",
            "Conversion Ratio Summary": "📊  CONVERSION RATIO",
            "Master Data (From April 25 to March 26)": "🗃️  MASTER DATA",
        }

        # ── Clickable routing nav ─────────────────────────────────────────────
        selected = st.radio(
            "nav",
            page_keys,
            index=page_keys.index(current_page) if current_page in page_keys else 0,
            label_visibility="collapsed",
            format_func=lambda key: label_map.get(key, key.upper()),
            key="nav_radio",
        )

        if selected and selected != current_page:
            st.session_state.current_page = selected

        # ── Spacer + sign-out ─────────────────────────────────────────────────
        st.markdown('<div style="height:20px"></div>', unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            from utils.auth import logout
            logout()


def navigate_to_page(page_name: str):
    """Programmatically navigate to a page."""
    st.session_state.current_page = page_name
    st.rerun()


def get_current_page() -> str:
    """Return currently active page key."""
    return st.session_state.get("current_page", NAV_ITEMS[0]["key"])
