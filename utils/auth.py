"""
Session-state based authentication for Streamlit.
Credentials are stored in st.secrets["credentials"].
"""

import streamlit as st
import bcrypt


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def login_form() -> bool:
    """
    Render login form. Returns True if the user is authenticated.
    Sets st.session_state.authenticated, .username, .role on success.
    """
    from utils.styles import inject_global_css
    inject_global_css()

    if st.session_state.get("authenticated"):
        return True

    # ── Branding header ──────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="height: 4vh;"></div>
        <div style="text-align: center; margin-bottom: 2rem;">
            <div style="
                width: 72px; height: 72px;
                background: linear-gradient(135deg, #1B3A6B 0%, #2D5FA8 100%);
                border-radius: 18px;
                display: flex; align-items: center; justify-content: center;
                font-size: 2.2rem;
                margin: 0 auto 1.1rem;
                box-shadow: 0 6px 20px rgba(27, 58, 107, 0.35);
            ">📊</div>
            <h1 style="
                color: #1B3A6B !important;
                font-size: 1.85rem !important;
                font-weight: 700 !important;
                margin: 0 0 0.25rem !important;
                letter-spacing: -0.4px;
            ">Salasar Services</h1>
            <p style="color: #64748B; font-size: 0.9rem; margin: 0;">
                Ahmedabad Branch &nbsp;·&nbsp; FY 2025-26 Sales Dashboard
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ── Login form (styled via CSS as a card) ────────────────────────────────
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown(
                "<p style='font-weight: 600; color: #1E293B; font-size: 1rem;"
                " margin: 0 0 1rem 0;'>Sign in to your account</p>",
                unsafe_allow_html=True,
            )
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("Sign In  →", use_container_width=True)

    if submitted:
        try:
            user_cfg = st.secrets["credentials"][username]
        except (KeyError, Exception):
            user_cfg = None
        if user_cfg and _verify_password(password, user_cfg["password_hash"]):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = user_cfg.get("role", "viewer")
            st.rerun()
        else:
            with col2:
                st.error("Invalid username or password.")

    # ── Footer ───────────────────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align: center; margin-top: 2.5rem;">
            <p style="color: #CBD5E1; font-size: 0.75rem; margin: 0;">
                © 2025 Salasar Services · Ahmedabad
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    return False


def require_auth():
    """Call at the top of every page. Stops rendering if not logged in."""
    if not st.session_state.get("authenticated"):
        login_form()
        st.stop()


def is_admin() -> bool:
    return st.session_state.get("role") == "admin"


def logout():
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()
