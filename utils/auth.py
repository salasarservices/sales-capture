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
    """Render glassmorphism login form - centered fixed position."""
    if st.session_state.get("authenticated"):
        return True

    # Glassmorphism login CSS - Fixed center positioning
    st.markdown("""
        <style>
        /* Hide sidebar on login */
        [data-testid="stSidebar"],
        [data-testid="stSidebarCollapsedControl"] {
            display: none !important;
        }
        
        /* Reset main container */
        .main {
            margin-left: 0 !important;
            margin-top: 0 !important;
            padding-top: 0 !important;
        }
        
        .block-container {
            padding: 0 !important;
            max-width: 100% !important;
            margin: 0 !important;
            width: 100% !important;
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100vh !important;
        }
        
        /* Full screen gradient background */
        [data-testid="stAppViewContainer"] > section {
            background: linear-gradient(135deg, #1555AB 0%, #1e6ad1 30%, #2a7dd4 60%, #3a8ecf 100%) !important;
            min-height: 100vh;
            height: 100vh;
            overflow: hidden;
        }
        
        /* Centered login card */
        .login-wrapper {
            position: fixed !important;
            top: 50% !important;
            left: 50% !important;
            transform: translate(-50%, -50%) !important;
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
            height: 100%;
            padding: 0;
        }
        
        .glass-card {
            background: rgba(0, 150, 136, 0.46) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 20px !important;
            padding: 35px 40px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25) !important;
            max-width: 380px;
            width: 90%;
        }
        
        .glass-logo {
            text-align: center;
            margin-bottom: 15px;
        }
        .glass-logo img {
            height: 45px;
            filter: brightness(0) invert(1);
            opacity: 0.95;
        }
        
        .glass-title {
            text-align: center;
            color: white;
            font-size: 1.6rem !important;
            font-weight: 600;
            margin: 0 0 5px 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            line-height: 1.3;
        }
        
        /* Form styling */
        .glass-form .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.3) !important;
            border-radius: 10px !important;
            color: white !important;
            padding: 12px 14px !important;
            font-size: 14px !important;
        }
        
        .glass-form .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.6) !important;
        }
        
        .glass-form .stTextInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.6) !important;
            background: rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.15) !important;
        }
        
        .glass-form label {
            color: rgba(255, 255, 255, 0.9) !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            margin-bottom: 6px !important;
            display: block;
        }
        
        .glass-form > div {
            margin-bottom: 15px !important;
        }
        
        /* Login button */
        .glass-form .stButton > button {
            background: linear-gradient(135deg, #ffffff 0%, #e8e8e8 100%) !important;
            color: #1555AB !important;
            border: none !important;
            border-radius: 10px !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            padding: 14px !important;
            width: 100% !important;
            margin-top: 10px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        }
        
        .glass-form .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
        }
        
        /* Error message */
        .glass-error {
            background: rgba(255, 100, 100, 0.25);
            border: 1px solid rgba(255, 100, 100, 0.4);
            border-radius: 8px;
            padding: 12px;
            color: white;
            font-size: 13px;
            text-align: center;
            margin-top: 12px;
        }
        
        /* Footer text */
        .glass-footer {
            text-align: center;
            color: rgba(255, 255, 255, 0.7);
            font-size: 11px;
            margin-top: 25px;
            font-weight: 500;
        }
        
        /* Remove Streamlit default styling */
        [data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Render login form - fixed center position
    st.markdown('<div class="login-wrapper">', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="glass-card">
            <div class="glass-logo">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
            </div>
            <h1 class="glass-title">Sales Capture Dashboard - Ahmedabad</h1>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username", placeholder="Enter username", key="login_username")
        password = st.text_input("Password", placeholder="Enter password", type="password", key="login_password")
        submitted = st.form_submit_button("Login", use_container_width=True)
    
    error_message = None
    if submitted:
        username = st.session_state.get("login_username", "")
        password = st.session_state.get("login_password", "")
        if not username or not password:
            error_message = "Please enter username and password"
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
                © Salasar Services (Insurance Brokers) Pvt. Ltd 2026
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