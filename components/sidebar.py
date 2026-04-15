"""
Sidebar component — dark admin-panel style with Material Icons Round.
Navigation via inline onclick handlers that click the hidden radio input,
so Streamlit's state management still drives page routing.
"""

import streamlit as st


NAV_ITEMS = [
    {
        "key": "Business Conversion Ratio",
        "label": "Business Conversion",
        "icon": "query_stats",
        "pill": None,
    },
    {
        "key": "Sales Capture Summary",
        "label": "Sales Capture",
        "icon": "description",
        "pill": None,
    },
    {
        "key": "Conversion Ratio Summary",
        "label": "Conversion Ratio",
        "icon": "bar_chart",
        "pill": None,
    },
    {
        "key": "Master Data (From April 25 to March 26)",
        "label": "Master Data",
        "icon": "storage",
        "pill": "Apr 25 – Mar 26",
    },
]


_SIDEBAR_CSS = """
<link href="https://fonts.googleapis.com/icon?family=Material+Icons+Round" rel="stylesheet">
<style>
/* ── Hide Streamlit's auto page-nav ── */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] nav {
    display: none !important;
}

/* ── Dark sidebar base ── */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid rgba(255, 255, 255, 0.07) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.35) !important;
}
[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
    padding-top: 0 !important;
}

/* ── Move radio off-screen; stays in DOM so .click() works ── */
[data-testid="stSidebar"] .stRadio {
    position: absolute !important;
    left: -9999px !important;
    top: -9999px !important;
}

/* ── Logo ── */
.sb-logo {
    text-align: center;
    padding: 28px 20px 22px;
}
.sb-logo img {
    height: 42px;
    filter: brightness(0) invert(1);
    opacity: 0.92;
}

/* ── Divider ── */
.sb-divider {
    border: none;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    margin: 0 0 8px 0;
}

/* ── Nav list ── */
.sb-nav-list {
    padding: 8px;
}

/* ── Nav item ── */
.sb-nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 8px;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
    color: #94a3b8;
    font-size: 13.5px;
    font-weight: 500;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    letter-spacing: 0.1px;
    margin-bottom: 2px;
    user-select: none;
    -webkit-user-select: none;
}
.sb-nav-item:hover {
    background: rgba(255, 255, 255, 0.07);
    color: #e2e8f0;
}
.sb-nav-item.active {
    background: #1e40af;
    color: #ffffff;
}
.sb-nav-item.active:hover {
    background: #1d4ed8;
}

/* ── Material icon inside nav item ── */
.sb-nav-item .material-icons-round {
    font-size: 20px;
    flex-shrink: 0;
    line-height: 1;
}

/* ── Nav label ── */
.sb-nav-label {
    flex: 1;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

/* ── Pill badge ── */
.sb-pill {
    display: inline-flex;
    align-items: center;
    padding: 2px 8px;
    border-radius: 20px;
    font-size: 10px;
    font-weight: 600;
    letter-spacing: 0.2px;
    background: rgba(255, 255, 255, 0.13);
    color: #cbd5e1;
    white-space: nowrap;
    flex-shrink: 0;
}
.sb-nav-item.active .sb-pill {
    background: rgba(255, 255, 255, 0.22);
    color: #dbeafe;
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

    # Inject CSS + Material Icons font (applied globally so font loads early)
    st.markdown(_SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown("""
            <div class="sb-logo">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
            </div>
            <hr class="sb-divider">
        """, unsafe_allow_html=True)

        # ── State init ────────────────────────────────────────────────────────
        if "current_page" not in st.session_state:
            st.session_state.current_page = NAV_ITEMS[0]["key"]

        current_page = st.session_state.get("current_page", NAV_ITEMS[0]["key"])
        page_keys = [item["key"] for item in NAV_ITEMS]

        # ── Hidden radio — off-screen but in DOM so JS .click() works ─────────
        selected = st.radio(
            "nav",
            page_keys,
            index=page_keys.index(current_page) if current_page in page_keys else 0,
            label_visibility="collapsed",
            key="nav_radio",
        )
        if selected and selected != current_page:
            st.session_state.current_page = selected

        # ── Visual nav items ──────────────────────────────────────────────────
        # onclick: clicks the matching hidden radio <input> so Streamlit reruns
        nav_html = '<div class="sb-nav-list">'
        for idx, item in enumerate(NAV_ITEMS):
            active_cls = "active" if item["key"] == current_page else ""
            pill_html = (
                f'<span class="sb-pill">{item["pill"]}</span>'
                if item.get("pill")
                else ""
            )
            # Single-quoted JS string avoids conflict with the outer double-quote attr
            js = (
                "var r=document.querySelectorAll("
                "'[data-testid=\"stSidebar\"] input[type=\"radio\"]');"
                f"if(r[{idx}])r[{idx}].click();"
            )
            nav_html += (
                f'<div class="sb-nav-item {active_cls}" onclick="{js}">'
                f'<span class="material-icons-round">{item["icon"]}</span>'
                f'<span class="sb-nav-label">{item["label"]}</span>'
                f"{pill_html}"
                f"</div>"
            )
        nav_html += "</div>"

        st.markdown(nav_html, unsafe_allow_html=True)

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
    """Return the currently active page key."""
    return st.session_state.get("current_page", NAV_ITEMS[0]["key"])
