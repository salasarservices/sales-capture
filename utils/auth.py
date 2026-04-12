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
        
        /* Full screen gradient background */
        [data-testid="stAppViewContainer"] > section {
            background:
                radial-gradient(circle at 14% 72%, rgba(34, 165, 214, 0.38) 0%, rgba(34, 165, 214, 0.0) 43%),
                radial-gradient(circle at 82% 32%, rgba(130, 158, 233, 0.30) 0%, rgba(130, 158, 233, 0.0) 44%),
                linear-gradient(122deg, #4BB4BB 0%, #4A86C8 44%, #A3938A 100%) !important;
            min-height: 100vh;
        }

        [data-testid="stAppViewContainer"] > section::before {
            content: "";
            position: fixed;
            inset: 0;
            background: rgba(255, 255, 255, 0.08);
            backdrop-filter: blur(4px);
            -webkit-backdrop-filter: blur(4px);
            pointer-events: none;
        }

        /* Glassmorphism login container */
        .login-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 24px;
            position: relative;
            z-index: 1;
        }

        .glass-card {
            background: rgba(157, 188, 204, 0.32) !important;
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 2px !important;
            padding: 46px 26px 24px !important;
            box-shadow: 0 28px 75px rgba(0, 0, 0, 0.25) !important;
            max-width: 360px;
            width: 360px;
        }

        .glass-logo {
            text-align: center;
            margin-bottom: 54px;
        }

        .glass-logo img {
            height: 74px;
            filter: brightness(0) invert(1);
            opacity: 0.96;
        }

        .glass-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.92);
            font-size: 17px;
            font-weight: 700;
            margin: 0 0 26px 0;
            line-height: 1.2;
            text-shadow: 0 2px 8px rgba(0,0,0,0.18);
        }

        .glass-divider {
            margin: 0 0 28px 0;
            border: 0;
            border-top: 1px solid rgba(255, 255, 255, 0.26);
        }

        /* Form styling */
        .glass-form label {
            color: rgba(255, 255, 255, 0.0) !important;
            font-size: 0 !important;
            font-weight: 500 !important;
            margin-bottom: 2px !important;
            display: block;
        }

        .glass-form .stTextInput > div > div > input {
            background: rgba(236, 242, 249, 0.92) !important;
            border: 1px solid rgba(255, 255, 255, 0.45) !important;
            border-radius: 1px !important;
            color: #1E2A39 !important;
            padding: 14px 14px !important;
            font-size: 14px !important;
            font-weight: 500 !important;
        }

        .glass-form .stTextInput > div > div > input::placeholder {
            color: rgba(46, 64, 84, 0.56) !important;
        }

        .glass-form .stTextInput > div > div > input:focus {
            border-color: rgba(198, 225, 240, 0.95) !important;
            box-shadow: 0 0 0 2px rgba(126, 174, 201, 0.35) !important;
        }

        .glass-form .stTextInput {
            margin-bottom: 0.36rem;
        }

        /* Login button */
        .glass-form .stButton > button {
            background: #24354A !important;
            color: #FFFFFF !important;
            border: 1px solid rgba(255, 255, 255, 0.22) !important;
            border-radius: 1px !important;
            font-weight: 700 !important;
            font-size: 16px !important;
            padding: 13px !important;
            width: 100% !important;
            margin-top: 0.5rem;
            transition: all 0.2s ease;
        }

        .glass-form .stButton > button:hover {
            background: #1A2A3E !important;
            border-color: rgba(255, 255, 255, 0.35) !important;
        }

        /* Error message */
        .glass-error {
            background: rgba(255, 100, 100, 0.2);
            border: 1px solid rgba(255, 100, 100, 0.3);
            border-radius: 10px;
            padding: 12px;
            color: white;
            font-size: 13px;
            text-align: center;
            margin-top: 15px;
        }

        /* Footer text */
        .glass-footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.64);
            font-size: 11px;
            margin-top: 18px;
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
            <p class="glass-subtitle">Circular Analysis Tool</p>
            <hr class="glass-divider">
    """, unsafe_allow_html=True)

    st.markdown('<div class="glass-form">', unsafe_allow_html=True)
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username", placeholder="sal.branch", key="login_username")
        password = st.text_input("Password", placeholder="••••••••••••••", type="password", key="login_password")
        submitted = st.form_submit_button("Sign in", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    error_message = None
    if submitted:
        # Get form values from session state
        username = st.session_state.get("login_username", "")
        password = st.session_state.get("login_password", "")
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
                IRDA License No: 2024-25/SALASAR/001
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
