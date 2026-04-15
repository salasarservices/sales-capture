"""
Sales Capture Summary page.
"""

import streamlit as st


def render_page():
    """Render the Sales Capture Summary page."""
    
    # Page header
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h1 style="color: #1A1F36; margin: 0; font-size: 22px; font-weight: 600;">
                📈 Sales Capture Summary
            </h1>
            <p style="color: #6B7280; margin: 8px 0 0 0; font-size: 14px;">
                Enquiry volume and premium conversion per sales person
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    from database.connection import get_db
    from database.queries import fetch_summary_sales
    
    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")
    
    with st.spinner("Loading data..."):
        df = fetch_summary_sales(db, fy=fy, branch=branch)
    
    if df.empty:
        st.warning("No data found.")
        return
    
    # Charts
    from components.charts import horizontal_bar_premium, pie_enquiry_share
    from components.data_tables import render_html_table
    from utils.formatters import format_inr, format_pct
    
    col1, col2 = st.columns([3, 2])
    with col1:
        st.plotly_chart(horizontal_bar_premium(df), width='stretch')
    with col2:
        st.plotly_chart(pie_enquiry_share(df), width='stretch')
    
    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
    st.divider()
    
    # Table
    st.markdown(
        '<p class="text-[13px] font-semibold text-[#1A1F36] border-l-[3px] border-[#185FA5] '
        'pl-[10px] my-3 block">Sales Capture Details</p>',
        unsafe_allow_html=True,
    )
    
    display_df = df.copy()
    display_df["Premium Converted (₹)"] = display_df["Premium Converted (₹)"].apply(format_inr)
    display_df["% Not Converted"] = display_df["% Not Converted"].apply(format_pct)
    
    render_html_table(display_df, height=400, id_col="CRE / RM")
