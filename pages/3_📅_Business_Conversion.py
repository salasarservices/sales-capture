"""
Tab C — Business Conversion Ratio
Monthly enquiry count and conversion rate for FY 2025-26.
"""

import streamlit as st

st.set_page_config(page_title="Business Conversion Ratio", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth, is_admin, render_sidebar_branding
from database.connection import get_db
from database.queries import fetch_business_conversion
from components.charts import dual_axis_monthly
from components.data_tables import render_html_table, export_csv_button
from utils.formatters import format_pct

require_auth()
inject_global_css()
render_sidebar_branding()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1>📅 Business Conversion Ratio</h1>
    <p class="page-subtitle">Month-by-month enquiry volume and conversion rate — FY 2025-26</p>
    """,
    unsafe_allow_html=True,
)

db = get_db()

with st.spinner("Loading monthly data…"):
    df = fetch_business_conversion(db)

if df.empty:
    st.warning("No data found.")
    st.stop()

# ── Chart ─────────────────────────────────────────────────────────────────────
chart_data = df[df["Month"] != "TOTAL"]
st.plotly_chart(dual_axis_monthly(chart_data), use_container_width=True)

st.divider()

# ── Table ─────────────────────────────────────────────────────────────────────
st.markdown('<p class="section-heading">Monthly Conversion Table</p>', unsafe_allow_html=True)
st.caption(
    ":red[Red] = conversion < 50% &nbsp;|&nbsp; "
    ":orange[Amber] = conversion < 70% &nbsp;|&nbsp; "
    "**TOTAL** row = full FY aggregate"
)

# Keep raw values for row colouring; format display copy
raw_conv = df["Conversion %"].copy()
display_df = df.copy()
display_df["Conversion %"] = display_df["Conversion %"].apply(format_pct)

render_html_table(
    display_df,
    height=520,
    id_col="Month",
    raw_conv=raw_conv,
)

if is_admin():
    export_csv_button(df, filename="business_conversion.csv")