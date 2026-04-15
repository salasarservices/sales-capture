"""Sidebar component — dark admin-panel style with Streamlit buttons for nav."""

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
:root {
    --app-sidebar-width: 21rem;
    --app-sidebar-gap: 0.85rem;
}

/* Never show Streamlit's sidebar collapse controls */
[data-testid="stSidebarCollapsedControl"],
button[kind="header"][aria-label*="sidebar" i] {
    display: none !important;
}

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
    width: var(--app-sidebar-width) !important;
    min-width: var(--app-sidebar-width) !important;
    max-width: var(--app-sidebar-width) !important;
    height: 100vh !important;
    z-index: 999 !important;
    background: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35) !important;
}

/* Keep dashboard content from sliding under fixed sidebar */
[data-testid="stAppViewContainer"] > section.main {
    margin-left: calc(var(--app-sidebar-width) + var(--app-sidebar-gap)) !important;
    width: calc(100% - var(--app-sidebar-width) - var(--app-sidebar-gap)) !important;
    max-width: calc(100% - var(--app-sidebar-width) - var(--app-sidebar-gap)) !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
}

/* Ensure Streamlit inner container also respects fixed sidebar width */
[data-testid="stAppViewContainer"] > section.main .block-container {
    max-width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1.25rem !important;
}

/* Responsive behavior: keep fixed sidebar, only tighten width/offset on smaller screens */
@media (max-width: 1200px) {
    :root {
        --app-sidebar-width: 18rem;
    }
}

@media (max-width: 992px) {
    :root {
        --app-sidebar-width: 16rem;
    }

    [data-testid="stAppViewContainer"] > section.main .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
    }
}

/* Sidebar inner content scroll */
section[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 0 !important;
    height: 100vh !important;
    overflow-y: auto !important;
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

/* Sidebar nav buttons (first four st.button widgets in sidebar) */
[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(-n+4) > button {
    width: 100% !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    background: transparent !important;
    color: #94a3b8 !important;
    text-transform: uppercase !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 0.6px !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 0.75rem 0.875rem !important;
    margin-bottom: 0.25rem !important;
    transition: background 0.15s ease, color 0.15s ease !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(-n+4) > button:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    color: #e2e8f0 !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(-n+4) > button[kind="primary"] {
    background: #1e40af !important;
    color: #ffffff !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(-n+4) > button[kind="primary"]:hover {
    background: #1d4ed8 !important;
}

/* Bottom sign-out button */
[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(5) > button {
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
    width: 100% !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(5) > button:hover {
    background: rgba(255, 255, 255, 0.07) !important;
    border-color: rgba(255, 255, 255, 0.25) !important;
    color: rgba(255, 255, 255, 0.85) !important;
}

[data-testid="stSidebar"] div[data-testid="stButton"]:nth-of-type(5) > button:active {
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

        for item in NAV_ITEMS:
            button_type = "primary" if item["key"] == current_page else "secondary"
            if st.button(
                f"{item['label']}",
                type=button_type,
                use_container_width=True,
                key=f"nav_{item['key']}",
            ):
                navigate_to_page(item["key"])

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
