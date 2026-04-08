"""
Plotly chart builders for the Salasar dashboard.
Colors follow the spec design system.
"""

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

COLOR_CONVERTED = "#22C55E"
COLOR_NOT_CONVERTED = "#EF4444"
COLOR_NAVY = "#1E3A5F"
COLOR_AMBER = "#F59E0B"


# ---------------------------------------------------------------------------
# Tab A — Stacked Bar: Converted vs Not Converted per CRE/RM
# ---------------------------------------------------------------------------

def stacked_bar_conversion(df: pd.DataFrame) -> go.Figure:
    """
    Input df columns: CRE / RM, Converted, Not Converted
    Excludes TOTAL row.
    """
    data = df[df["CRE / RM"] != "TOTAL"].copy()
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Converted",
        x=data["CRE / RM"],
        y=data["Converted"],
        marker_color=COLOR_CONVERTED,
        hovertemplate="%{x}<br>Converted: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        name="Not Converted",
        x=data["CRE / RM"],
        y=data["Not Converted"],
        marker_color=COLOR_NOT_CONVERTED,
        hovertemplate="%{x}<br>Not Converted: %{y}<extra></extra>",
    ))
    fig.update_layout(
        barmode="stack",
        title="Converted vs Not Converted by CRE/RM",
        xaxis_title="CRE / RM",
        yaxis_title="Number of Enquiries",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        plot_bgcolor="white",
        margin=dict(t=50, b=80),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab A — Grouped Bar: Fresh / Renewal / Expanded per CRE/RM
# ---------------------------------------------------------------------------

def grouped_bar_proposal_type(df: pd.DataFrame) -> go.Figure:
    """
    Input df from summary_conversion_pipeline.
    Columns: CRE / RM, fresh_converted, renewal_converted, expanded_converted
    """
    data = df[df["CRE / RM"] != "TOTAL"].copy()
    fig = go.Figure()
    colors = {"Fresh": "#3B82F6", "Renewal": "#8B5CF6", "Expanded": "#F59E0B"}
    for ptype, col in [("Fresh", "fresh_converted"), ("Renewal", "renewal_converted"), ("Expanded", "expanded_converted")]:
        if col in data.columns:
            fig.add_trace(go.Bar(
                name=ptype,
                x=data["CRE / RM"],
                y=data[col],
                marker_color=colors[ptype],
                hovertemplate=f"%{{x}}<br>{ptype} Converted: %{{y}}<extra></extra>",
            ))
    fig.update_layout(
        barmode="group",
        title="Converted by Proposal Type per CRE/RM",
        xaxis_title="CRE / RM",
        yaxis_title="Converted",
        legend=dict(orientation="h", yanchor="bottom", y=-0.3),
        plot_bgcolor="white",
        margin=dict(t=50, b=80),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab B — Horizontal Bar: Premium Converted per CRE/RM
# ---------------------------------------------------------------------------

def horizontal_bar_premium(df: pd.DataFrame) -> go.Figure:
    data = df[df["CRE / RM"] != "TOTAL"].copy().sort_values("Premium Converted (₹)")
    # Colour by conversion rate (not converted %)
    conv_rates = 100 - data["% Not Converted"]
    fig = go.Figure(go.Bar(
        x=data["Premium Converted (₹)"],
        y=data["CRE / RM"],
        orientation="h",
        marker=dict(
            color=conv_rates,
            colorscale=[[0, COLOR_NOT_CONVERTED], [0.5, COLOR_AMBER], [1, COLOR_CONVERTED]],
            showscale=True,
            colorbar=dict(title="Conv. Rate %"),
        ),
        hovertemplate="%{y}<br>Premium: ₹%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        title="Premium Converted by CRE/RM",
        xaxis_title="Total Premium (₹)",
        yaxis_title="",
        plot_bgcolor="white",
        margin=dict(t=50, l=160),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab B — Pie: Share of Enquiries per CRE/RM
# ---------------------------------------------------------------------------

def pie_enquiry_share(df: pd.DataFrame) -> go.Figure:
    data = df[df["CRE / RM"] != "TOTAL"].copy()
    fig = go.Figure(go.Pie(
        labels=data["CRE / RM"],
        values=data["Total Enquiries"],
        hole=0.35,
        hovertemplate="%{label}<br>%{value} enquiries (%{percent})<extra></extra>",
    ))
    fig.update_layout(
        title="Share of Enquiries by CRE/RM",
        legend=dict(orientation="v"),
        margin=dict(t=50),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab C — Dual-Axis: Bar (enquiries) + Line (conversion %)
# ---------------------------------------------------------------------------

def dual_axis_monthly(df: pd.DataFrame) -> go.Figure:
    data = df[df["Month"] != "TOTAL"].copy()
    avg_conv = data["Conversion %"].mean()

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="No. of Enquiries",
        x=data["Month"],
        y=data["No. of Enquiries"],
        marker_color=COLOR_NAVY,
        opacity=0.75,
        yaxis="y1",
        hovertemplate="%{x}<br>Enquiries: %{y}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        name="Conversion %",
        x=data["Month"],
        y=data["Conversion %"],
        mode="lines+markers",
        line=dict(color=COLOR_CONVERTED, width=2),
        marker=dict(size=8),
        yaxis="y2",
        hovertemplate="%{x}<br>Conversion: %{y:.1f}%<extra></extra>",
    ))
    # Reference line: annual average
    fig.add_trace(go.Scatter(
        name=f"Annual Avg ({avg_conv:.1f}%)",
        x=data["Month"],
        y=[avg_conv] * len(data),
        mode="lines",
        line=dict(color=COLOR_AMBER, width=1.5, dash="dash"),
        yaxis="y2",
        hoverinfo="skip",
    ))
    fig.update_layout(
        title="Monthly Enquiries & Conversion Rate",
        xaxis_title="Month",
        yaxis=dict(title="No. of Enquiries", side="left"),
        yaxis2=dict(title="Conversion %", side="right", overlaying="y",
                    tickformat=".1f", ticksuffix="%"),
        legend=dict(orientation="h", yanchor="bottom", y=-0.35),
        plot_bgcolor="white",
        margin=dict(t=50, b=100),
    )
    return fig


# ---------------------------------------------------------------------------
# Tab D — Funnel Chart
# ---------------------------------------------------------------------------

def funnel_chart(total: int, quoted: int, closed: int) -> go.Figure:
    pct_quoted = round(quoted / total * 100, 1) if total else 0
    pct_closed = round(closed / total * 100, 1) if total else 0

    fig = go.Figure(go.Funnel(
        y=["Total Enquiries", "Quote Submitted", "Business Closed"],
        x=[total, quoted, closed],
        textinfo="value+percent initial",
        marker=dict(color=[COLOR_NAVY, COLOR_AMBER, COLOR_CONVERTED]),
        connector=dict(line=dict(color="lightgrey", width=1)),
        hovertemplate="%{label}<br>Count: %{value}<br>%{percentInitial} of total<extra></extra>",
    ))
    fig.update_layout(
        title="Sales Funnel",
        margin=dict(t=50),
        plot_bgcolor="white",
    )
    return fig
