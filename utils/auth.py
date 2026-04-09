"""
Session-state based authentication for Streamlit.
Credentials are stored in st.secrets["credentials"].
"""

import streamlit as st
import bcrypt

LOGO_URL = "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def login_form() -> bool:
    """
    Render the split-layout login page.
    Returns True if the user is already authenticated.
    Sets st.session_state.authenticated / .username / .role on success.
    """
    from utils.styles import inject_login_css
    inject_login_css()

    if st.session_state.get("authenticated"):
        return True

    st.markdown("<div class='login-wrap'>", unsafe_allow_html=True)
    _, center_col, _ = st.columns([1.2, 1, 1.2])
    with center_col:
        st.markdown(
            f"""
            <div class="login-brand">
                <img src="{LOGO_URL}" class="login-logo" alt="Salasar logo" />
                <h2>Sales Enquiry Dashboard</h2>
                <p>Ahmedabad Branch · FY 2025-26</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter username")
            password = st.text_input("Password", type="password", placeholder="Enter password")
            submitted = st.form_submit_button("SIGN IN", use_container_width=True)
        st.markdown(
            "<p class='login-footer'>© Salasar Services Insurance Brokers Pvt. Ltd.</p>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

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
            with center_col:
                st.error("Invalid username or password.")

    return False


def render_sidebar_branding() -> None:
    """Render standard authenticated sidebar branding and sign-out controls."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 0.9rem 0 0.5rem 0;">
                <img src="{LOGO_URL}"
                     style="height: 42px; object-fit: contain;
                            filter: brightness(0) invert(1); opacity: 0.88;
                            display: block;">
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        role_label = "Admin" if is_admin() else "Viewer"
        st.markdown(
            f"""
            <div style="
                display:flex; align-items:center; gap:0.55rem;
                padding:0.45rem 0 0.6rem 0;
            ">
                <div style="
                    width:30px; height:30px;
                    background:rgba(255,255,255,0.11);
                    border-radius:50%;
                    display:flex; align-items:center;
                    justify-content:center; font-size:0.9rem; flex-shrink:0;
                ">👤</div>
                <div>
                    <div style="color:#FFFFFF; font-size:0.84rem; font-weight:600;">
                        {st.session_state.username}
                    </div>
                    <div style="color:rgba(255,255,255,0.46); font-size:0.69rem;">
                        {role_label}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sign Out", use_container_width=True):
            logout()


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
