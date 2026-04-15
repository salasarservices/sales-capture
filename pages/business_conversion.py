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
    fy     = st.session_state.get("fy",     "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")

    with st.spinner("Loading data..."):
        df = fetch_business_conversion(db, fy=fy, branch=branch)
    
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
    
    display_df = df.rename(columns={
        "No. of Enquiries":  "No. of Enquiries",
        "Business Converted": "Business Converted",
        "Conversion %":       "Percentage Converted",
    }).copy()
    display_df["Percentage Converted"] = display_df["Percentage Converted"].apply(format_pct)

    render_html_table(display_df, height=500, id_col="Month")
