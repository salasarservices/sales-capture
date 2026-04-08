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
    if st.session_state.get("authenticated"):
        return True

    st.markdown(
        """
        <div style='text-align:center; padding: 2rem 0 1rem 0;'>
            <h1 style='color:#1E3A5F; font-size:2rem;'>Salasar Services</h1>
            <p style='color:#64748B;'>Ahmedabad Branch — FY 2025-26 Sales Dashboard</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

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
                st.error("Invalid username or password.")

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
