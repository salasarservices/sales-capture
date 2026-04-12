"""
Salasar Services — Sales Dashboard
Entry point: authentication gate.
"""

import streamlit as st

st.set_page_config(
    page_title="Salasar Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

from utils.auth import login_form

# ── Auth gate ────────────────────────────────────────────────────────────────
if not st.session_state.get("authenticated"):
    login_form()
    st.stop()

# Default post-login landing page
st.switch_page("pages/3_📅_Business_Conversion.py")
