"""
Business Conversion Ratio page.
"""

import streamlit as st
import streamlit_shadcn_ui as ui


def render_page():
    """Render the Business Conversion Ratio page."""

    # Breadcrumb — page context  ("text" is the required key, not "label")
    ui.breadcrumb(
        [{"text": "Salasar Analytics", "href": None}, {"text": "Business Conversion Ratio", "href": None}],
        key="bc_breadcrumb",
    )

    # Page header — .render() is required; bare ui.element() calls return a
    # UIElement object but do not call component_func() unless rendered explicitly.
    ui.element("h1", children=["📅 Business Conversion Ratio"],
               className="text-[22px] font-semibold text-gray-900 mt-0 mb-1 leading-tight").render()
    ui.element("p", children=["Month-by-month enquiry volume and conversion rate"],
               className="text-sm text-gray-500 mt-0 mb-6").render()

    # Load data
    from database.connection import get_db
    from database.queries import fetch_business_conversion

    db = get_db()
    fy = st.session_state.get("fy", "2025-26")

    with st.spinner("Loading data..."):
        df = fetch_business_conversion(db, fy=fy)

    if df.empty:
        ui.alert(
            title="No Data Found",
            description="No business conversion data available for the selected period.",
        )
        return

    from components.charts import dual_axis_monthly
    from components.data_tables import render_html_table
    from utils.formatters import format_pct

    chart_data = df[df["Month"] != "TOTAL"]
    st.plotly_chart(dual_axis_monthly(chart_data), width='stretch')

    # Divider
    ui.element("hr", className="border-t border-gray-200 my-6").render()

    # Section heading + legend caption
    ui.element("h2", children=["Monthly Conversion Details"],
               className="text-sm font-semibold text-gray-800 border-l-4 border-[#185FA5] pl-3 mt-0 mb-1").render()
    ui.element("p", children=["Red = conversion < 50%  ·  Amber = conversion < 70%  ·  Total = full year aggregate"],
               className="text-xs text-gray-400 mt-0 mb-3").render()

    raw_conv = df["Conversion %"].copy()
    display_df = df.copy()
    display_df["Conversion %"] = display_df["Conversion %"].apply(format_pct)

    render_html_table(display_df, height=500, id_col="Month", raw_conv=raw_conv)
