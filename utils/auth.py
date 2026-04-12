"""
Authentication utilities for Streamlit.
Credentials stored in st.secrets["credentials"].
"""

import streamlit as st
import bcrypt

LOGO_URL = "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"


def _verify_password(plain: str, hashed: str) -> bool:
    """Verify password against bcrypt hash."""
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def is_authenticated() -> bool:
    """Check if user is authenticated."""
    return st.session_state.get("authenticated", False)


def is_admin() -> bool:
    """Check if current user is admin."""
    return st.session_state.get("role") == "admin"


def require_auth():
    """Require authentication - redirect to login if not authenticated."""
    if not is_authenticated():
        login_form()
        st.stop()


def login_form() -> bool:
    """Render login form."""
    if st.session_state.get("authenticated"):
        return True

    from utils.styles import inject_login_css
    inject_login_css()
    st.markdown('<div class="login-page-bg"></div>', unsafe_allow_html=True)
    st.markdown('<div class="login-orb orb-one"></div><div class="login-orb orb-two"></div>', unsafe_allow_html=True)

    _, center_col, _ = st.columns([1.6, 1.1, 1.6])
    with center_col:
        st.markdown(
            f"""
            <div class="glass-login-card">
                <img src="{LOGO_URL}" class="glass-login-logo">
                <h1 class="glass-login-title">Business Analytics Portal</h1>
                <p class="glass-login-subtitle">Sign in to continue</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter username", key="_login_user")
            password = st.text_input("Password", placeholder="••••••••", type="password", key="_login_pass")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

        st.markdown('<p class="login-footnote">© Salasar Services Insurance Brokers Pvt. Ltd. 2026</p>', unsafe_allow_html=True)

    if submitted:
        try:
            user_cfg = st.secrets["credentials"][username]
        except (KeyError, Exception):
            user_cfg = None

        if user_cfg and _verify_password(password, user_cfg["password_hash"]):
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.session_state["role"] = user_cfg.get("role", "viewer")
            st.rerun()
        else:
            with center_col:
                st.error("Invalid username or password.")

    return False


def render_sidebar_branding() -> None:
    """Render logo + user info + sign-out in the sidebar."""
    with st.sidebar:
        st.markdown(f'<img src="{LOGO_URL}" style="height:40px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.88;display:block;margin:0.75rem 0 0.5rem;">', unsafe_allow_html=True)
        st.divider()

        role_label = "Admin" if is_admin() else "Viewer"
        username = st.session_state.get("username", "Unknown")

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
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()
