"""
Master Data page - From April 25 to March 26.
"""

import streamlit as st


def render_page():
    """Render the Master Data page."""
    
    st.title("📋 Master Data")
    st.caption("Enquiry details from April 2025 to March 2026")
    
    # Load data
    from database.connection import get_db
    from database.queries import fetch_filter_options, fetch_enquiries
    
    db = get_db()
    fy = st.session_state.get("fy", "2025-26")
    branch = st.session_state.get("branch", "Ahmedabad")
    
    # Data currency note
    with st.expander("ℹ️ Data source note", expanded=False):
        st.markdown(
            """
Records shown here come from the MongoDB database, seeded from the source Excel file
(`Sales Funnel & Enquiry Capture(Apr25 To Mar26)`).

The source sheet contains **~408 rows** for FY 2025-26. If the total record count here
is significantly lower, the database needs to be re-seeded with the current Excel file:

```
python scripts/seed_from_excel.py \\
  --file "<path-to-xlsx>" \\
  --sheet "Sales Funnel & Enquiry Capture(Apr25 To Mar26)" \\
  --fy "2025-26" \\
  --branch "Ahmedabad"
```

The script is idempotent — it upserts by `enquiry_no`, so re-running it will not create duplicates.
            """,
            unsafe_allow_html=False,
        )

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
            selected_months = st.multiselect("Month", 
                ["Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan", "Feb", "Mar"],
                placeholder="All")
        with col5:
            company_search = st.text_input("Search Company", placeholder="Type to search...")
    
    # Map month labels to numbers
    month_map = {"Apr": 4, "May": 5, "Jun": 6, "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12, "Jan": 1, "Feb": 2, "Mar": 3}
    month_ints = [month_map[m] for m in selected_months] if selected_months else None
    
    # Pagination
    PAGE_SIZE = 50
    if "master_page" not in st.session_state:
        st.session_state.master_page = 1
    
    # Reset page on filter change
    filter_key = str((selected_cre, selected_types, selected_req, selected_months, company_search))
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
            page_size=PAGE_SIZE
        )
    
    total_pages = max(1, -(-total_rows // PAGE_SIZE))
    
    if df.empty:
        st.info("No records found for the selected filters.")
        return
    
    # Format currency columns
    from utils.formatters import format_inr
    for col in ["Premium Potential", "Tentative Brokerage (12%)"]:
        if col in df.columns:
            df[col] = df[col].apply(lambda x: format_inr(x) if pd.notna(x) else "")
    
    # Display table
    from components.data_tables import render_enquiry_table
    
    st.dataframe(df, width='stretch', height=500, hide_index=True)
    
    # Pagination
    col1, col2, col3 = st.columns([1, 4, 1])
    with col1:
        if st.button("← Previous", disabled=st.session_state.master_page <= 1):
            st.session_state.master_page -= 1
            st.rerun()
    with col2:
        st.caption(f"Page {st.session_state.master_page} of {total_pages} · {total_rows:,} records")
    with col3:
        if st.button("Next →", disabled=st.session_state.master_page >= total_pages):
            st.session_state.master_page += 1
            st.rerun()


import pandas as pd
