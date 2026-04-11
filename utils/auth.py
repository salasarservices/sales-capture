"""
Authentication utilities for Streamlit - now uses Django API.
"""

import streamlit as st
from api_client import login as api_login, logout as api_logout, refresh_access_token

LOGO_URL = "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def is_admin() -> bool:
    """Check if current user is admin."""
    user = st.session_state.get("user", {})
    return user.get("role") == "admin"


def require_auth():
    """Require authentication - redirect to login if not authenticated."""
    if not is_authenticated():
        login_form()
        st.stop()


def login_form() -> bool:
    """Render login form using Django API."""
    if st.session_state.get("authenticated"):
        return True

    from utils.styles import inject_login_css
    inject_login_css()

    left_col, right_col = st.columns([5, 7])

    with left_col:
        st.markdown(
            f'<div class="login-brand-card">'
            f'<img src="{LOGO_URL}" class="login-brand-logo">'
            f'<h1 class="login-brand-heading">Sales Enquiry<br>Dashboard</h1>'
            f'<p class="login-brand-sub">Ahmedabad &nbsp;&middot;&nbsp; FY 2025-26</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    with right_col:
        st.markdown('<div style="height:18vh;"></div>', unsafe_allow_html=True)

        _, form_col, _ = st.columns([1, 8, 1])
        with form_col:
            st.markdown(f'<img src="{LOGO_URL}" style="height:36px;object-fit:contain;display:block;margin-bottom:1.25rem;">', unsafe_allow_html=True)
            st.markdown('<h2 style="font-size:1.85rem;font-weight:700;color:#1E293B;margin:0 0 0.2rem;letter-spacing:-0.3px;">Login</h2>', unsafe_allow_html=True)
            st.markdown('<p style="color:#64748B;font-size:0.83rem;margin:0 0 1.5rem;">Enter your dashboard credentials</p>', unsafe_allow_html=True)

            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter username", key="_login_user")
                password = st.text_input("Password", placeholder="••••••••", type="password", key="_login_pass")
                submitted = st.form_submit_button("SIGN IN", use_container_width=True)

        if submitted:
            try:
                api_login(username, password)
                st.rerun()
            except Exception as e:
                with form_col:
                    st.error(f"Invalid username or password.")

    return False


def render_sidebar_branding() -> None:
    """Render logo + user info + sign-out in the sidebar."""
    with st.sidebar:
        st.markdown(f'<img src="{LOGO_URL}" style="height:40px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.88;display:block;margin:0.75rem 0 0.5rem;">', unsafe_allow_html=True)
        st.divider()

        role_label = "Admin" if is_admin() else "Viewer"
        user = st.session_state.get("user", {})
        username = user.get("username", "Unknown")

        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.55rem;padding:0.45rem 0 0.6rem;">'
            f'<div style="width:30px;height:30px;background:rgba(255,255,255,0.11);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;flex-shrink:0;">👤</div>'
            f'<div><div style="color:#FFFFFF;font-size:0.84rem;font-weight:600;">{username}</div>'
            f'<div style="color:rgba(255,255,255,0.46);font-size:0.69rem;">{role_label}</div></div></div>',
            unsafe_allow_html=True,
        )

        if st.button("Sign Out", use_container_width=True):
            logout()


def logout():
    """Logout and clear session."""
    api_logout()
    for key in ["authenticated", "username", "role", "user", "access_token", "refresh_token"]:
        st.session_state.pop(key, None)
    st.rerun()