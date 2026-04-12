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
        
        /* Full screen gradient background */
        [data-testid="stAppViewContainer"] > section {
            background: linear-gradient(135deg, #1555AB 0%, #1e6ad1 30%, #2a7dd4 60%, #3a8ecf 100%) !important;
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
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 24px !important;
            padding: 50px 45px !important;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25) !important;
            max-width: 420px;
            width: 100%;
        }
        
        .glass-logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .glass-logo img {
            height: 55px;
            filter: brightness(0) invert(1);
            opacity: 0.95;
        }
        
        .glass-title {
            text-align: center;
            color: white;
            font-size: 28px;
            font-weight: 700;
            margin: 0 0 8px 0;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .glass-subtitle {
            text-align: center;
            color: rgba(255, 255, 255, 0.75);
            font-size: 14px;
            margin: 0 0 35px 0;
        }
        
        /* Form styling */
        .glass-form label {
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            margin-bottom: 8px !important;
            display: block;
        }
        
        .glass-form .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 12px !important;
            color: white !important;
            padding: 14px 16px !important;
            font-size: 14px !important;
        }
        
        .glass-form .stTextInput > div > div > input::placeholder {
            color: rgba(255, 255, 255, 0.5) !important;
        }
        
        .glass-form .stTextInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.5) !important;
            background: rgba(255, 255, 255, 0.15) !important;
            box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1) !important;
        }
        
        /* Login button */
        .glass-form .stButton > button {
            background: linear-gradient(135deg, #ffffff 0%, #f0f0f0 100%) !important;
            color: #1555AB !important;
            border: none !important;
            border-radius: 12px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            padding: 16px !important;
            width: 100% !important;
            margin-top: 20px;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        }
        
        .glass-form .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.2);
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
            color: rgba(255, 255, 255, 0.5);
            font-size: 11px;
            margin-top: 25px;
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
            <h1 class="glass-title">Welcome Back</h1>
            <p class="glass-subtitle">Sign in to access your dashboard</p>
    """, unsafe_allow_html=True)
    
    with st.form("login_form", clear_on_submit=True):
        username = st.text_input("Username", placeholder="Enter your username")
        password = st.text_input("Password", placeholder="••••••••", type="password")
        submitted = st.button("Sign in")
    
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