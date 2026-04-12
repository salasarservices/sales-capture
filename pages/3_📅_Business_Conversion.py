"""
Tab C — Business Conversion Ratio
Monthly enquiry count and conversion rate for FY 2025-26.
"""

import streamlit as st

st.set_page_config(page_title="Business Conversion Ratio", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth, is_admin
from database.connection import get_db
from database.queries import fetch_business_conversion
from components.charts import dual_axis_monthly
from components.data_tables import render_html_table, export_csv_button
from components.sidebar import render_sidebar, render_header, get_active_filters
from utils.formatters import format_pct

require_auth()
inject_global_css()
render_sidebar()
render_header()
filters = get_active_filters()
month_map = {"Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12, "Jan": 1, "Feb": 2, "Mar": 3}
month_ints = [month_map[m] for m in filters["months"]]

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
    df = fetch_business_conversion(
        db,
        fy=filters["fy"],
        branch=filters["branch"],
        cre_rms=filters["cre_rms"],
        proposal_types=filters["proposal_types"],
        requirements=filters["requirements"],
        months=month_ints,
    )

if df.empty:
    st.warning("No data found.")
    st.stop()

# ── Chart ─────────────────────────────────────────────────────────────────────
chart_data = df[df["Month"] != "TOTAL"]
with st.container(border=True):
    st.markdown("**Monthly Enquiries & Conversion Rate**")
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
