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
    
    # Render styled cards
    st.markdown('<div class="nav-cards">', unsafe_allow_html=True)
    
    for label, icon in nav_items:
        bg_color = PASTEL_COLORS.get(label, "#FFFFFF")
        is_active = "active" if label == st.session_state.get("current_page") else ""
        
        st.markdown(f"""
            <div class="nav-card-item {is_active}" 
                 style="background-color: {bg_color};">
                <span class="nav-icon">{icon}</span>
                {label}
            </div>
        """, unsafe_allow_html=True)
    
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
    
    # Sign out button
    if st.button("Sign out", use_container_width=True):
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