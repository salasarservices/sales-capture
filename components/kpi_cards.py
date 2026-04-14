"""
Preline-style KPI stat cards.

Renders a single st.markdown block per row — a CSS grid of self-contained
HTML cards with a colored top bar, uppercase label, icon badge, and value.

Color coding:
  blue  → volume / count metrics   (navy #185FA5)
  green → rate / conversion metrics (#1D9E75)
  amber → currency / revenue metrics (#EF9F27)
"""

import streamlit as st
from utils.formatters import format_inr, format_pct, format_count


def _card(color: str, icon: str, label: str, value: str) -> str:
    """Return HTML for one stat card."""
    return f"""
    <div class="hs-kpi-card hs-kpi-{color}">
        <div class="hs-kpi-header">
            <p class="hs-kpi-label">{label}</p>
            <span class="hs-kpi-icon hs-kpi-icon-{color}">{icon}</span>
        </div>
        <p class="hs-kpi-value">{value}</p>
    </div>"""


def render_kpi_row(kpis: dict) -> None:
    """Render 5 KPI stat cards in a single row."""
    total_enq  = kpis.get("total_enquiries", 0)
    total_conv = kpis.get("total_converted", 0)
    conv_rate  = kpis.get("overall_conversion_rate", 0.0)
    premium    = kpis.get("total_premium_converted", 0.0)
    brokerage  = kpis.get("total_brokerage_converted", 0.0)

    cards = (
        _card("blue",  "📋", "Total Enquiries",    format_count(total_enq))
        + _card("green", "✅", "Total Converted",   format_count(total_conv))
        + _card("green", "📈", "Conversion Rate",   format_pct(conv_rate))
        + _card("amber", "₹",  "Premium Converted", format_inr(premium, short=True))
        + _card("amber", "💼", "Brokerage Converted", format_inr(brokerage, short=True))
    )

    st.markdown(
        f'<div class="hs-kpi-grid hs-kpi-grid-5">{cards}</div>',
        unsafe_allow_html=True,
    )


def render_funnel_kpi_row(total: int, quoted: int, closed: int) -> None:
    """Render 3 funnel-stage KPI cards."""
    quote_pct  = round(quoted / total * 100, 1) if total else 0.0
    closed_pct = round(closed / total * 100, 1) if total else 0.0

    cards = (
        _card("blue",  "📋", "Total Enquiries",  format_count(total))
        + _card("amber", "📝", "Quote Submitted",
                f"{format_count(quoted)} <span style='font-size:0.85rem;font-weight:500;opacity:0.7'>({quote_pct}%)</span>")
        + _card("green", "🏆", "Business Closed",
                f"{format_count(closed)} <span style='font-size:0.85rem;font-weight:500;opacity:0.7'>({closed_pct}%)</span>")
    )

    st.markdown(
        f'<div class="hs-kpi-grid hs-kpi-grid-3">{cards}</div>',
        unsafe_allow_html=True,
    )
