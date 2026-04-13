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
    """Render centered glassmorphism login form."""
    if st.session_state.get("authenticated"):
        return True

    st.markdown(
        """
        <style>
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="stHeader"] {
            display: none !important;
        }

        [data-testid="stAppViewContainer"] {
            background:
                radial-gradient(circle at 12% 20%, rgba(141, 196, 255, 0.35) 0%, rgba(141, 196, 255, 0) 42%),
                radial-gradient(circle at 88% 84%, rgba(125, 241, 220, 0.30) 0%, rgba(125, 241, 220, 0) 40%),
                linear-gradient(130deg, #1f4e79 0%, #315f8a 45%, #5f7fa6 100%);
        }

        [data-testid="stAppViewContainer"]::before {
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(6px);
            -webkit-backdrop-filter: blur(6px);
            pointer-events: none;
            z-index: 0;
        }

        .main .block-container {
            min-height: 100vh;
            max-width: 100% !important;
            padding: 0 1rem !important;
            display: flex;
            align-items: stretch;
            justify-content: center;
            flex-direction: column;
            position: relative;
            z-index: 1;
        }

        div[data-testid="stForm"] {
            background: rgb(0 150 136 / 46%);
            border: 1px solid rgba(255, 255, 255, 0.28);
            box-shadow: 0 18px 55px rgba(6, 27, 49, 0.28);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 20px;
            padding: 2rem 1.4rem 1.2rem;
        }

        .login-logo-wrap {
            text-align: center;
            margin-bottom: 1.2rem;
        }

        .login-logo-wrap img {
            width: 160px;
            max-width: 60%;
            filter: brightness(0) invert(1);
            opacity: 0.95;
        }

        .login-title {
            text-align: center;
            color: rgba(255, 255, 255, 0.95);
            font-size: 1.05rem;
            font-weight: 700;
            margin: 0.35rem 0 1.1rem;
        }

        .login-divider {
            border: 0;
            border-top: 1px solid rgba(255, 255, 255, 0.30);
            margin: 0 0 1rem;
        }

        div[data-testid="stForm"] label {
            color: rgba(255, 255, 255, 0.92) !important;
            font-weight: 600 !important;
            font-size: 0.92rem !important;
        }

        div[data-testid="stForm"] .stTextInput input {
            background: rgba(238, 244, 250, 0.94) !important;
            border: 1px solid rgba(255, 255, 255, 0.45) !important;
            border-radius: 10px !important;
            color: #16263a !important;
            padding: 0.68rem 0.8rem !important;
        }

        div[data-testid="stForm"] .stButton > button,
        div[data-testid="stForm"] .stFormSubmitButton > button {
            width: 100%;
            border-radius: 10px;
            background: linear-gradient(110deg, #123a64 0%, #0d4a73 100%);
            border: 1px solid rgba(255, 255, 255, 0.35);
            color: #fff;
            font-weight: 700;
            padding: 0.62rem 0.75rem;
        }

        .login-footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.75);
            font-size: 0.72rem;
            margin-top: 0.65rem;
        }

        .login-error {
            margin-top: 0.75rem;
            border-radius: 8px;
            border: 1px solid rgba(255, 140, 140, 0.45);
            background: rgba(180, 44, 44, 0.22);
            color: #fff;
            font-size: 0.82rem;
            padding: 0.55rem 0.65rem;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    error_message = None
    _, center_col, _ = st.columns([1, 1.8, 1])
    with center_col:
        with st.form("login_form", clear_on_submit=True):
            st.markdown(
                f"""
                <div class="login-logo-wrap">
                    <img src="{LOGO_URL}" alt="Salasar">
                </div>
                <p class="login-title">Sales Capture Dashboard - Ahmedabad</p>
                <hr class="login-divider">
                """,
                unsafe_allow_html=True,
            )

            username = st.text_input("Username", placeholder="sal.branch", key="login_username")
            password = st.text_input(
                "Password",
                placeholder="••••••••••••••",
                type="password",
                key="login_password",
            )
            submitted = st.form_submit_button("Sign in", width="stretch")

            st.markdown(
                '<div class="login-footer">© Salasar Services (Insurance Brokers) Pvt. Ltd 2026</div>',
                unsafe_allow_html=True,
            )

    if submitted:
        username = st.session_state.get("login_username", "")
        password = st.session_state.get("login_password", "")

        if not username or not password:
            error_message = "Please enter both username and password"
        else:
            try:
                user_cfg = st.secrets["credentials"].get(username)
            except Exception:
                user_cfg = None

            if user_cfg and _verify_password(password, user_cfg.get("password_hash", "")):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user_cfg.get("role", "viewer")
                st.rerun()
            else:
                error_message = "Invalid username or password"

    if error_message:
        st.markdown(f'<div class="login-error">{error_message}</div>', unsafe_allow_html=True)

    return False


def logout():
    """Logout and clear session."""
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()


def render_sidebar_branding():
    """Backward-compatible sidebar branding for legacy page modules."""
    st.sidebar.markdown(
        """
        <div style="text-align:center; padding: 0.5rem 0.4rem 0.8rem;">
            <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"
                 alt="Salasar"
                 style="width:170px; max-width:100%; filter: brightness(0) invert(1); opacity:0.96;">
        </div>
        """,
        unsafe_allow_html=True,
    )
