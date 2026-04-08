"""
Tab D — Sales Funnel & Enquiry Capture
Funnel visualisation + filterable, paginated enquiry detail table.
"""

import streamlit as st

st.set_page_config(page_title="Sales Funnel", layout="wide")

from utils.auth import require_auth, is_admin
from database.connection import get_db
from database.queries import fetch_funnel_metrics, fetch_enquiries, fetch_filter_options
from components.charts import funnel_chart
from components.data_tables import render_table, export_csv_button
from utils.fiscal_month import all_fiscal_labels, month_label_to_int
from utils.formatters import format_inr

require_auth()

st.title("🔍 Sales Funnel & Enquiry Capture")
st.caption("Filter and explore the full enquiry pipeline")

db = get_db()

# ---- Filter Options ----
with st.spinner("Loading filter options…"):
    opts = fetch_filter_options(db)

# ---- Filter Bar ----
with st.expander("Filters", expanded=True):
    fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    with fcol1:
        selected_months = st.multiselect(
            "Month", options=all_fiscal_labels(), placeholder="All months"
        )
    with fcol2:
        selected_cre = st.multiselect(
            "CRE / RM", options=opts["cre_rms"], placeholder="All"
        )
    with fcol3:
        selected_types = st.multiselect(
            "Proposal Type", options=opts["proposal_types"], placeholder="All"
        )
    with fcol4:
        selected_req = st.multiselect(
            "Product / Requirement", options=opts["requirements"], placeholder="All"
        )
    with fcol5:
        company_search = st.text_input("Search Company", placeholder="Type to search…")

# Convert month labels → month integers for MongoDB query
month_ints = [month_label_to_int(m) for m in selected_months] if selected_months else None

# Build extra_match for funnel metrics
extra_match: dict = {}
if month_ints:
    extra_match["$expr"] = {"$in": [{"$month": "$date_referred"}, month_ints]}
if selected_cre:
    extra_match["cre_rm_accountable"] = {"$in": selected_cre}
if selected_types:
    extra_match["type_of_proposal"] = {"$in": selected_types}
if selected_req:
    extra_match["requirement"] = {"$in": selected_req}
if company_search:
    import re
    extra_match["company_name"] = {"$regex": re.escape(company_search), "$options": "i"}

# ---- Funnel ----
with st.spinner("Loading funnel…"):
    funnel = fetch_funnel_metrics(db, extra_match=extra_match if extra_match else None)

total = funnel.get("total_enquiries", 0)
quoted = funnel.get("quote_submitted", 0)
closed = funnel.get("business_closed", 0)

fcol_l, fcol_r = st.columns([2, 3])
with fcol_l:
    st.plotly_chart(funnel_chart(total, quoted, closed), use_container_width=True)

with fcol_r:
    st.subheader("Funnel Summary")
    m1, m2, m3 = st.columns(3)
    m1.metric("Total Enquiries", total)
    m2.metric(
        "Quote Submitted",
        quoted,
        delta=f"{round(quoted/total*100,1)}% of total" if total else "—",
    )
    m3.metric(
        "Business Closed",
        closed,
        delta=f"{round(closed/total*100,1)}% of total" if total else "—",
    )

    if total and quoted:
        drop1 = total - quoted
        drop2 = quoted - closed if quoted else 0
        st.caption(
            f"Drop-off: Enquiry → Quote: **{drop1}** ({round(drop1/total*100,1)}%)  |  "
            f"Quote → Closed: **{drop2}** ({round(drop2/quoted*100,1) if quoted else 0}%)"
        )

st.divider()

# ---- Enquiry Detail Table ----
st.subheader("Enquiry Detail")

PAGE_SIZE = 25
if "funnel_page" not in st.session_state:
    st.session_state.funnel_page = 1

# Reset to page 1 on filter change
filter_key = str((selected_months, selected_cre, selected_types, selected_req, company_search))
if st.session_state.get("_last_filter") != filter_key:
    st.session_state.funnel_page = 1
    st.session_state["_last_filter"] = filter_key

with st.spinner("Loading enquiries…"):
    df, total_rows = fetch_enquiries(
        db,
        months=month_ints,
        cre_rms=selected_cre if selected_cre else None,
        proposal_types=selected_types if selected_types else None,
        requirements=selected_req if selected_req else None,
        company_search=company_search,
        page=st.session_state.funnel_page,
        page_size=PAGE_SIZE,
    )

total_pages = max(1, -(-total_rows // PAGE_SIZE))  # ceiling division

if df.empty:
    st.info("No records found for selected filters.")
else:
    # Format currency columns for display
    display_df = df.copy()
    for col in ["Premium Potential", "Tentative Brokerage (12%)"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(format_inr)

    render_table(display_df, height=500, key="funnel_table")

    # Pagination controls
    pcol1, pcol2, pcol3 = st.columns([1, 3, 1])
    with pcol1:
        if st.button("← Prev", disabled=st.session_state.funnel_page <= 1):
            st.session_state.funnel_page -= 1
            st.rerun()
    with pcol2:
        st.caption(
            f"Page {st.session_state.funnel_page} of {total_pages} "
            f"({total_rows} records total)"
        )
    with pcol3:
        if st.button("Next →", disabled=st.session_state.funnel_page >= total_pages):
            st.session_state.funnel_page += 1
            st.rerun()

    if is_admin():
        st.caption("Export downloads current page only. For full export, remove all filters.")
        export_csv_button(df, filename="enquiries_export.csv")
