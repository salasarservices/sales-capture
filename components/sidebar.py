"""
Sidebar component - Glassmorphism design with 4 navigation tabs.
"""

import streamlit as st
from datetime import date


# Pastel colors for nav cards (Sentence Case labels)
PASTEL_COLORS = {
    "Business Conversion Ratio": "#E8F4FD",      # Light blue
    "Sales Capture Summary": "#E8F8F0",          # Light green
    "Conversion Ratio Summary": "#FEF3E2",        # Light amber
    "Master Data (From April 25 to March 26)": "#F3E8FD",  # Light purple
}

# Sidebar background color
SIDEBAR_COLOR = "rgb(22, 85, 171)"


def render_sidebar():
    """Render the sidebar with glassmorphism effect and 4 nav tabs."""
    
    # Glassmorphism CSS
    st.markdown(f"""
        <style>
        [data-testid="stSidebar"] {{
            background: linear-gradient(160deg, #1555AB 0%, #1a5aaa 50%, #1a4d80 100%) !important;
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-right: none !important;
            box-shadow: 4px 0 25px rgba(0, 0, 0, 0.2) !important;
        }}
        
        [data-testid="stSidebar"] > div:first-child {{
            background: transparent !important;
        }}
        
        [data-testid="stSidebar"] .stRadio > label {{
            display: none !important;
        }}
        
        /* Hide Streamlit radio circle */
        [data-testid="stSidebar"] .stRadio [aria-disabled="false"] {{
            opacity: 0;
            position: absolute;
        }}
        
        /* Logo styling */
        .sidebar-logo {{
            text-align: center;
            padding: 1.2rem 0.5rem 0.5rem;
            margin-bottom: 0.5rem;
        }}
        .sidebar-logo img {{
            height: 42px;
            filter: brightness(0) invert(1);
            opacity: 0.95;
        }}
        
        /* Sidebar title */
        .sidebar-title {{
            text-align: center;
            color: rgba(255, 255, 255, 0.9);
            font-size: 13px;
            font-weight: 500;
            margin-bottom: 1rem;
            padding: 0 0.5rem;
        }}
        
        /* Navigation cards container */
        .nav-cards {{
            display: flex;
            flex-direction: column;
            gap: 14px;
            padding: 0.75rem;
            margin-top: 0.5rem;
        }}
        
        /* Individual nav card */
        .nav-card-item {{
            padding: 18px 20px;
            border-radius: 14px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            font-size: 14px;
            font-weight: 500;
            color: #1A1F36;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
        }}
        
        .nav-card-item:hover {{
            transform: translateY(-3px);
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
        }}
        
        .nav-card-item.active {{
            font-weight: 600;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            transform: translateY(-3px);
        }}
        
        /* Icon styling */
        .nav-icon {{
            font-size: 20px;
            margin-right: 14px;
            width: 28px;
            text-align: center;
        }}
        
        /* User info section */
        .sidebar-user {{
            position: absolute;
            bottom: 90px;
            left: 0;
            right: 0;
            padding: 1rem;
            text-align: center;
        }}
        .user-name {{
            color: white;
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 6px;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }}
        .user-role {{
            color: rgba(255, 255, 255, 0.75);
            font-size: 12px;
        }}
        
        /* Sign out button */
        .signout-section {{
            position: absolute;
            bottom: 25px;
            left: 0;
            right: 0;
            padding: 0 1rem;
        }}
        .signout-btn {{
            width: 100%;
            padding: 12px;
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 10px;
            color: white;
            font-size: 13px;
            font-weight: 500;
            cursor: pointer;
            transition: all 0.25s ease;
        }}
        .signout-btn:hover {{
            background: rgba(255, 255, 255, 0.22);
            border-color: rgba(255, 255, 255, 0.3);
        }}
        
        /* IRDA text */
        .irda-text {{
            color: rgba(255, 255, 255, 0.45);
            font-size: 10px;
            text-align: center;
            margin-top: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)
    
    # Logo
    st.markdown("""
        <div class="sidebar-logo">
            <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="sidebar-title">Navigation</div>', unsafe_allow_html=True)
    
    # Navigation tabs - 4 cards with different pastel colors (Sentence Case)
    nav_items = [
        ("Business Conversion Ratio", "📅"),
        ("Sales Capture Summary", "📈"),
        ("Conversion Ratio Summary", "📊"),
        ("Master Data (From April 25 to March 26)", "📋"),
    ]
    
    # Get current page or default to first (Business Conversion Ratio)
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Business Conversion Ratio"
    
    current_page = st.session_state.get("current_page", "Business Conversion Ratio")
    
    # Create radio buttons for state management (hidden)
    selected = st.radio(
        "nav",
        [label for label, _ in nav_items],
        index=[label for label, _ in nav_items].index(current_page) if current_page in [l for l, _ in nav_items] else 0,
        label_visibility="collapsed",
        key="nav_radio"
    )
    
    if selected:
        st.session_state.current_page = selected
    
    # Render interactive nav cards (buttons) so clicking a card changes page
    st.markdown('<div class="nav-cards">', unsafe_allow_html=True)

    for index, (label, icon) in enumerate(nav_items):
        bg_color = PASTEL_COLORS.get(label, "#FFFFFF")
        is_active = label == st.session_state.get("current_page")
        border_color = "rgba(26, 31, 54, 0.25)" if is_active else "rgba(26, 31, 54, 0.08)"
        shadow = "0 8px 25px rgba(0, 0, 0, 0.15)" if is_active else "0 2px 8px rgba(0, 0, 0, 0.06)"
        weight = "600" if is_active else "500"

        st.markdown(
            f"""
            <style>
            div[data-testid="stVerticalBlock"] div[data-testid="stButton"] button[key="nav_card_{index}"] {{
                background: {bg_color} !important;
                color: #1A1F36 !important;
                border: 1px solid {border_color} !important;
                border-radius: 14px !important;
                padding: 0.85rem 0.9rem !important;
                min-height: 58px !important;
                font-size: 14px !important;
                font-weight: {weight} !important;
                text-align: left !important;
                box-shadow: {shadow} !important;
                transition: all 0.25s ease !important;
                justify-content: flex-start !important;
                margin-bottom: 0.45rem !important;
            }}
            div[data-testid="stVerticalBlock"] div[data-testid="stButton"] button[key="nav_card_{index}"]:hover {{
                transform: translateY(-3px);
                box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12) !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        if st.button(f"{icon}  {label}", key=f"nav_card_{index}", use_container_width=True):
            if st.session_state.get("current_page") != label:
                st.session_state.current_page = label
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)
    
    # User info at bottom
    username = st.session_state.get("username", "Admin")
    role = st.session_state.get("role", "viewer")
    role_label = "Admin" if role == "admin" else "Viewer"
    
    st.markdown(f"""
        <div class="sidebar-user">
            <div class="user-name">👤 {username}</div>
            <div class="user-role">🔐 {role_label}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Sign out button - use a form to isolate it
    with st.form("signout_form"):
        submitted = st.form_submit_button("Sign out", use_container_width=True)
    
    if submitted:
        from utils.auth import logout
        logout()
    
    # IRDA license text
    st.markdown("""
        <div class="irda-text">IRDA License No: 2024-25/SALASAR/001</div>
    """, unsafe_allow_html=True)


def navigate_to_page(page_name: str):
    """Navigate to a specific page."""
    st.session_state.current_page = page_name
    st.rerun()


def get_current_page() -> str:
    """Get the current page name."""
    return st.session_state.get("current_page", "Business Conversion Ratio")
