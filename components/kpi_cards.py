"""
KPI card row using st.metric.
KPI cards with a cleaner dashboard presentation.
"""

import streamlit as st
from utils.formatters import format_inr, format_pct, format_count


def _kpi_card(label: str, value: str):
    st.markdown(
        f"""
        <div class="salasar-kpi-card">
            <div class="salasar-kpi-label">{label}</div>
            <div class="salasar-kpi-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_row(kpis: dict):
    """Render 5 KPI cards in a single row."""
    total_enq = kpis.get("total_enquiries", 0)
    total_conv = kpis.get("total_converted", 0)
    conv_rate = kpis.get("overall_conversion_rate", 0.0)
    premium = kpis.get("total_premium_converted", 0.0)
    brokerage = kpis.get("total_brokerage_converted", 0.0)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Enquiries (FY)", format_count(total_enq))
        _kpi_card("Total Enquiries (FY)", format_count(total_enq))
    with col2:
        st.metric("Total Converted", format_count(total_conv))
        _kpi_card("Total Converted", format_count(total_conv))
    with col3:
        st.metric("Conversion Rate", format_pct(conv_rate))
        _kpi_card("Conversion Rate", format_pct(conv_rate))
    with col4:
        st.metric("Premium Converted", format_inr(premium, short=True))
        _kpi_card("Premium Converted", format_inr(premium, short=True))
    with col5:
        st.metric("Brokerage Converted", format_inr(brokerage, short=True))
        _kpi_card("Brokerage Converted", format_inr(brokerage, short=True))
