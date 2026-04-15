"""
KPI cards — pure native Streamlit st.metric() widgets, zero custom CSS.
"""

import streamlit as st
from utils.formatters import format_inr, format_pct, format_count


def render_kpi_row(kpis: dict) -> None:
    """Render 5 KPI metrics in a single row."""
    total_enq  = kpis.get("total_enquiries", 0)
    total_conv = kpis.get("total_converted", 0)
    conv_rate  = kpis.get("overall_conversion_rate", 0.0)
    premium    = kpis.get("total_premium_converted", 0.0)
    brokerage  = kpis.get("total_brokerage_converted", 0.0)

    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("📋 Total Enquiries",    format_count(total_enq))
    c2.metric("✅ Total Converted",    format_count(total_conv))
    c3.metric("📈 Conversion Rate",    format_pct(conv_rate))
    c4.metric("₹ Premium Converted",  format_inr(premium, short=True))
    c5.metric("💼 Brokerage Converted", format_inr(brokerage, short=True))


def render_funnel_kpi_row(total: int, quoted: int, closed: int) -> None:
    """Render 3 funnel-stage KPI metrics."""
    quote_pct  = round(quoted / total * 100, 1) if total else 0.0
    closed_pct = round(closed / total * 100, 1) if total else 0.0

    c1, c2, c3 = st.columns(3)
    c1.metric("📋 Total Enquiries", format_count(total))
    c2.metric("📝 Quote Submitted", f"{format_count(quoted)} ({quote_pct}%)")
    c3.metric("🏆 Business Closed", f"{format_count(closed)} ({closed_pct}%)")
