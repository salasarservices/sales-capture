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
    """Render 5 KPI metric cards in a single row using st.metric."""
    total_enq  = kpis.get("total_enquiries", 0)
    total_conv = kpis.get("total_converted", 0)
    conv_rate  = kpis.get("overall_conversion_rate", 0.0)
    premium    = kpis.get("total_premium_converted", 0.0)
    brokerage  = kpis.get("total_brokerage_converted", 0.0)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    # Card 1 - Total Enquiries (Blue tint - volume)
    with col1:
        st.markdown('<div class="kpi-blue" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Total enquiries", format_count(total_enq))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 2 - Total Converted (Green tint - rate/count)
    with col2:
        st.markdown('<div class="kpi-green" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Total converted", format_count(total_conv))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 3 - Conversion Rate (Green tint - rate)
    with col3:
        st.markdown('<div class="kpi-green" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Conversion rate", format_pct(conv_rate))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 4 - Premium Converted (Amber tint - currency)
    with col4:
        st.markdown('<div class="kpi-amber" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Premium converted", format_inr(premium, short=True))
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Card 5 - Brokerage Converted (Amber tint - currency)
    with col5:
        st.markdown('<div class="kpi-amber" style="padding: 12px; border-radius: 8px;">', unsafe_allow_html=True)
        st.metric("Brokerage converted", format_inr(brokerage, short=True))
        st.markdown('</div>', unsafe_allow_html=True)


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