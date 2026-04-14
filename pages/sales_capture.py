"""
Sales Capture Summary page.
"""

import streamlit as st
import streamlit_shadcn_ui as ui


def render_page():
    """Render the Sales Capture Summary page."""

    # Breadcrumb — page context
    ui.breadcrumb(
        [{"label": "Salasar Analytics", "href": None}, {"label": "Sales Capture Summary", "href": None}],
        class_name="mb-2",
    )

    # Page header
    ui.element("h1", children=["📈 Sales Capture Summary"],
               className="text-[22px] font-semibold text-gray-900 mt-0 mb-1 leading-tight")
    ui.element("p", children=["Enquiry volume and premium conversion per sales person"],
               className="text-sm text-gray-500 mt-0 mb-6")

    # Load data
    from database.connection import get_db
    from database.queries import fetch_summary_sales

    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")

    with st.spinner("Loading data..."):
        df = fetch_summary_sales(db, fy=fy, branch=branch)

    if df.empty:
        ui.alert(
            title="No Data Found",
            description="No sales capture data available for the selected period and branch.",
        )
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

    # Divider
    ui.element("hr", className="border-t border-gray-200 my-6")

    # Section heading
    ui.element("h2", children=["Sales Capture Details"],
               className="text-sm font-semibold text-gray-800 border-l-4 border-[#185FA5] pl-3 mt-0 mb-3")

    display_df = df.copy()
    display_df["Premium Converted (₹)"] = display_df["Premium Converted (₹)"].apply(format_inr)
    display_df["% Not Converted"] = display_df["% Not Converted"].apply(format_pct)

    render_html_table(display_df, height=400, id_col="CRE / RM")
