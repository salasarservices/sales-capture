"""
Tab D — Master Data
"""

import streamlit as st

st.set_page_config(page_title="Master Data", layout="wide")

from utils.styles import inject_global_css
from utils.auth import require_auth
from components.sidebar import render_sidebar, render_header

require_auth()
inject_global_css()
render_sidebar()
render_header()

st.markdown(
    """
    <h1>🗂️ Master Data</h1>
    <p class="page-subtitle">Source master records for the active fiscal period.</p>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div style="
        display:inline-block;
        padding:0.35rem 0.72rem;
        border-radius:999px;
        background:#FFF7E8;
        border:1px solid #FBD38D;
        color:#9A5B00;
        font-weight:600;
        font-size:0.78rem;
    ">
        APR 25 to MAR 26
    </div>
    """,
    unsafe_allow_html=True,
)

st.info("Master data view scaffolded. We can plug in table modules next.")
