"""
Sidebar component — dark admin-panel style with Material Icons Round.

All CSS (Material Icons font, dark theme, nav styles, fixed sidebar) is
injected via inject_global_css() in utils/styles.py, which is the only
reliable injection point in this Streamlit app.

Navigation works via inline onclick handlers that programmatically click
the hidden radio <input>, triggering a Streamlit rerun and page switch.
"""

import streamlit as st


NAV_ITEMS = [
    {
        "key": "Business Conversion Ratio",
        "label": "Business Conversion Ratio",
        "icon": "query_stats",
        "pill": None,
    },
    {
        "key": "Sales Capture Summary",
        "label": "Sales Capture Summary",
        "icon": "description",
        "pill": None,
    },
    {
        "key": "Conversion Ratio Summary",
        "label": "Conversion Ratio Summary",
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


def render_sidebar():
    """Render the dark admin-panel sidebar.

    CSS is NOT injected here — it lives in utils/styles.py::inject_global_css()
    which is called first in app.py and is the proven injection path.
    """
    with st.sidebar:
        # ── Logo ──────────────────────────────────────────────────────────────
        st.markdown(
            '<div class="sb-logo">'
            '<img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">'
            '</div>'
            '<hr class="sb-divider">',
            unsafe_allow_html=True,
        )

        # ── State ──────────────────────────────────────────────────────────────
        if "current_page" not in st.session_state:
            st.session_state.current_page = NAV_ITEMS[0]["key"]

        current_page = st.session_state.get("current_page", NAV_ITEMS[0]["key"])
        page_keys = [item["key"] for item in NAV_ITEMS]

        # ── Hidden radio — stays in DOM (off-screen via CSS) so JS .click() works
        selected = st.radio(
            "nav",
            page_keys,
            index=page_keys.index(current_page) if current_page in page_keys else 0,
            label_visibility="collapsed",
            key="nav_radio",
        )
        if selected and selected != current_page:
            st.session_state.current_page = selected

        # ── Nav items (visual) — onclick clicks the matching hidden radio input ─
        nav_html = '<div class="sb-nav-list">'
        for idx, item in enumerate(NAV_ITEMS):
            active_cls = "active" if item["key"] == current_page else ""
            pill_html = (
                f'<span class="sb-pill">{item["pill"]}</span>'
                if item.get("pill")
                else ""
            )
            # Inline JS: find all radio inputs inside sidebar, click index idx
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
