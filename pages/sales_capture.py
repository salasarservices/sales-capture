"""
Sales Capture Summary page.
"""

import streamlit as st


def render_page():
    """Render the Sales Capture Summary page."""
    
    st.title("📈 Sales Capture Summary")
    st.caption("Enquiry volume and premium conversion per sales person")
    
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
    
    st.divider()

    st.subheader("Sales Capture Details")
    
    display_df = df.copy()
    display_df["Premium Converted (₹)"] = display_df["Premium Converted (₹)"].apply(format_inr)
    display_df["% Not Converted"] = display_df["% Not Converted"].apply(format_pct)
    
    render_html_table(display_df, height=400, id_col="CRE / RM")
