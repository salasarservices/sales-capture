"""
Tab B — Summary: Sales Capture
Per CRE/RM: total enquiries, converted, premium, not converted.
"""

import streamlit as st

st.set_page_config(page_title="Summary: Sales Capture", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth, is_admin
from database.connection import get_db
from database.queries import fetch_summary_sales
from components.charts import horizontal_bar_premium, pie_enquiry_share
from components.data_tables import render_table, export_csv_button, highlight_totals_row
from utils.formatters import format_inr, format_pct

inject_global_css()
require_auth()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1>📈 Summary: Sales Capture</h1>
    <p class="page-subtitle">Enquiry volume and premium conversion per CRE/RM</p>
    """,
    unsafe_allow_html=True,
)

db = get_db()

with st.spinner("Loading sales data…"):
    df = fetch_summary_sales(db)

if df.empty:
    st.warning("No data found.")
    st.stop()

# ── Charts ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2])
with col1:
    st.plotly_chart(horizontal_bar_premium(df), use_container_width=True)
with col2:
    st.plotly_chart(pie_enquiry_share(df), use_container_width=True)

st.divider()

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown(
    '<p class="section-heading">Sales Capture Summary</p>',
    unsafe_allow_html=True,
)

display_df = df.copy()
display_df["Premium Converted (₹)"] = display_df["Premium Converted (₹)"].apply(format_inr)
display_df["% Not Converted"]       = display_df["% Not Converted"].apply(format_pct)

styled = highlight_totals_row(display_df)
st.dataframe(styled, use_container_width=True, height=400, hide_index=True)

if is_admin():
    export_csv_button(df, filename="summary_sales.csv")
