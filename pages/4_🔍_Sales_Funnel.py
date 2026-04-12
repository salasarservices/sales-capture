"""
Tab D — Sales Funnel & Enquiry Capture
Funnel visualisation + filterable, paginated enquiry detail table.
"""

import streamlit as st

st.set_page_config(page_title="Sales Funnel", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth, is_admin
from database.connection import get_db
from database.queries import fetch_funnel_metrics, fetch_enquiries
from components.charts import funnel_chart
from components.kpi_cards import render_funnel_kpi_row
from components.data_tables import render_enquiry_table, export_csv_button
from components.sidebar import render_sidebar, render_header, get_active_filters
from utils.formatters import format_inr

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
    <h1>🔍 Sales Funnel &amp; Enquiry Capture</h1>
    <p class="page-subtitle">Filter and explore the full enquiry pipeline</p>
    """,
    unsafe_allow_html=True,
)

db = get_db()

company_search = st.text_input("Search Company", placeholder="Filter by company name…")
extra_match: dict = {
    "$expr": {"$in": [{"$month": "$date_referred"}, month_ints]},
}
if filters["cre_rms"]:
    extra_match["cre_rm_accountable"] = {"$in": filters["cre_rms"]}
if filters["proposal_types"]:
    extra_match["type_of_proposal"] = {"$in": filters["proposal_types"]}
if filters["requirements"]:
    extra_match["requirement"] = {"$in": filters["requirements"]}
if company_search.strip():
    import re
    extra_match["company_name"] = {"$regex": re.escape(company_search.strip()), "$options": "i"}

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
    with st.container(border=True):
        st.markdown("**Sales Funnel**")
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
            <div style="display:flex; flex-direction:column; gap:0.75rem; margin-top:0.5rem;">
                <div style="background:#FEF2F2; border-left:4px solid #B91C1C;
                            padding:1rem 1.25rem;">
                    <div style="font-size:0.68rem; font-weight:700; color:#B91C1C;
                                text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.3rem;">
                        Enquiry → Quote Drop-off
                    </div>
                    <div style="font-size:1.4rem; font-weight:700; color:#1E293B;">
                        {drop1}
                        <span style="font-size:0.9rem; color:#B91C1C;">({pct_drop1}%)</span>
                    </div>
                    <div style="font-size:0.80rem; color:#64748B; margin-top:0.2rem;">
                        enquiries did not receive a quote
                    </div>
                </div>
                <div style="background:#FFFBEB; border-left:4px solid #D97706;
                            padding:1rem 1.25rem;">
                    <div style="font-size:0.68rem; font-weight:700; color:#D97706;
                                text-transform:uppercase; letter-spacing:0.5px; margin-bottom:0.3rem;">
                        Quote → Closed Drop-off
                    </div>
                    <div style="font-size:1.4rem; font-weight:700; color:#1E293B;">
                        {drop2}
                        <span style="font-size:0.9rem; color:#D97706;">({pct_drop2}%)</span>
                    </div>
                    <div style="font-size:0.80rem; color:#64748B; margin-top:0.2rem;">
                        quoted enquiries did not close
                    </div>
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

filter_key = str((filters["months"], filters["cre_rms"], filters["proposal_types"], filters["requirements"], company_search))
if st.session_state.get("_last_filter") != filter_key:
    st.session_state.funnel_page = 1
    st.session_state["_last_filter"] = filter_key

with st.spinner("Loading enquiries…"):
    df, total_rows = fetch_enquiries(
        db,
        fy=filters["fy"],
        branch=filters["branch"],
        months=month_ints,
        cre_rms=filters["cre_rms"] if filters["cre_rms"] else None,
        proposal_types=filters["proposal_types"] if filters["proposal_types"] else None,
        requirements=filters["requirements"] if filters["requirements"] else None,
        company_search=company_search.strip(),
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
