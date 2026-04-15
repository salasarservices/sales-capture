"""
Preline-style KPI stat cards — styled with Tailwind CSS utility classes.

Color coding:
  blue  → volume / count metrics   (navy  #185FA5)
  green → rate / conversion metrics (#1D9E75)
  amber → currency / revenue metrics (#EF9F27)

Card anatomy (Tailwind):
  • White bg, gray-200 border, rounded-xl, subtle shadow
  • 3 px top accent bar via absolute div (brand color, arbitrary value)
  • Header row: uppercase label left, icon badge right
  • Icon badge: colored bg square (arbitrary value), rounded-lg
  • Value: large semibold text in brand color (arbitrary value)

The grid containers use `grid grid-cols-5` / `grid grid-cols-3` with `gap-3`.
Tailwind Play CDN picks up all classes via its DOM MutationObserver.
"""

import streamlit as st
from utils.formatters import format_inr, format_pct, format_count

# ── Brand token maps (arbitrary Tailwind values) ─────────────────────────────
_TOP_BAR = {"blue": "#185FA5", "green": "#1D9E75", "amber": "#EF9F27"}
_ICON_BG  = {"blue": "#E6F1FB", "green": "#EAF3DE", "amber": "#FAEEDA"}
_VAL_COL  = {"blue": "#0C447C", "green": "#27500A", "amber": "#633806"}


def _card(color: str, icon: str, label: str, value: str) -> str:
    """Return HTML for one stat card using Tailwind utility classes."""
    top  = _TOP_BAR.get(color, "#185FA5")
    ibg  = _ICON_BG.get(color,  "#E6F1FB")
    vcol = _VAL_COL.get(color,  "#0C447C")
    return (
        '<div class="bg-white border border-gray-200 rounded-xl p-4 shadow-sm relative overflow-hidden">'
            # 3 px colored top accent bar — position/height not in Tailwind defaults
            f'<div style="position:absolute;top:0;left:0;right:0;height:3px;background:{top};border-radius:12px 12px 0 0;"></div>'
            # Header: label + icon badge
            '<div class="flex justify-between items-start mb-2.5">'
                f'<p class="text-[10.5px] uppercase tracking-[0.07em] font-bold text-gray-500 leading-snug m-0">{label}</p>'
                f'<span class="w-8 h-8 rounded-lg flex items-center justify-center text-[15px] flex-shrink-0" style="background:{ibg};">{icon}</span>'
            '</div>'
            # Value
            f'<p class="text-[1.45rem] font-semibold leading-tight m-0" style="color:{vcol};">{value}</p>'
        '</div>'
    )


def render_kpi_row(kpis: dict) -> None:
    """Render 5 KPI stat cards in a responsive 5-column grid."""
    total_enq  = kpis.get("total_enquiries", 0)
    total_conv = kpis.get("total_converted", 0)
    conv_rate  = kpis.get("overall_conversion_rate", 0.0)
    premium    = kpis.get("total_premium_converted", 0.0)
    brokerage  = kpis.get("total_brokerage_converted", 0.0)

    cards = (
        _card("blue",  "📋", "Total Enquiries",      format_count(total_enq))
        + _card("green", "✅", "Total Converted",    format_count(total_conv))
        + _card("green", "📈", "Conversion Rate",    format_pct(conv_rate))
        + _card("amber", "₹",  "Premium Converted",  format_inr(premium, short=True))
        + _card("amber", "💼", "Brokerage Converted", format_inr(brokerage, short=True))
    )

    st.markdown(
        f'<div class="grid grid-cols-5 gap-3 my-2">{cards}</div>',
        unsafe_allow_html=True,
    )


def render_funnel_kpi_row(total: int, quoted: int, closed: int) -> None:
    """Render 3 funnel-stage KPI cards in a 3-column grid."""
    quote_pct  = round(quoted / total * 100, 1) if total else 0.0
    closed_pct = round(closed / total * 100, 1) if total else 0.0

    cards = (
        _card("blue",  "📋", "Total Enquiries", format_count(total))
        + _card("amber", "📝", "Quote Submitted",
                f"{format_count(quoted)}"
                f"<span class='text-[0.85rem] font-medium opacity-70 ml-1'>({quote_pct}%)</span>")
        + _card("green", "🏆", "Business Closed",
                f"{format_count(closed)}"
                f"<span class='text-[0.85rem] font-medium opacity-70 ml-1'>({closed_pct}%)</span>")
    )

    st.markdown(
        f'<div class="grid grid-cols-3 gap-3 my-2">{cards}</div>',
        unsafe_allow_html=True,
    )
