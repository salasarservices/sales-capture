"""
Business Conversion Ratio page.
"""

import streamlit as st
from datetime import date


def render_page():
    """Render the Business Conversion Ratio page."""
    
    st.title("📅 Business Conversion Ratio")
    st.caption("Month-by-month enquiry volume and conversion rate")
    
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
    st.plotly_chart(dual_axis_monthly(chart_data), width='stretch')
    
    st.divider()

    st.subheader("Monthly Conversion Details")
    st.caption("Total = full year aggregate")
    
    raw_conv = df["Conversion %"].copy()
    display_df = df.copy()
    display_df["Conversion %"] = display_df["Conversion %"].apply(format_pct)
    
    render_html_table(display_df, height=500, id_col="Month", raw_conv=raw_conv)
