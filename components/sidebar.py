"""Sidebar component styled to match the provided dashboard mockup."""

import streamlit as st


NAV_ITEMS = [
    "Business Conversion Ratio",
    "Sales Capture Summary",
    "Conversion Ratio Summary",
    "Master Data (From April 25 to March 26)",
]


def render_sidebar():
    """Render sidebar UI aligned to the reference design."""

    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{
            background: #26479D !important;
            border-right: none !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            background: transparent !important;
            padding-top: 0.5rem;
            padding-bottom: 1rem;
        }}

        .sidebar-logo {{
            text-align: center;
            padding: 0.4rem 0.4rem 0.6rem;
        }}

        .sidebar-logo img {{
            width: 170px;
            max-width: 100%;
            filter: brightness(0) invert(1);
            opacity: 0.96;
        }}

        .user-panel {{
            display: flex;
            align-items: center;
            background: #6C4AA7;
            border-radius: 12px;
            padding: 0.9rem 0.6rem;
            margin: 0.25rem 0.35rem 0.6rem;
            gap: 0.75rem;
        }}

        .user-avatar {{
            width: 48px;
            height: 48px;
            border-radius: 999px;
            background: #95D38A;
            flex-shrink: 0;
        }}

        .user-lines {{
            color: white;
            font-size: 0.84rem;
            line-height: 1.65;
            font-weight: 600;
        }}

        .user-lines span {{
            color: rgba(255, 255, 255, 0.92);
            font-weight: 500;
        }}

        [data-testid="stSidebar"] .stButton {{
            margin: 0.45rem 0.35rem;
        }}

        [data-testid="stSidebar"] .stButton > button {{
            width: 100%;
            border-radius: 14px;
            background: #9AD8E8 !important;
            color: #101826 !important;
            border: none !important;
            font-size: 1.08rem;
            font-weight: 700;
            min-height: 42px;
            cursor: pointer;
        }}

        [data-testid="stSidebar"] .stButton > button:hover {{
            background: #A5DFED !important;
        }}

        .masterdata-note {{
            margin-top: -0.25rem;
            margin-left: 6.05rem;
            font-size: 0.64rem;
            color: white;
            background: #44BC7A;
            border-radius: 999px;
            padding: 0.26rem 0.55rem;
            display: inline-block;
        }}

        .logout-wrap {{
            margin-top: 9rem;
            margin-left: 0.35rem;
            margin-right: 0.35rem;
            margin-bottom: 0.5rem;
        }}

        .logout-wrap [data-testid="stButton"] {{
            margin: 0;
        }}

        .logout-wrap [data-testid="stButton"] button {{
            background: #6B4BA6 !important;
            color: #FFFFFF !important;
            font-size: 1.05rem;
            font-weight: 700;
        }}
        </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username", "Show Username")
    session_text = st.session_state.get("session_duration", "Show Session Duration")

    st.markdown("""
        <div class="sidebar-logo">
            <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="user-panel">
            <div class="user-avatar"></div>
            <div class="user-lines">
                USER: <span>{username}</span><br>
                SESSION: <span>{session_text}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

    if "current_page" not in st.session_state:
        st.session_state.current_page = "Business Conversion Ratio"

    for item in NAV_ITEMS:
        if st.button(item, use_container_width=True, key=f"nav_{item}"):
            st.session_state.current_page = item
            st.rerun()
        if item == "Master Data (From April 25 to March 26)":
            st.markdown('<div class="masterdata-note">April 25 to March 26</div>', unsafe_allow_html=True)

    st.markdown('<div class="logout-wrap">', unsafe_allow_html=True)
    submitted = st.button("Logout", use_container_width=True, key="logout_btn")
    st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        from utils.auth import logout
        logout()


def navigate_to_page(page_name: str):
    """Navigate to a specific page."""
    st.session_state.current_page = page_name
    st.rerun()


def get_current_page() -> str:
    """Get the current page name."""
    return st.session_state.get("current_page", "Business Conversion Ratio")
