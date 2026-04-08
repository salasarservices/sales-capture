"""
Tab C — Business Conversion Ratio
Monthly enquiry count and conversion rate for FY 2025-26.
"""

import streamlit as st

st.set_page_config(page_title="Business Conversion Ratio", layout="wide")

from utils.auth import require_auth, is_admin
from database.connection import get_db
from database.queries import fetch_business_conversion
from components.charts import dual_axis_monthly
from components.data_tables import export_csv_button, highlight_conversion_row
from utils.formatters import format_pct

require_auth()

st.title("📅 Business Conversion Ratio")
st.caption("Monthly enquiry volume and conversion rate — FY 2025-26")

db = get_db()

with st.spinner("Loading monthly data…"):
    df = fetch_business_conversion(db)

if df.empty:
    st.warning("No data found.")
    st.stop()

# ---- Chart ----
chart_data = df[df["Month"] != "TOTAL"]
st.plotly_chart(dual_axis_monthly(chart_data), use_container_width=True)

st.divider()

# ---- Table ----
st.subheader("Monthly Conversion Table")
st.caption(
    ":red[Red] = conversion < 50% &nbsp;|&nbsp; "
    ":orange[Amber] = conversion < 70% &nbsp;|&nbsp; "
    "**TOTAL** row = full FY aggregate"
)

display_df = df.copy()
display_df["Conversion %"] = display_df["Conversion %"].apply(
    lambda x: format_pct(x) if x != "TOTAL" else format_pct(x)
)

# Use styled dataframe with conditional row colours
styled = highlight_conversion_row(df, conv_col="Conversion %")
st.dataframe(styled, use_container_width=True, height=500, hide_index=True)

if is_admin():
    export_csv_button(df, filename="business_conversion.csv")
