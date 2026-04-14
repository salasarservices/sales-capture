import streamlit as st

# Pastel colors for nav cards (in order)
PASTEL_COLORS = [
    '#E8F4FD',  # Business Conversion Ratio - light blue
    '#E8F8F0',  # Sales Capture Summary - light green
    '#FEF3E2',  # Conversion Ratio Summary - light amber
    '#F3E8FD',  # Master Data - light purple
]


def render_sidebar():
    st.markdown('''
        <style>
        [data-testid=\"stSidebar\"] {
            background: linear-gradient(160deg, #1555AB 0%, #1a5aaa 50%, #1a4d80 100%) !important;
            backdrop-filter: blur(12px);
            border-right: none !important;
            box-shadow: 4px 0 25px rgba(0, 0, 0, 0.2) !important;
        }
        [data-testid=\"stSidebar\"] > div:first-child { background: transparent !important; }
        [data-testid=\"stSidebar\"] hr { display: none !important; }
        
        .sidebar-logo { text-align: center; padding: 1rem 0.5rem; }
        .sidebar-logo img { height: 38px; filter: brightness(0) invert(1); }
        
        .sidebar-title {
            text-align: center;
            color: rgba(255, 255, 255, 0.85);
            font-size: 12px;
            font-weight: 500;
            margin-bottom: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .sidebar-user {
            position: absolute;
            bottom: 85px;
            left: 0; right: 0;
            padding: 0.75rem;
            text-align: center;
        }
        .user-name { color: white; font-size: 13px; font-weight: 600; }
        .user-role { color: rgba(255, 255, 255, 0.7); font-size: 11px; }
        
        .irda-text {
            position: absolute;
            bottom: 15px;
            left: 0; right: 0;
            color: rgba(255, 255, 255, 0.4);
            font-size: 9px;
            text-align: center;
        }
        
        [data-testid=\"stSidebar\"] .stButton > button {
            background: rgba(255, 255, 255, 0.1);
            border: 1px solid rgba(255, 255, 255, 0.15);
            color: white;
            border-radius: 8px;
            font-size: 12px;
        }
        </style>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
        <div class=\"sidebar-logo\">
            <img src=\"https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png\" alt=\"Salasar\">
        </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class=\"sidebar-title\">Navigation</div>', unsafe_allow_html=True)
    
    nav_items = [
        ('Business Conversion Ratio', '📅'),
        ('Sales Capture Summary', '📈'),
        ('Conversion Ratio Summary', '📊'),
        ('Master Data (From April 25 to March 26)', '📋'),
    ]
    
    if 'current_page' not in st.session_state:
        st.session_state['current_page'] = 'Business Conversion Ratio'
    
    # Render navigation buttons with different pastel colors
    for i, (label, icon) in enumerate(nav_items):
        color = PASTEL_COLORS[i]
        
        # Custom CSS for this specific button
        st.markdown(f'''
            <style>
            [data-testid=\"stSidebar\"] button[key=\"nav_{label}\"] {{
                background-color: {color} !important;
                border: none !important;
                border-radius: 12px !important;
                padding: 14px 16px !important;
                margin-bottom: 8px !important;
                text-align: left !important;
                color: #1A1F36 !important;
                font-size: 13px !important;
                font-weight: 500 !important;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05) !important;
                transition: all 0.2s ease !important;
                display: flex !important;
                align-items: center !important;
            }}
            [data-testid=\"stSidebar\"] button[key=\"nav_{label}\"]:hover {{
                transform: translateY(-2px) !important;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1) !important;
            }}
            </style>
        ''', unsafe_allow_html=True)
        
        if st.button(f'{icon} {label}', key=f'nav_{label}', use_container_width=True):
            st.session_state['current_page'] = label
            st.rerun()
    
    # User info
    username = st.session_state.get('username', 'Admin')
    role = st.session_state.get('role', 'viewer')
    role_label = 'Admin' if role == 'admin' else 'Viewer'
    
    st.markdown(f'''
        <div class=\"sidebar-user\">
            <div class=\"user-name\">👤 {username}</div>
            <div class=\"user-role\">🔐 {role_label}</div>
        </div>
    ''', unsafe_allow_html=True)
    
    if st.button('Sign out', key='signout'):
        from utils.auth import logout
        logout()
    
    st.markdown('''
        <div class=\"irda-text\">IRDA License No: 2024-25/SALASAR/001</div>
    ''', unsafe_allow_html=True)


def navigate_to_page(page_name: str):
    st.session_state['current_page'] = page_name
    st.rerun()


def get_current_page() -> str:
    return st.session_state.get('current_page', 'Business Conversion Ratio')