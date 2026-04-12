"""
Sidebar component with filters and navigation.
Implements UI-DESIGN-INSTRUCTION.md specifications.
"""

import streamlit as st
from datetime import date


MONTH_OPTIONS = ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"]


def render_sidebar():
    """Render the sidebar with filters and navigation."""
    with st.sidebar:
        st.markdown("""
            <div style="padding: 0.6rem 0 0.2rem;">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" 
                     style="height: 36px;">
                <div style="margin-top: 0.4rem; font-size: 13px; font-weight: 500; color: #1A1F36;">
                    Salasar Services — Sales analytics
                </div>
            </div>
        """, unsafe_allow_html=True)

        role = st.session_state.get("role", "viewer")
        role_label = "Admin" if role == "admin" else "Viewer"
        username = st.session_state.get("username", "Unknown")
        st.caption(f"{username} · {role_label}")
        st.divider()

        if "filters_init" not in st.session_state:
            st.session_state.branch = "Ahmedabad"
            st.session_state.fy = "2025-26"
            st.session_state.filters_init = True

        branch = st.selectbox("Branch", ["Ahmedabad", "Surat", "Rajkot", "Vadodara"], index=0)
        fy = st.selectbox("Financial year", ["2024-25", "2025-26", "2026-27"], index=1)
        st.session_state.branch = branch
        st.session_state.fy = fy
        st.divider()

        st.caption("Filters")
        try:
            from database.connection import get_db
            from database.queries import fetch_filter_options
            db = get_db()
            opts = fetch_filter_options(db, fy=st.session_state.fy, branch=st.session_state.branch)
            cre_rms = opts.get("cre_rms", [])
            products = opts.get("requirements", [])
            proposal_types = opts.get("proposal_types", ["Fresh", "Renewal", "Expanded"])
        except Exception:
            cre_rms = ["Kashyap", "Darshan", "Vijay", "Vipul", "Punit", "Hitesh"]
            products = ["Standard Fire & Peril Policy", "Marine Policy", "Contractors All Risk Policy"]
            proposal_types = ["Fresh", "Renewal", "Expanded"]

        selected_cre = st.multiselect("CRE/RM", cre_rms, default=cre_rms)
        selected_types = st.multiselect("Proposal type", proposal_types, default=proposal_types)
        selected_products = st.multiselect("Product", products, default=products)
        month_range = st.select_slider("Month range", options=MONTH_OPTIONS, value=("Apr", "Mar"))

        st.session_state.selected_cre = selected_cre
        st.session_state.selected_types = selected_types
        st.session_state.selected_products = selected_products
        st.session_state.month_range = month_range

        if st.button("Reset filters", use_container_width=True):
            st.session_state.selected_cre = cre_rms
            st.session_state.selected_types = proposal_types
            st.session_state.selected_products = products
            st.session_state.month_range = ("Apr", "Mar")
            st.rerun()

        st.divider()
        st.caption("Navigation")
        nav_options = ["📊 Summary Conversion", "📈 Summary Sales", "📅 Business Conversion", "🔍 Sales Funnel"]
        selected_nav = st.radio("Navigation", nav_options, label_visibility="collapsed")
        page_map = {
            "📊 Summary Conversion": "1_📊_Summary_Conversion",
            "📈 Summary Sales": "2_📈_Summary_Sales",
            "📅 Business Conversion": "3_📅_Business_Conversion",
            "🔍 Sales Funnel": "4_🔍_Sales_Funnel",
        }
        st.session_state.current_page = page_map.get(selected_nav, "1_📊_Summary_Conversion")

        st.divider()
        if st.button("Sign out", use_container_width=True):
            from utils.auth import logout
            logout()
        st.caption("IRDA License No: 2024-25/SALASAR/001")


def render_header():
    """Render the header context bar."""
    today = date.today().strftime("%d %b %Y")
    branch = st.session_state.get("branch", "Ahmedabad")
    fy = st.session_state.get("fy", "2025-26")
    role = st.session_state.get("role", "viewer")
    username = st.session_state.get("username", "Admin")
    
    role_label = "Admin" if role == "admin" else "Viewer"
    
    st.markdown(f"""
        <div style="
            background-color: #042C53;
            padding: 12px 24px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: -1rem -1rem 1rem -1rem;
        ">
            <div>
                <div style="font-size: 18px; font-weight: 500; color: #B5D4F4;">
                    Salasar Services — Sales Analytics
                </div>
                <div style="font-size: 11px; color: #378ADD;">
                    {branch} · FY {fy} · {today}
                </div>
            </div>
            <div style="display: flex; gap: 12px; align-items: center;">
                <div style="
                    background: #0C447C;
                    color: #B5D4F4;
                    padding: 3px 10px;
                    border-radius: 20px;
                    font-size: 11px;
                ">
                    {role_label}
                </div>
                <div style="
                    background: #0F6E56;
                    color: #9FE1CB;
                    padding: 3px 10px;
                    border-radius: 20px;
                    font-size: 11px;
                ">
                    Live
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)


def get_filtered_data():
    """Get the filtered data based on current filter state."""
    from database.connection import get_db
    from database.queries import fetch_filter_options
    
    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")
    
    # Build match query
    match = {"fy": fy, "branch": branch}
    
    selected_cre = st.session_state.get("selected_cre", [])
    if selected_cre:
        match["cre_rm_accountable"] = {"$in": selected_cre}
    
    selected_types = st.session_state.get("selected_types", [])
    if selected_types:
        match["type_of_proposal"] = {"$in": selected_types}
    
    selected_products = st.session_state.get("selected_products", [])
    if selected_products:
        match["requirement"] = {"$in": selected_products}
    
    return db, match


def get_active_filters() -> dict:
    """Return canonical active filters from session state."""
    start_month, end_month = st.session_state.get("month_range", ("Apr", "Mar"))
    start_idx = MONTH_OPTIONS.index(start_month)
    end_idx = MONTH_OPTIONS.index(end_month)
    selected_months = MONTH_OPTIONS[start_idx:end_idx + 1] if start_idx <= end_idx else MONTH_OPTIONS[start_idx:] + MONTH_OPTIONS[:end_idx + 1]
    return {
        "fy": st.session_state.get("fy", "2025-26"),
        "branch": st.session_state.get("branch", "Ahmedabad"),
        "cre_rms": st.session_state.get("selected_cre", []),
        "proposal_types": st.session_state.get("selected_types", []),
        "requirements": st.session_state.get("selected_products", []),
        "months": selected_months,
    }
