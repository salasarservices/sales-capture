"""
Plotly chart builders for the Salasar dashboard.
- Subtle plot background (not stark white)
- Transparent paper background (card CSS provides container colour)
- X-axis labels rotated -30° with automargin to prevent overlap
- No rounded corners (handled by CSS)
"""

import plotly.graph_objects as go
import pandas as pd

# ── Brand palette ─────────────────────────────────────────────────────────────
COLOR_CONVERTED     = "#15803D"
COLOR_NOT_CONVERTED = "#B91C1C"
COLOR_NAVY          = "#1B3A6B"
COLOR_NAVY_LT       = "#2D5FA8"
COLOR_GOLD          = "#C8860A"
COLOR_AMBER         = "#D97706"
COLOR_BLUE          = "#2563EB"
COLOR_PURPLE        = "#7C3AED"
COLOR_TEAL          = "#0D9488"

# Base layout dict — no margin (added per-chart via _DEFAULT_MARGIN or override)
_LAYOUT_BASE = dict(
    font=dict(family="Inter, -apple-system, sans-serif", size=12, color="#1E293B"),
    plot_bgcolor="rgba(247, 249, 252, 1)",   # very subtle blue-gray — NOT white
    paper_bgcolor="rgba(0, 0, 0, 0)",         # transparent; CSS card provides white bg
    hoverlabel=dict(
        bgcolor="#1B3A6B",
        font_color="#FFFFFF",
        bordercolor="#1B3A6B",
        font_size=12,
    ),
)

_DEFAULT_MARGIN = dict(t=48, b=90, l=20, r=20)   # extra bottom for rotated labels


def _apply_base(fig: go.Figure, **extra) -> go.Figure:
    """Apply consistent layout + axis styling. `extra` overrides any base key."""
    layout = {**_LAYOUT_BASE, "margin": _DEFAULT_MARGIN, **extra}
    fig.update_layout(**layout)
    fig.update_xaxes(
        showgrid=False,
        zeroline=False,
        tickangle=-30,          # rotate labels to prevent overlap
        automargin=True,        # auto-expand margin when labels overflow
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#64748B"),
    )
    fig.update_yaxes(
        gridcolor="#E8EDF4",
        gridwidth=1,
        zeroline=False,
        tickfont=dict(size=11, color="#64748B"),
        title_font=dict(size=12, color="#64748B"),
    )
    return fig


# ── Tab A — Stacked Bar: Converted vs Not Converted per CRE/RM ───────────────

def stacked_bar_conversion(df: pd.DataFrame) -> go.Figure:
    data = df[df["CRE / RM"] != "TOTAL"].copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Converted",
        x=data["CRE / RM"],
        y=data["Converted"],
        marker=dict(color=COLOR_CONVERTED, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Converted: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Not Converted",
        x=data["CRE / RM"],
        y=data["Not Converted"],
        marker=dict(color=COLOR_NOT_CONVERTED, line=dict(width=0)),
        hovertemplate="<b>%{x}</b><br>Not Converted: %{y}<extra></extra>",
    ))
    return _apply_base(
        fig,
        barmode="stack",
        title=dict(text="Converted vs Not Converted by CRE/RM",
                   font=dict(size=14, color=COLOR_NAVY, weight="bold")),
        xaxis_title="CRE / RM",
        yaxis_title="No. of Enquiries",
        legend=dict(orientation="h", yanchor="bottom", y=-0.38,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        bargap=0.35,
    )


# ── Tab A — Grouped Bar: Fresh / Renewal / Expanded per CRE/RM ───────────────

def grouped_bar_proposal_type(df: pd.DataFrame) -> go.Figure:
    data = df[df["CRE / RM"] != "TOTAL"].copy()
    fig = go.Figure()
    specs = [
        ("Fresh",    "fresh_converted",    COLOR_BLUE),
        ("Renewal",  "renewal_converted",  COLOR_PURPLE),
        ("Expanded", "expanded_converted", COLOR_GOLD),
    ]
    for label, col, color in specs:
        if col in data.columns:
            fig.add_trace(go.Bar(
                name=label,
                x=data["CRE / RM"],
                y=data[col],
                marker=dict(color=color, line=dict(width=0)),
                hovertemplate=f"<b>%{{x}}</b><br>{label}: %{{y}}<extra></extra>",
            ))
    return _apply_base(
        fig,
        barmode="group",
        title=dict(text="Converted by Proposal Type per CRE/RM",
                   font=dict(size=14, color=COLOR_NAVY, weight="bold")),
        xaxis_title="CRE / RM",
        yaxis_title="Converted",
        legend=dict(orientation="h", yanchor="bottom", y=-0.38,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        bargap=0.28, bargroupgap=0.06,
    )


# ── Tab B — Horizontal Bar: Premium Converted per CRE/RM ─────────────────────

def horizontal_bar_premium(df: pd.DataFrame) -> go.Figure:
    data = df[df["CRE / RM"] != "TOTAL"].copy().sort_values("Premium Converted (₹)")
    conv_rates = 100 - data["% Not Converted"]
    fig = go.Figure(go.Bar(
        x=data["Premium Converted (₹)"],
        y=data["CRE / RM"],
        orientation="h",
        marker=dict(
            color=conv_rates,
            colorscale=[
                [0.0, COLOR_NOT_CONVERTED],
                [0.5, COLOR_AMBER],
                [1.0, COLOR_CONVERTED],
            ],
            showscale=True,
            colorbar=dict(
                title=dict(text="Conv %", font=dict(size=10)),
                thickness=12,
                tickfont=dict(size=10),
                outlinewidth=0,
            ),
            line=dict(width=0),
        ),
        hovertemplate="<b>%{y}</b><br>Premium: ₹%{x:,.0f}<extra></extra>",
    ))
    # Horizontal bar — no x-axis label rotation needed; override tickangle
    _apply_base(
        fig,
        title=dict(text="Premium Converted by CRE/RM",
                   font=dict(size=14, color=COLOR_NAVY, weight="bold")),
        xaxis_title="Total Premium (₹)",
        yaxis_title="",
        margin=dict(t=48, b=40, l=170, r=20),
    )
    fig.update_xaxes(tickangle=0)   # horizontal bar — numeric axis, no rotation
    return fig


# ── Tab B — Donut: Share of Enquiries per CRE/RM ─────────────────────────────

def pie_enquiry_share(df: pd.DataFrame) -> go.Figure:
    data = df[df["CRE / RM"] != "TOTAL"].copy()
    palette = [COLOR_NAVY, COLOR_BLUE, COLOR_TEAL, COLOR_GOLD,
               COLOR_PURPLE, COLOR_AMBER, "#0EA5E9", "#6366F1"]
    fig = go.Figure(go.Pie(
        labels=data["CRE / RM"],
        values=data["Total Enquiries"],
        hole=0.42,
        marker=dict(colors=palette[:len(data)],
                    line=dict(color="#FFFFFF", width=2)),
        hovertemplate="<b>%{label}</b><br>%{value} enquiries (%{percent})<extra></extra>",
        textinfo="percent",
        textfont=dict(size=11),
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        margin=dict(t=48, b=20, l=20, r=20),
        title=dict(text="Share of Enquiries by CRE/RM",
                   font=dict(size=14, color=COLOR_NAVY, weight="bold")),
        legend=dict(orientation="v", font=dict(size=11), bgcolor="rgba(0,0,0,0)"),
        annotations=[dict(
            text="Enquiries", x=0.5, y=0.5, showarrow=False,
            font=dict(size=12, color="#64748B"),
        )],
    )
    return fig


# ── Tab C — Dual-Axis: Bar (enquiries) + Line (conversion %) ─────────────────

def dual_axis_monthly(df: pd.DataFrame) -> go.Figure:
    data = df[df["Month"] != "TOTAL"].copy()
    avg_conv = data["Conversion %"].mean()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="No. of Enquiries",
        x=data["Month"],
        y=data["No. of Enquiries"],
        marker=dict(color=COLOR_NAVY, opacity=0.82, line=dict(width=0)),
        yaxis="y1",
        hovertemplate="<b>%{x}</b><br>Enquiries: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name="Conversion %",
        x=data["Month"],
        y=data["Conversion %"],
        mode="lines+markers",
        line=dict(color=COLOR_CONVERTED, width=2.5),
        marker=dict(size=7, color=COLOR_CONVERTED, line=dict(color="#FFFFFF", width=1.5)),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>Conversion: %{y:.1f}%<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name=f"Annual Avg ({avg_conv:.1f}%)",
        x=data["Month"],
        y=[avg_conv] * len(data),
        mode="lines",
        line=dict(color=COLOR_GOLD, width=1.5, dash="dash"),
        yaxis="y2",
        hoverinfo="skip",
    ))
    return _apply_base(
        fig,
        title=dict(text="Monthly Enquiries & Conversion Rate",
                   font=dict(size=14, color=COLOR_NAVY, weight="bold")),
        xaxis_title="Month",
        yaxis=dict(
            title="No. of Enquiries", side="left",
            showgrid=True, gridcolor="#E8EDF4",
            tickfont=dict(size=11, color="#64748B"),
            title_font=dict(size=12, color="#64748B"),
        ),
        yaxis2=dict(
            title="Conversion %", side="right", overlaying="y",
            tickformat=".1f", ticksuffix="%",
            showgrid=False,
            tickfont=dict(size=11, color="#64748B"),
            title_font=dict(size=12, color="#64748B"),
        ),
        legend=dict(orientation="h", yanchor="bottom", y=-0.38,
                    bgcolor="rgba(0,0,0,0)", font=dict(size=12)),
        bargap=0.35,
        margin=dict(t=48, b=100, l=20, r=20),
    )


# ── Tab D — Funnel Chart ──────────────────────────────────────────────────────

def funnel_chart(total: int, quoted: int, closed: int) -> go.Figure:
    fig = go.Figure(go.Funnel(
        y=["Total Enquiries", "Quote Submitted", "Business Closed"],
        x=[total, quoted, closed],
        textinfo="value+percent initial",
        textfont=dict(size=13, color="#FFFFFF"),
        marker=dict(
            color=[COLOR_NAVY, COLOR_GOLD, COLOR_CONVERTED],
            line=dict(color=["#FFFFFF"] * 3, width=1),
        ),
        connector=dict(line=dict(color="#D1D9E6", width=1)),
        hovertemplate=(
            "<b>%{label}</b><br>Count: %{value}<br>%{percentInitial} of total<extra></extra>"
        ),
    ))
    fig.update_layout(
        **_LAYOUT_BASE,
        title=dict(text="Sales Funnel",
                   font=dict(size=14, color=COLOR_NAVY, weight="bold")),
        margin=dict(t=48, b=20, l=20, r=20),
    )
    return fig
