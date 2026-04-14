"""
KPI metric cards based on UI-DESIGN-INSTRUCTION.md.
Uses st.metric with tinted backgrounds per type:
- Volume metrics → Blue tint (#E6F1FB)
- Rate/count metrics → Green tint (#EAF3DE)  
- Currency metrics → Amber tint (#FAEEDA)
"""

import streamlit as st
from utils.formatters import format_inr, format_pct, format_count


def render_kpi_row(kpis: dict):
    """Render modern KPI cards with accent strips and delta arrows."""
    total_enq = int(kpis.get("total_enquiries", 0) or 0)
    total_conv = int(kpis.get("total_converted", 0) or 0)
    conv_rate = float(kpis.get("overall_conversion_rate", 0.0) or 0.0)
    premium = float(kpis.get("total_premium_converted", 0.0) or 0.0)
    brokerage = float(kpis.get("total_brokerage_converted", 0.0) or 0.0)

    conv_share = round((total_conv / total_enq) * 100, 1) if total_enq else 0.0
    benchmark_rate = 75.0
    rate_delta = round(conv_rate - benchmark_rate, 1)
    total_value = premium + brokerage
    premium_share = round((premium / total_value) * 100, 1) if total_value else 0.0
    brokerage_share = round((brokerage / total_value) * 100, 1) if total_value else 0.0

    cards = [
        ("Total enquiries", format_count(total_enq), "Blue", "Volume", "kpi-tone-blue", None, False),
        ("Total converted", format_count(total_conv), "Green", "Count", "kpi-tone-green", f"{conv_share}% of enquiries", True),
        ("Conversion rate", format_pct(conv_rate), "Green", "Rate", "kpi-tone-green", f"{abs(rate_delta):.1f} pp vs 75% benchmark", rate_delta >= 0),
        ("Premium converted", format_inr(premium, short=True), "Amber", "Value", "kpi-tone-amber", f"{premium_share}% share", True),
        ("Brokerage converted", format_inr(brokerage, short=True), "Amber", "Value", "kpi-tone-amber", f"{brokerage_share}% share", True),
    ]

    cols = st.columns(5)
    for col, (label, value, pill, sublabel, tone, delta_text, positive) in zip(cols, cards):
        with col:
            delta_html = ""
            if delta_text:
                arrow = "↑" if positive else "↓"
                delta_cls = "kpi-delta-up" if positive else "kpi-delta-down"
                delta_html = f'<div class="kpi-delta {delta_cls}">{arrow} {delta_text}</div>'

            st.markdown(
                f"""
                <div class="kpi-card {tone}">
                    <div class="kpi-head">
                        <span class="kpi-label">{label}</span>
                        <span class="kpi-pill">{pill}</span>
                    </div>
                    <div class="kpi-value">{value}</div>
                    <div class="kpi-sub">{sublabel}</div>
                    {delta_html}
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_funnel_kpi_row(total: int, quoted: int, closed: int):
    """Render 3 funnel-stage KPI cards."""
    quote_pct  = round(quoted / total * 100, 1) if total else 0.0
    closed_pct = round(closed / total * 100, 1) if total else 0.0
    
    col1, col2, col3 = st.columns(3)
    
    # Card 1 - Total Enquiries (Blue tint)
    with col1:
        st.markdown('<div class="kpi-blue" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Total enquiries", format_count(total))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 2 - Quote Submitted (Amber tint - revenue indicator)
    with col2:
        st.markdown('<div class="kpi-amber" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Quote Submitted", f"{quoted} ({quote_pct}%)")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 3 - Business Closed (Green tint - positive)
    with col3:
        st.markdown('<div class="kpi-green" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Business Closed", f"{closed} ({closed_pct}%)")
        st.markdown('</div>', unsafe_allow_html=True)
