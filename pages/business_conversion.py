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

    # Source data discrepancy notes
    with st.expander("⚠️ Known discrepancies vs. source Excel sheet", expanded=False):
        st.markdown(
            """
**Dashboard figures are sourced from MongoDB and are correctly calculated.**
The source Excel sheet (`Sales Funnel & Enquiry Capture(Apr25 To Mar26)`) has two known formula errors
that cause it to display different numbers:

1. **Jan / Feb / Mar '26 — Impossible conversion rates (e.g. 2000%)**
   The sheet's `Count(Q)` formula for *Business Converted* does not apply a year filter for these
   months, so it counts converted records across **all years** instead of just FY 2025-26.
   The dashboard values for these months are correct.

2. **Apr – Dec '25 — All show exactly 45 enquiries**
   The month filter in the sheet appears to return cached / all-data for these months, giving a
   uniform count regardless of the actual volume per month.
   The dashboard derives counts directly from each row's date, so per-month figures here are accurate.

If the total record count looks lower than expected, MongoDB may need to be re-seeded from the
latest Excel file using `scripts/seed_from_excel.py`.
            """,
            unsafe_allow_html=False,
        )

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
