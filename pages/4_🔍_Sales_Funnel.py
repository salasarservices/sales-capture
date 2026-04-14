"""
Tab D — Sales Funnel & Enquiry Capture
Funnel visualisation + filterable, paginated enquiry detail table.
"""

import streamlit as st

st.set_page_config(page_title="Sales Funnel", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth, is_admin, render_sidebar_branding
from database.connection import get_db
from database.queries import fetch_funnel_metrics, fetch_enquiries, fetch_filter_options
from components.charts import funnel_chart
from components.kpi_cards import render_funnel_kpi_row
from components.data_tables import render_enquiry_table, export_csv_button
from utils.fiscal_month import all_fiscal_labels, month_label_to_int
from utils.formatters import format_inr

require_auth()
inject_global_css()
render_sidebar_branding()

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(
    """
    <h1>🔍 Sales Funnel &amp; Enquiry Capture</h1>
    <p class="page-subtitle">Filter and explore the full enquiry pipeline</p>
    """,
    unsafe_allow_html=True,
)

db = get_db()

# ── Filter options ────────────────────────────────────────────────────────────
with st.spinner("Loading filter options…"):
    opts = fetch_filter_options(db)

# ── Filter bar ────────────────────────────────────────────────────────────────
with st.expander("🔽  Filters", expanded=True):
    fcol1, fcol2, fcol3, fcol4, fcol5 = st.columns(5)
    with fcol1:
        selected_months = st.multiselect("Month", options=all_fiscal_labels(), placeholder="All months")
    with fcol2:
        selected_cre    = st.multiselect("CRE / RM", options=opts["cre_rms"], placeholder="All")
    with fcol3:
        selected_types  = st.multiselect("Proposal Type", options=opts["proposal_types"], placeholder="All")
    with fcol4:
        selected_req    = st.multiselect("Product / Requirement", options=opts["requirements"], placeholder="All")
    with fcol5:
        company_search  = st.text_input("Search Company", placeholder="Type to search…")

month_ints = [month_label_to_int(m) for m in selected_months] if selected_months else None

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

# ── Funnel metrics ────────────────────────────────────────────────────────────
with st.spinner("Loading funnel…"):
    funnel = fetch_funnel_metrics(db, extra_match=extra_match if extra_match else None)

total  = funnel.get("total_enquiries", 0)
quoted = funnel.get("quote_submitted", 0)
closed = funnel.get("business_closed", 0)

# ── KPI cards ─────────────────────────────────────────────────────────────────
render_funnel_kpi_row(total, quoted, closed)
st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

# ── Funnel chart + drop-off analysis ──────────────────────────────────────────
fcol_l, fcol_r = st.columns([2, 3])
with fcol_l:
    st.plotly_chart(funnel_chart(total, quoted, closed), use_container_width=True)

with fcol_r:
    st.markdown('<p class="section-heading">Pipeline Drop-off Analysis</p>', unsafe_allow_html=True)
    if total and quoted:
        drop1     = total - quoted
        drop2     = quoted - closed if quoted else 0
        pct_drop1 = round(drop1 / total  * 100, 1)
        pct_drop2 = round(drop2 / quoted * 100, 1) if quoted else 0
        st.markdown(
            f"""
            <div class="hs-dropoff-stack">
                <div class="hs-dropoff-card hs-dropoff-red">
                    <div class="hs-dropoff-tag">Enquiry → Quote Drop-off</div>
                    <div class="hs-dropoff-value">
                        {drop1}
                        <span class="hs-dropoff-pct">({pct_drop1}%)</span>
                    </div>
                    <div class="hs-dropoff-sub">enquiries did not receive a quote</div>
                </div>
                <div class="hs-dropoff-card hs-dropoff-amber">
                    <div class="hs-dropoff-tag">Quote → Closed Drop-off</div>
                    <div class="hs-dropoff-value">
                        {drop2}
                        <span class="hs-dropoff-pct">({pct_drop2}%)</span>
                    </div>
                    <div class="hs-dropoff-sub">quoted enquiries did not close</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.info("No data to display drop-off analysis.")

st.divider()

# ── Enquiry detail table ──────────────────────────────────────────────────────
st.markdown('<p class="section-heading">Enquiry Detail</p>', unsafe_allow_html=True)

PAGE_SIZE = 100
if "funnel_page" not in st.session_state:
    st.session_state.funnel_page = 1

filter_key = str((selected_months, selected_cre, selected_types, selected_req, company_search))
if st.session_state.get("_last_filter") != filter_key:
    st.session_state.funnel_page = 1
    st.session_state["_last_filter"] = filter_key

with st.spinner("Loading enquiries…"):
    df, total_rows = fetch_enquiries(
        db,
        months=month_ints,
        cre_rms=selected_cre    if selected_cre    else None,
        proposal_types=selected_types if selected_types else None,
        requirements=selected_req   if selected_req   else None,
        company_search=company_search,
        page=st.session_state.funnel_page,
        page_size=PAGE_SIZE,
    )

total_pages = max(1, -(-total_rows // PAGE_SIZE))

if df.empty:
    st.info("No records found for selected filters.")
else:
    # Format currency columns before rendering
    display_df = df.copy()
    for col in ["Premium Potential", "Tentative Brokerage (12%)"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(format_inr)

    render_enquiry_table(display_df, height=600)

    # ── Pagination ────────────────────────────────────────────────────────
    pcol1, pcol2, pcol3 = st.columns([1, 4, 1])
    with pcol1:
        if st.button("← Prev", disabled=st.session_state.funnel_page <= 1):
            st.session_state.funnel_page -= 1
            st.rerun()
    with pcol2:
        st.caption(
            f"Page **{st.session_state.funnel_page}** of **{total_pages}** "
            f"&nbsp;·&nbsp; {total_rows:,} records total"
        )
    with pcol3:
        if st.button("Next →", disabled=st.session_state.funnel_page >= total_pages):
            st.session_state.funnel_page += 1
            st.rerun()

    if is_admin():
        st.caption("Export downloads current page only. Remove filters for full export.")
        export_csv_button(df, filename="enquiries_export.csv")