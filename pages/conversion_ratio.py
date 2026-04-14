"""
Conversion Ratio Summary page.
"""

import streamlit as st
import streamlit_shadcn_ui as ui


def render_page():
    """Render the Conversion Ratio Summary page."""

    # Breadcrumb — page context
    ui.breadcrumb(
        [{"label": "Salasar Analytics", "href": None}, {"label": "Conversion Ratio Summary", "href": None}],
        class_name="mb-2",
    )

    # Page header
    ui.element("h1", children=["📊 Conversion Ratio Summary"],
               className="text-[22px] font-semibold text-gray-900 mt-0 mb-1 leading-tight")
    ui.element("p", children=["Per CRE/RM breakdown by proposal type (Fresh, Renewal, Expanded)"],
               className="text-sm text-gray-500 mt-0 mb-6")

    # Load data
    from database.connection import get_db
    from database.queries import fetch_kpis, fetch_summary_conversion

    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")

    # KPI row
    with st.spinner("Loading KPIs..."):
        kpis = fetch_kpis(db, fy=fy, branch=branch)

    from components.kpi_cards import render_kpi_row
    render_kpi_row(kpis)

    # Divider
    ui.element("hr", className="border-t border-gray-200 my-5")

    # Charts
    with st.spinner("Loading data..."):
        df = fetch_summary_conversion(db, fy=fy, branch=branch)

    if df.empty:
        ui.alert(
            title="No Data Found",
            description="No conversion ratio data available for the selected period and branch.",
        )
        return

    from components.charts import stacked_bar_conversion, grouped_bar_proposal_type
    from components.data_tables import render_html_table
    from utils.formatters import format_inr, format_pct

    # Prepare chart data
    sales_view = df[["CRE / RM", "fresh_converted", "renewal_converted",
                     "expanded_converted", "total_not_converted", "total_enquiries"]].copy()
    sales_view["Converted"] = (sales_view["fresh_converted"].fillna(0) +
                               sales_view["renewal_converted"].fillna(0) +
                               sales_view["expanded_converted"].fillna(0))
    sales_view["Not Converted"] = sales_view["total_not_converted"].fillna(0)
    sales_view["Total Enquiries"] = sales_view["total_enquiries"].fillna(0)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(stacked_bar_conversion(sales_view), width='stretch')
    with col2:
        st.plotly_chart(grouped_bar_proposal_type(df), width='stretch')

    # Divider
    ui.element("hr", className="border-t border-gray-200 my-6")

    # Section heading
    ui.element("h2", children=["Conversion Ratio Details"],
               className="text-sm font-semibold text-gray-800 border-l-4 border-[#185FA5] pl-3 mt-0 mb-3")

    display_cols = {
        "CRE / RM": "CRE / RM",
        "total_enquiries": "Total",
        "fresh_total": "Fresh Total",
        "fresh_converted": "Fresh Conv.",
        "fresh_premium": "Fresh Premium (₹)",
        "fresh_pct": "Fresh %",
        "renewal_total": "Renewal Total",
        "renewal_converted": "Renewal Conv.",
        "renewal_premium": "Renewal Premium (₹)",
        "renewal_pct": "Renewal %",
        "expanded_total": "Expanded Total",
        "expanded_converted": "Expanded Conv.",
        "expanded_premium": "Expanded Premium (₹)",
        "expanded_pct": "Expanded %",
        "total_premium_converted": "Total Premium (₹)",
        "total_not_converted": "Not Conv.",
        "pct_not_converted": "% Not Conv.",
    }

    display_df = df[[c for c in display_cols if c in df.columns]].rename(columns=display_cols)

    for col in display_df.columns:
        if "(₹)" in col:
            display_df[col] = display_df[col].apply(format_inr)
        elif col.endswith("%"):
            display_df[col] = display_df[col].apply(format_pct)

    render_html_table(display_df, height=420, id_col="CRE / RM")
