"""
Tab A — Summary: Conversion Ratio
Per CRE/RM breakdown by proposal type (Fresh / Renewal / Expanded).
"""

import streamlit as st

st.set_page_config(page_title="Summary: Conversion Ratio", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth, is_admin, render_sidebar_branding
from database.connection import get_db
from database.queries import fetch_kpis, fetch_summary_conversion
from components.kpi_cards import render_kpi_row
from components.charts import stacked_bar_conversion, grouped_bar_proposal_type
from components.data_tables import render_html_table, export_csv_button
from utils.formatters import format_inr, format_pct

require_auth()
inject_global_css()
render_sidebar_branding()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1>📊 Summary: Conversion Ratio</h1>
    <p class="page-subtitle">Per CRE/RM breakdown — Fresh, Renewal, and Expanded business</p>
    """,
    unsafe_allow_html=True,
)

db = get_db()

# ── KPI Row ───────────────────────────────────────────────────────────────────
with st.spinner("Loading KPIs…"):
    kpis = fetch_kpis(db)
render_kpi_row(kpis)
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)
st.divider()

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading conversion data…"):
    df = fetch_summary_conversion(db)

if df.empty:
    st.warning("No data found for FY 2025-26 / Ahmedabad.")
    st.stop()

# ── Charts ────────────────────────────────────────────────────────────────────
sales_view = df[["CRE / RM", "fresh_converted", "renewal_converted",
                  "expanded_converted", "total_not_converted", "total_enquiries"]].copy()
sales_view["Converted"]      = (sales_view["fresh_converted"].fillna(0)
                                 + sales_view["renewal_converted"].fillna(0)
                                 + sales_view["expanded_converted"].fillna(0))
sales_view["Not Converted"]  = sales_view["total_not_converted"].fillna(0)
sales_view["Total Enquiries"]= sales_view["total_enquiries"].fillna(0)

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(stacked_bar_conversion(sales_view), width="stretch")
with col2:
    st.plotly_chart(grouped_bar_proposal_type(df), width="stretch")

st.divider()

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-heading">Conversion Ratio Detail</p>', unsafe_allow_html=True)

display_cols = {
    "CRE / RM":                  "CRE / RM",
    "total_enquiries":           "Total",
    "fresh_total":               "Fresh Total",
    "fresh_converted":           "Fresh Conv.",
    "fresh_premium":             "Fresh Premium (₹)",
    "fresh_brokerage":           "Fresh Brokerage (₹)",
    "fresh_pct":                 "Fresh %",
    "renewal_total":             "Renewal Total",
    "renewal_converted":         "Renewal Conv.",
    "renewal_premium":           "Renewal Premium (₹)",
    "renewal_brokerage":         "Renewal Brokerage (₹)",
    "renewal_pct":               "Renewal %",
    "expanded_total":            "Expanded Total",
    "expanded_converted":        "Expanded Conv.",
    "expanded_premium":          "Expanded Premium (₹)",
    "expanded_brokerage":        "Expanded Brokerage (₹)",
    "expanded_pct":              "Expanded %",
    "total_premium_converted":   "Total Premium (₹)",
    "total_brokerage_converted": "Total Brokerage (₹)",
    "total_not_converted":       "Not Conv.",
    "pct_not_converted":         "% Not Conv.",
}

display_df = df[[c for c in display_cols if c in df.columns]].rename(columns=display_cols)

for col in display_df.columns:
    if "(₹)" in col:
        display_df[col] = display_df[col].apply(format_inr)
    elif col.endswith("%"):
        display_df[col] = display_df[col].apply(format_pct)

render_html_table(display_df, height=420, id_col="CRE / RM")

if is_admin():
    export_csv_button(df, filename="summary_conversion.csv")
