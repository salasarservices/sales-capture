"""
Table rendering helpers for the Salasar Sales Dashboard.

render_html_table()     — styled HTML table for summary pages (few columns)
render_enquiry_table()  — fixed-width HTML table for the wide enquiry detail view
export_csv_button()     — CSV download button
"""

import streamlit as st
import pandas as pd
import io
import html as _html

# ─────────────────────────────────────────────────────────────────────────────
#  Short column aliases for the enquiry detail table
# ─────────────────────────────────────────────────────────────────────────────
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

# Column widths (%) — total = 100
_ENQ_WIDTHS = [
    3, 6, 9, 6, 5, 7,        # Enq #, Date, Company, Contact, Phone, Email
    5, 5, 4, 5,               # Product, Premium, Type, Expiry
    7, 5,                     # CRE/RM, Brokerage
    5, 5, 4, 5, 5, 4, 4,     # Q.Planned, Q.Actual, Quoted, C.Planned, C.Actual, Closed, Reason
]

_YES_NO_COLS = {"Quoted", "Closed"}


def _escape(val) -> str:
    return _html.escape(str(val)) if val is not None and str(val) != "nan" else ""


def _yes_no_cell(val: str) -> str:
    v = str(val).strip()
    if v.lower() == "yes":
        return '<span class="badge-yes">● Yes</span>'
    if v.lower() == "no":
        return '<span class="badge-no">● No</span>'
    return _escape(val)


# ─────────────────────────────────────────────────────────────────────────────
#  Generic summary table
# ─────────────────────────────────────────────────────────────────────────────

def render_html_table(
    df: pd.DataFrame,
    height: int = 500,
    id_col: str = None,
    raw_conv: pd.Series = None,
) -> None:
    """
    Render a styled HTML table with bold uppercase navy headers.

    Parameters
    ----------
    df          : display-formatted DataFrame
    height      : max vertical height in px (table scrolls inside)
    id_col      : column whose value == "TOTAL" gets the total-row style
    raw_conv    : raw float Series for conversion-rate row colouring
                  (red < 50 %, amber < 70 %)
    """
    # Header row
    header_cells = "".join(
        f"<th title='{_escape(col)}'>{_escape(col)}</th>"
        for col in df.columns
    )

    rows_html = []
    for idx in range(len(df)):
        row = df.iloc[idx]

        # Row class
        if id_col and str(row.get(id_col, "")) == "TOTAL":
            row_cls = "dash-table-total"
        elif raw_conv is not None:
            try:
                val = float(raw_conv.iloc[idx])
                row_cls = "dash-table-red" if val < 50 else (
                    "dash-table-amber" if val < 70 else ""
                )
            except (TypeError, ValueError):
                row_cls = ""
        else:
            row_cls = ""

        cells = "".join(
            f"<td title='{_escape(row[col])}'>{_escape(row[col])}</td>"
            for col in df.columns
        )
        rows_html.append(f'<tr class="{row_cls}">{cells}</tr>')

    st.markdown(
        f"""
        <div class="dash-table-wrapper" style="max-height:{height}px;">
            <table class="dash-table">
                <thead><tr>{header_cells}</tr></thead>
                <tbody>{"".join(rows_html)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Wide enquiry detail table
# ─────────────────────────────────────────────────────────────────────────────

def render_enquiry_table(df: pd.DataFrame, height: int = 600) -> None:
    """
    Render the Sales Funnel enquiry table with:
    - Short column aliases (fit all 19 columns without horizontal scroll)
    - Fixed proportional column widths via <colgroup>
    - Yes/No badge colouring for Quoted and Closed columns
    """
    # Rename to short aliases
    renamed = df.rename(columns=_ENQ_ALIASES)
    cols = [c for c in _ENQ_ALIASES.values() if c in renamed.columns]
    renamed = renamed[cols]

    # Build <colgroup>
    widths = _ENQ_WIDTHS[: len(cols)]
    col_els = "".join(
        f'<col style="width:{w}%">' for w in widths
    )

    # Header
    header_cells = "".join(
        f"<th title='{c}'>{c}</th>" for c in renamed.columns
    )

    # Body
    rows_html = []
    for idx in range(len(renamed)):
        row = renamed.iloc[idx]
        cells = []
        for col in renamed.columns:
            raw = row[col]
            if col in _YES_NO_COLS:
                cells.append(f"<td>{_yes_no_cell(raw)}</td>")
            else:
                v = _escape(raw)
                cells.append(f"<td title='{v}'>{v}</td>")
        rows_html.append(f"<tr>{''.join(cells)}</tr>")

    st.markdown(
        f"""
        <div class="dash-table-wrapper" style="max-height:{height}px; overflow-x:hidden;">
            <table class="dash-table enquiry-table">
                <colgroup>{col_els}</colgroup>
                <thead><tr>{header_cells}</tr></thead>
                <tbody>{"".join(rows_html)}</tbody>
            </table>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
#  Legacy helpers (kept for backward compatibility)
# ─────────────────────────────────────────────────────────────────────────────

def render_table(df: pd.DataFrame, height: int = 450, key: str = "table"):
    """Fallback: native Streamlit dataframe."""
    st.dataframe(df, use_container_width=True, height=height, hide_index=True, key=key)


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


def highlight_conversion_row(
    df: pd.DataFrame, conv_col: str = "Conversion %"
) -> "pd.DataFrame.style":
    """Pandas-style row colouring (used as fallback where native df is needed)."""
    def _style(row):
        if row.get("Month") == "TOTAL":
            return ["font-weight:bold; background-color:#F1F5F9"] * len(row)
        try:
            val = float(row.get(conv_col, 100))
        except (TypeError, ValueError):
            return [""] * len(row)
        bg = "background-color:#FEE2E2" if val < 50 else (
            "background-color:#FEF3C7" if val < 70 else ""
        )
        return [bg] * len(row)

    return df.style.apply(_style, axis=1)


def highlight_totals_row(
    df: pd.DataFrame, id_col: str = "CRE / RM"
) -> "pd.DataFrame.style":
    def _style(row):
        if row.get(id_col) == "TOTAL":
            return ["font-weight:bold; background-color:#F1F5F9"] * len(row)
        return [""] * len(row)
    return df.style.apply(_style, axis=1)
