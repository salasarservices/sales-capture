"""
KPI card row — custom HTML cards with colored top-border accents and icons.
"""

import streamlit as st
from utils.formatters import format_inr, format_pct, format_count


def _card(label: str, value: str, icon: str, variant: str) -> str:
    return f"""
    <div class="kpi-card {variant}">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-content">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
        </div>
    </div>
    """


def render_kpi_row(kpis: dict):
    """Render 5 KPI metric cards in a single row."""
    total_enq  = kpis.get("total_enquiries", 0)
    total_conv = kpis.get("total_converted", 0)
    conv_rate  = kpis.get("overall_conversion_rate", 0.0)
    premium    = kpis.get("total_premium_converted", 0.0)
    brokerage  = kpis.get("total_brokerage_converted", 0.0)

    cards = [
        ("Total Enquiries (FY)", format_count(total_enq),          "📋", "navy"),
        ("Total Converted",      format_count(total_conv),          "✅", "green"),
        ("Conversion Rate",      format_pct(conv_rate),             "📈", "blue"),
        ("Premium Converted",    format_inr(premium, short=True),   "💰", "gold"),
        ("Brokerage Converted",  format_inr(brokerage, short=True), "💼", "purple"),
    ]

    cols = st.columns(5)
    for col, (label, value, icon, variant) in zip(cols, cards):
        with col:
            st.markdown(_card(label, value, icon, variant), unsafe_allow_html=True)


def render_funnel_kpi_row(total: int, quoted: int, closed: int):
    """Render 3 funnel-stage KPI cards for the Sales Funnel page."""
    quote_pct  = round(quoted / total * 100, 1) if total else 0.0
    closed_pct = round(closed / total * 100, 1) if total else 0.0

    cards = [
        ("Total Enquiries",  str(total),
         "🗂️", "navy"),
        ("Quote Submitted",  f"{quoted}  ({quote_pct}%)",
         "📄", "gold"),
        ("Business Closed",  f"{closed}  ({closed_pct}%)",
         "🏆", "green"),
    ]

    cols = st.columns(3)
    for col, (label, value, icon, variant) in zip(cols, cards):
        with col:
            st.markdown(_card(label, value, icon, variant), unsafe_allow_html=True)
