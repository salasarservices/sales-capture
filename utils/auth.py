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
    """Render glassmorphism login form."""
    if st.session_state.get("authenticated"):
        return True

    # Glassmorphism login CSS
    st.markdown("""
        <style>
        /* Hide sidebar on login */
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }

        .main { margin-left: 0 !important; }
        .main .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
        }

        /* Full-screen soft multi-tone gradient background */
        [data-testid="stAppViewContainer"] > section {
            background: linear-gradient(135deg,
                #5CC8BE 0%,
                #6BAABF 25%,
                #8A9EBB 50%,
                #A89080 75%,
                #C8956A 100%) !important;
            min-height: 100vh;
        }

        /* Glassmorphism login container */
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }

        .glass-card {
            background: rgba(255, 255, 255, 0.14) !important;
            backdrop-filter: blur(24px);
            -webkit-backdrop-filter: blur(24px);
            border: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 20px !important;
            padding: 48px 44px !important;
            box-shadow: 0 24px 64px rgba(0, 0, 0, 0.22) !important;
            max-width: 400px;
            width: 100%;
        }

        .glass-logo {
            text-align: center;
            margin-bottom: 24px;
        }
        .glass-logo img {
            height: 52px;
            filter: brightness(0) invert(1);
            opacity: 0.96;
        }

        .glass-divider {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.22);
            margin: 0 0 28px 0;
        }

        .glass-title {
            text-align: center;
            color: white;
            font-size: 22px;
            font-weight: 700;
            margin: 0 0 28px 0;
            letter-spacing: 0.3px;
            text-shadow: 0 2px 6px rgba(0,0,0,0.15);
        }

        /* Hide Streamlit input labels on login page */
        [data-testid="stForm"] label {
            display: none !important;
        }
        [data-testid="stForm"] .stTextInput {
            margin-bottom: 12px;
        }

        /* Input fields */
        [data-testid="stForm"] .stTextInput > div > div > input {
            background: rgba(240, 244, 248, 0.92) !important;
            border: 1px solid rgba(255, 255, 255, 0.4) !important;
            border-radius: 10px !important;
            color: #1A1F36 !important;
            padding: 14px 16px !important;
            font-size: 14px !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.08) !important;
        }

        [data-testid="stForm"] .stTextInput > div > div > input::placeholder {
            color: #9AA3AF !important;
        }

        [data-testid="stForm"] .stTextInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.7) !important;
            background: rgba(255, 255, 255, 0.98) !important;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2) !important;
        }

        /* Login button — dark charcoal */
        [data-testid="stForm"] .stButton > button,
        [data-testid="stFormSubmitButton"] > button {
            background: #2C3344 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 15px !important;
            padding: 15px !important;
            width: 100% !important;
            margin-top: 6px;
            transition: all 0.25s ease;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
            letter-spacing: 0.3px;
        }

        [data-testid="stForm"] .stButton > button:hover,
        [data-testid="stFormSubmitButton"] > button:hover {
            background: #1E2535 !important;
            transform: translateY(-1px);
            box-shadow: 0 8px 22px rgba(0, 0, 0, 0.3);
        }

        /* Error message */
        .glass-error {
            background: rgba(255, 100, 100, 0.18);
            border: 1px solid rgba(255, 100, 100, 0.28);
            border-radius: 10px;
            padding: 12px;
            color: white;
            font-size: 13px;
            text-align: center;
            margin-top: 14px;
        }

        /* Footer text */
        .glass-footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.52);
            font-size: 11px;
            margin-top: 28px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Render login form
    st.markdown('<div class="login-container">', unsafe_allow_html=True)

    st.markdown("""
        <div class="glass-card">
            <div class="glass-logo">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
            </div>
            <hr class="glass-divider">
            <h1 class="glass-title">Circular Analysis Tool</h1>
    """, unsafe_allow_html=True)

    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username", placeholder="Username")
        password = st.text_input("Password", placeholder="Password", type="password")
        submitted = st.form_submit_button("Sign In", use_container_width=True)
    
    error_message = None
    if submitted:
        if not username or not password:
            error_message = "Please enter both username and password"
        else:
            try:
                user_cfg = st.secrets["credentials"].get(username)
            except:
                user_cfg = None
            
            if user_cfg and _verify_password(password, user_cfg.get("password_hash", "")):
                st.session_state["authenticated"] = True
                st.session_state["username"] = username
                st.session_state["role"] = user_cfg.get("role", "viewer")
                st.rerun()
            else:
                error_message = "Invalid username or password"
    
    if error_message:
        st.markdown(f'<div class="glass-error">{error_message}</div>', unsafe_allow_html=True)
    
    st.markdown("""
            <div class="glass-footer">
                &copy; Salasar Services Insurance Brokers Pvt. Ltd. 2026
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    return False


def logout():
    """Logout and clear session."""
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()