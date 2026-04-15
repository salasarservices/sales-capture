"""
Sidebar — pure native Streamlit, zero custom CSS.
"""

import streamlit as st

NAV_ITEMS = [
    ("Business Conversion Ratio",               "📅 Business Conversion"),
    ("Sales Capture Summary",                   "📈 Sales Capture"),
    ("Conversion Ratio Summary",                "📊 Conversion Ratio"),
    ("Master Data (From April 25 to March 26)", "📋 Master Data"),
]


def render_sidebar():
    """Render the sidebar using only native Streamlit widgets."""
    # Hide auto-generated multipage nav and the collapse/expand toggle
    # so the sidebar is always visible and can never be accidentally hidden.
    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"]             { display: none !important; }
        [data-testid="stSidebarCollapseButton"]  { display: none !important; }
        [data-testid="stSidebarCollapsedControl"]{ display: none !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.sidebar:
        st.image(
            "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png",
            use_container_width=True,
        )
        st.markdown(
            "<div style='text-align:center; line-height:1.5;'>"
            "<span style='font-size:15px;'>Sales capture report</span><br>"
            "<span style='font-size:15px;'>Ahmedabad</span>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.divider()

        if "current_page" not in st.session_state:
            st.session_state.current_page = NAV_ITEMS[0][0]

        page_keys   = [key   for key, _     in NAV_ITEMS]
        page_labels = [label for _,   label in NAV_ITEMS]
        current     = st.session_state.get("current_page", page_keys[0])
        idx         = page_keys.index(current) if current in page_keys else 0

        selected_label = st.radio(
            "Navigation",
            page_labels,
            index=idx,
            label_visibility="collapsed",
        )

        for key, label in NAV_ITEMS:
            if label == selected_label:
                st.session_state.current_page = key
                break

        st.divider()

        if st.button("Sign out", use_container_width=True):
            from utils.auth import logout
            logout()


def get_current_page() -> str:
    """Return the currently active page key."""
    return st.session_state.get("current_page", NAV_ITEMS[0][0])
