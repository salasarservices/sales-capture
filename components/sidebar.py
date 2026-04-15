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

_SIDEBAR_STYLES = """
<style>
@import url('https://fonts.googleapis.com/icon?family=Material+Icons+Round');

/* Hide Streamlit auto page-nav */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] nav {
    display: none !important;
}

/* Fixed sidebar */
section[data-testid="stSidebar"] {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    height: 100vh !important;
    z-index: 999 !important;
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

/* Keep hidden radio in DOM, but invisible */
[data-testid="stSidebar"] div[data-testid="stRadio"],
[data-testid="stSidebar"] .stRadio {
    position: absolute !important;
    left: -9999px !important;
    top: -9999px !important;
    width: 1px !important;
    height: 1px !important;
    opacity: 0 !important;
    pointer-events: none !important;
    overflow: hidden !important;
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

/* Nav list */
.sb-nav-list {
    padding: 8px;
}

/* Nav item */
.sb-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
    color: #94a3b8;
    font-size: 13px;
    font-weight: 700;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0.6px;
    text-transform: uppercase;
    margin-bottom: 4px;
    user-select: none;
    -webkit-user-select: none;
}

.sb-nav-item:hover {
    background: rgba(255, 255, 255, 0.07);
    color: #e2e8f0;
}

.sb-nav-item.active {
    background: #c1f99e;
    color: #ffffff;
}

.sb-nav-item.active:hover {
    background: #1d4ed8;
}

/* Material icon */
.sb-nav-item .material-icons-round {
    font-size: 20px;
    flex-shrink: 0;
    line-height: 1;
}

/* Label */
.sb-nav-label {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* Bottom sign-out button */
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
    """Render fixed dark sidebar with custom nav."""
    # Use markdown HTML injection so styles apply to main app DOM (not iframe)
    st.markdown(_SIDEBAR_STYLES, unsafe_allow_html=True)

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

        # Hidden radio for Streamlit-native state/rerun behavior
        selected = st.radio(
            "nav",
            page_keys,
            index=page_keys.index(current_page) if current_page in page_keys else 0,
            label_visibility="collapsed",
            key="nav_radio",
        )

        if selected and selected != current_page:
            st.session_state.current_page = selected

        # Visual nav items
        nav_html = '<div class="sb-nav-list">'
        for idx, item in enumerate(NAV_ITEMS):
            active_cls = "active" if item["key"] == current_page else ""

            js = (
                "var r=document.querySelectorAll("
                "'[data-testid=\"stSidebar\"] input[type=\"radio\"]');"
                f"if(r[{idx}])r[{idx}].click();"
            )

            nav_html += (
                f'<div class="sb-nav-item {active_cls}" onclick="{js}">'
                f'<span class="material-icons-round">{item["icon"]}</span>'
                f'<span class="sb-nav-label">{item["label"]}</span>'
                "</div>"
            )

        nav_html += "</div>"
        st.markdown(nav_html, unsafe_allow_html=True)

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
