"""
Master Data page - From April 25 to March 26.
"""

import hashlib
import pandas as pd
import streamlit as st
import streamlit_shadcn_ui as ui


def render_page():
    """Render the Master Data page."""

    # Breadcrumb — page context
    ui.breadcrumb(
        [{"label": "Salasar Analytics", "href": None}, {"label": "Master Data", "href": None}],
        class_name="mb-2",
    )

    # Page header
    ui.element("h1", children=["📋 Master Data"],
               className="text-[22px] font-semibold text-gray-900 mt-0 mb-1 leading-tight")
    ui.element("p", children=["Enquiry details from April 2025 to March 2026"],
               className="text-sm text-gray-500 mt-0 mb-6")

    # Load data
    from database.connection import get_db
    from database.queries import fetch_filter_options, fetch_enquiries

    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")

    # Get filter options
    with st.spinner("Loading filters..."):
        opts = fetch_filter_options(db, fy=fy, branch=branch)

    # Filters
    with st.expander("🔽 Filters", expanded=True):
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            selected_cre = st.multiselect("CRE/RM", opts.get("cre_rms", []), placeholder="All")
        with col2:
            selected_types = st.multiselect("Proposal Type", opts.get("proposal_types", []), placeholder="All")
        with col3:
            selected_req = st.multiselect("Product", opts.get("requirements", []), placeholder="All")
        with col4:
            selected_months = st.multiselect(
                "Month",
                ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
                placeholder="All",
            )
        with col5:
            company_search = st.text_input("Search Company", placeholder="Type to search...")

    # Map month labels to numbers
    month_map = {
        "Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9,
        "Oct": 10, "Nov": 11, "Dec": 12, "Jan": 1, "Feb": 2, "Mar": 3,
    }
    month_ints = [month_map[m] for m in selected_months] if selected_months else None

    # Pagination state
    PAGE_SIZE = 50
    if "master_page" not in st.session_state:
        st.session_state.master_page = 1

    # Reset page when filters change; use filter hash as pagination key so
    # ui.pagination resets to page 1 automatically on filter change
    filter_key = str((selected_cre, selected_types, selected_req, selected_months, company_search))
    filter_hash = hashlib.md5(filter_key.encode()).hexdigest()[:8]
    if st.session_state.get("_last_master_filter") != filter_key:
        st.session_state.master_page = 1
        st.session_state["_last_master_filter"] = filter_key

    # Load data
    with st.spinner("Loading data..."):
        df, total_rows = fetch_enquiries(
            db,
            fy=fy,
            branch=branch,
            cre_rms=selected_cre if selected_cre else None,
            proposal_types=selected_types if selected_types else None,
            requirements=selected_req if selected_req else None,
            months=month_ints,
            company_search=company_search,
            page=st.session_state.master_page,
            page_size=PAGE_SIZE,
        )

    total_pages = max(1, -(-total_rows // PAGE_SIZE))

    if df.empty:
        ui.alert(
            title="No Records Found",
            description="No enquiry records match the selected filters. Try adjusting or clearing the filters.",
        )
        return

    # Format currency columns
    from utils.formatters import format_inr
    for col in ["Premium Potential", "Tentative Brokerage (12%)"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: format_inr(x) if pd.notna(x) else "")

    # Data table
    st.dataframe(df, width='stretch', height=500, hide_index=True)

    # ── Pagination ──────────────────────────────────────────────────────────────
    ui.element("div", className="h-4")  # spacer

    # Record count summary
    start_rec = (st.session_state.master_page - 1) * PAGE_SIZE + 1
    end_rec = min(st.session_state.master_page * PAGE_SIZE, total_rows)
    ui.element(
        "p",
        children=[f"Showing {start_rec:,}–{end_rec:,} of {total_rows:,} records  ·  Page {st.session_state.master_page} of {total_pages}"],
        className="text-xs text-gray-400 text-center mb-2 mt-0",
    )

    # shadcn pagination component — key changes with filter so it resets to page 1
    clicked_page = ui.pagination(
        key=f"pag_{filter_hash}",
        totalPages=total_pages,
        initialPage=st.session_state.master_page,
    )
    if clicked_page and clicked_page != st.session_state.master_page:
        st.session_state.master_page = clicked_page
        st.rerun()
