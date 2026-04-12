"""
Business Conversion Ratio page.
"""

import streamlit as st
from datetime import date


def render_page():
    """Render the Business Conversion Ratio page."""
    
    # Page header
    st.markdown("""
        <div style="margin-bottom: 1.5rem;">
            <h1 style="color: #1A1F36; margin: 0; font-size: 22px; font-weight: 600;">
                📅 Business Conversion Ratio
            </h1>
            <p style="color: #6B7280; margin: 8px 0 0 0; font-size: 14px;">
                Month-by-month enquiry volume and conversion rate
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Load data
    from database.connection import get_db
    from database.queries import fetch_business_conversion
    
    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    
    with st.spinner("Loading data..."):
        df = fetch_business_conversion(db, fy=fy)
    
    if df.empty:
        st.warning("No data found.")
        return
    
    # Display chart and table
    from components.charts import dual_axis_monthly
    from components.data_tables import render_html_table
    from utils.formatters import format_pct
    
    # Chart
    chart_data = df[df["Month"] != "TOTAL"]
    st.plotly_chart(dual_axis_monthly(chart_data), width="stretch")
    
    st.markdown("<div style='height: 1.5rem'></div>", unsafe_allow_html=True)
    st.divider()
    
    # Table
    st.markdown('<p class="section-heading">Monthly Conversion Details</p>', unsafe_allow_html=True)
    st.caption("Red = conversion < 50% | Amber = conversion < 70% | Total = full year aggregate")
    
    raw_conv = df["Conversion %"].copy()
    display_df = df.copy()
    display_df["Conversion %"] = display_df["Conversion %"].apply(format_pct)
    
    render_html_table(display_df, height=500, id_col="Month", raw_conv=raw_conv)