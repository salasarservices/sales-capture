"""
Table rendering helpers — styled HTML tables with brand colours.
"""

import streamlit as st
import pandas as pd
import io
import random

# ── Brand tokens ─────────────────────────────────────────────────────────────
_NAVY        = "#042C53"
_NAVY_MED    = "#185FA5"
_NAVY_ACCENT = "#378ADD"
_NAVY_LT     = "#EBF2FB"
_BORDER      = "#B5D4F4"

# Short column aliases for the enquiry detail table
_ENQ_ALIASES = {
    "Enquiry No.":                                        "Enq #",
    "Date (When The Proposal Referred To The Company)":   "Date",
    "Company Name":                                       "Company",
    "Name of the Contact Person":                         "Contact",
    "Phone No.":                                          "Phone",
    "E-Mail":                                             "Email",
    "Requirement":                                        "Product",
    "Premium Potential":                                  "Premium (₹)",
    "Type Of Proposal":                                   "Type",
    "Expiry Date Of Existing Policy (If Renewal)":        "Expiry",
    "CRE(Expanded) / RM(New) Accountable":                "CRE / RM",
    "Tentative Brokerage (12%)":                          "Brokerage (₹)",
    "Quote Submission Date — Planned Date":               "Q. Planned",
    "Quote Submission Date — Actual Date":                 "Q. Actual",
    "Quote Submitted":                                    "Quoted",
    "Actual Closure Date — Planned Date":                 "C. Planned",
    "Actual Closure Date — Actual Date":                  "C. Actual",
    "Business Closed":                                    "Closed",
    "Reason For Sales Not Closed":                        "Reason",
}


def _styled_table(df: pd.DataFrame, height: int = 500) -> None:
    """Render a beautifully styled HTML table with brand colours, bold headers,
    alternating row shading, sticky header, and row hover effect."""

    tid = f"tbl_{random.randint(100_000, 999_999)}"

    headers_html = "".join(f"<th>{col}</th>" for col in df.columns)

    rows_parts = []
    for i, (_, row) in enumerate(df.iterrows()):
        first = str(row.iloc[0]).upper() if len(row) > 0 else ""
        if first == "TOTAL":
            cls = "total-row"
        elif i % 2 == 0:
            cls = "even-row"
        else:
            cls = "odd-row"
        cells = "".join(f"<td>{'' if pd.isna(v) else v}</td>" for v in row)
        rows_parts.append(f'<tr class="{cls}">{cells}</tr>')

    html = f"""
<style>
#{tid}-wrap {{
    overflow: auto;
    max-height: {height}px;
    border: 1px solid {_BORDER};
    border-radius: 8px;
    box-shadow: 0 2px 10px rgba(4,44,83,0.10);
    margin-bottom: 4px;
}}
#{tid}-wrap table {{
    border-collapse: collapse;
    width: 100%;
    font-family: inherit;
}}
#{tid}-wrap thead th {{
    position: sticky;
    top: 0;
    z-index: 3;
    background: {_NAVY};
    color: #ffffff;
    font-weight: 700;
    font-size: 0.78rem;
    text-transform: uppercase;
    letter-spacing: 0.45px;
    padding: 10px 14px;
    text-align: left;
    white-space: nowrap;
    border-right: 1px solid rgba(255,255,255,0.10);
    border-bottom: 2px solid {_NAVY_ACCENT};
}}
#{tid}-wrap thead th:last-child {{ border-right: none; }}
#{tid}-wrap td {{
    padding: 7px 14px;
    font-size: 0.82rem;
    color: #1A1F36;
    border-bottom: 1px solid {_BORDER};
    border-right: 1px solid #EDF2F7;
    white-space: nowrap;
}}
#{tid}-wrap td:last-child {{ border-right: none; }}
#{tid}-wrap tr.even-row  {{ background: {_NAVY_LT}; }}
#{tid}-wrap tr.odd-row   {{ background: #ffffff; }}
#{tid}-wrap tr.total-row {{
    background: {_NAVY_MED};
    color: #ffffff;
    font-weight: 700;
}}
#{tid}-wrap tr.total-row td {{ color: #ffffff; border-bottom: none; }}
#{tid}-wrap tr.even-row:hover td,
#{tid}-wrap tr.odd-row:hover td  {{ background: #cce0f7; }}
</style>
<div id="{tid}-wrap">
  <table>
    <thead><tr>{headers_html}</tr></thead>
    <tbody>{"".join(rows_parts)}</tbody>
  </table>
</div>
"""
    st.markdown(html, unsafe_allow_html=True)


def render_html_table(
    df: pd.DataFrame,
    height: int = 500,
    id_col: str = None,
    raw_conv: pd.Series = None,
) -> None:
    """Render a styled data table."""
    _styled_table(df, height=height)


def render_enquiry_table(df: pd.DataFrame, height: int = 600) -> None:
    """Render the enquiry detail table with column aliases and brand styling."""
    renamed = df.rename(columns=_ENQ_ALIASES)
    cols = [c for c in _ENQ_ALIASES.values() if c in renamed.columns]
    _styled_table(renamed[cols], height=height)


def render_table(df: pd.DataFrame, height: int = 450, key: str = "table"):
    """Styled table (legacy fallback)."""
    _styled_table(df, height=height)


def export_csv_button(
    df: pd.DataFrame,
    filename: str = "export.csv",
    label: str = "⬇ Export CSV",
):
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name=filename,
        mime="text/csv",
        key=f"dl_{filename}",
    )
