"""Sidebar component styled to match the provided dashboard mockup."""

import streamlit as st
from utils.auth import logout


NAV_ITEMS = [
    "Business Conversion Ratio",
    "Sales Capture Summary",
    "Conversion Ratio Summary",
    "Master Data (From April 25 to March 26)",
]


def _build_user_badge_data() -> dict[str, str]:
    """Prepare profile badge values for sidebar card."""
    username = st.session_state.get("username", "sallead")
    role = st.session_state.get("role", "admin")
    session_text = st.session_state.get("session_duration", "0:38")
    db_status = st.session_state.get("db_status", "Connected")
    env = st.session_state.get("app_env", "Production")

    initials = (username[:3] or "SAL").upper()

    return {
        "username": username,
        "handle": f"@{username}",
        "role": role.upper(),
        "session_text": session_text,
        "db_status": db_status,
        "env": env.upper(),
        "initials": initials,
    }


def render_sidebar():
    """Render sidebar UI aligned to the reference design."""

    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] {
            display: none !important;
        }

        [data-testid="stSidebar"] {
            background: #26479D !important;
            border-right: none !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
            padding-top: 0.5rem;
            padding-bottom: 1rem;
        }

        .sidebar-logo {
            text-align: center;
            padding: 0.4rem 0.4rem 0.6rem;
        }

        .sidebar-logo img {
            width: 170px;
            max-width: 100%;
            filter: brightness(0) invert(1);
            opacity: 0.96;
        }

        .profile-badge {
            position: relative;
            background: #ECECEC;
            border-radius: 14px;
            padding: 0.65rem;
            margin: 0.35rem 0.35rem 0.85rem;
            border-top: 3px solid #20B769;
            color: #213242;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.12);
        }

        .badge-top {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            padding-bottom: 0.55rem;
            border-bottom: 1px solid rgba(33, 50, 66, 0.14);
        }

        .badge-avatar {
            width: 42px;
            height: 42px;
            border-radius: 999px;
            background: #D9DEC9;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.86rem;
            font-weight: 700;
            color: #234523;
            flex-shrink: 0;
        }

        .badge-name-wrap {
            min-width: 0;
            flex: 1;
        }

        .badge-name {
            font-size: 1rem;
            line-height: 1.05;
            color: #121212;
            font-weight: 700;
            margin: 0;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }

        .badge-handle {
            margin: 0.08rem 0 0;
            font-size: 0.76rem;
            color: #2A4762;
            opacity: 0.9;
            font-weight: 600;
        }

        .badge-role {
            border-radius: 999px;
            padding: 0.24rem 0.58rem;
            background: #D4DDC4;
            color: #3F5A23;
            font-size: 0.7rem;
            font-weight: 800;
            letter-spacing: 0.06em;
        }

        .badge-meta {
            display: grid;
            grid-template-columns: 1fr auto;
            row-gap: 0.34rem;
            column-gap: 0.35rem;
            margin-top: 0.55rem;
            font-size: 0.88rem;
            align-items: center;
        }

        .meta-label {
            color: #35526D;
            font-weight: 500;
        }

        .meta-value {
            color: #111827;
            font-weight: 700;
            justify-self: end;
        }

        .meta-db {
            color: #128C56;
            font-weight: 700;
            justify-self: end;
        }

        .meta-db-dot {
            font-size: 0.68rem;
            margin-right: 0.22rem;
            vertical-align: middle;
        }

        .meta-env {
            justify-self: end;
            background: #D4DDC4;
            border-radius: 999px;
            padding: 0.2rem 0.58rem;
            font-size: 0.72rem;
            color: #2F5720;
            font-weight: 800;
            letter-spacing: 0.04em;
        }

        [data-testid="stSidebar"] .stButton {
            margin: 0.45rem 0.35rem;
        }

        [data-testid="stSidebar"] .stButton > button {
            width: 100%;
            border-radius: 14px;
            background: #9AD8E8 !important;
            color: #101826 !important;
            border: none !important;
            font-size: 1.08rem;
            font-weight: 700;
            min-height: 42px;
            cursor: pointer;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #A5DFED !important;
        }

        .masterdata-note {
            margin-top: -0.25rem;
            margin-left: 6.05rem;
            font-size: 0.64rem;
            color: white;
            background: #44BC7A;
            border-radius: 999px;
            padding: 0.26rem 0.55rem;
            display: inline-block;
        }

        .logout-wrap {
            margin-top: 9rem;
            margin-left: 0.35rem;
            margin-right: 0.35rem;
            margin-bottom: 0.5rem;
        }

        .logout-wrap [data-testid="stButton"] {
            margin: 0;
        }

        .logout-wrap [data-testid="stButton"] button {
            background: #6B4BA6 !important;
            color: #FFFFFF !important;
            font-size: 1.05rem;
            font-weight: 700;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    badge_data = _build_user_badge_data()

    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-logo">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
            </div>
        """,
            unsafe_allow_html=True,
        )

        st.markdown(
            f"""
            <div class="profile-badge">
                <div class="badge-top">
                    <div class="badge-avatar">{badge_data['initials']}</div>
                    <div class="badge-name-wrap">
                        <p class="badge-name">{badge_data['username']}</p>
                        <p class="badge-handle">{badge_data['handle']}</p>
                    </div>
                    <span class="badge-role">{badge_data['role']}</span>
                </div>
                <div class="badge-meta">
                    <span class="meta-label">Session</span>
                    <span class="meta-value">Active • {badge_data['session_text']}</span>
                    <span class="meta-label">DB</span>
                    <span class="meta-db"><span class="meta-db-dot">●</span>{badge_data['db_status']}</span>
                    <span class="meta-label">Env</span>
                    <span class="meta-env">{badge_data['env']}</span>
                </div>
            </div>
        """,
            unsafe_allow_html=True,
        )

        if "current_page" not in st.session_state:
            st.session_state.current_page = "Business Conversion Ratio"

        for item in NAV_ITEMS:
            if st.button(item, width="stretch", key=f"nav_{item}"):
                st.session_state.current_page = item
                st.rerun()
            if item == "Master Data (From April 25 to March 26)":
                st.markdown('<div class="masterdata-note">April 25 to March 26</div>', unsafe_allow_html=True)

        st.markdown('<div class="logout-wrap">', unsafe_allow_html=True)
        submitted = st.button("Logout", width="stretch", key="logout_btn")
        st.markdown('</div>', unsafe_allow_html=True)

    if submitted:
        logout()


def navigate_to_page(page_name: str):
    """Navigate to a specific page."""
    st.session_state.current_page = page_name
    st.rerun()


def get_current_page() -> str:
    """Get the current page name."""
    return st.session_state.get("current_page", "Business Conversion Ratio")
