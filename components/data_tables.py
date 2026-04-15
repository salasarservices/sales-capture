"""
Table rendering helpers — styled with Tailwind CSS utility classes.

render_html_table()    — summary tables (business conversion, sales capture, etc.)
render_enquiry_table() — wide master-data table (19 columns, fixed proportional widths)
export_csv_button()    — CSV download button

Tailwind handles all static structural styling (border, rounded, bg, text, padding,
sticky thead, hover).  Two small patterns that Tailwind can't express cleanly are
delegated to named classes defined in utils/styles._STREAMLIT_OVERRIDES:

  .tw-row-total td  — bold / slate bg / top-border for the TOTAL summary row
  .tw-row-red td    — red tint when conversion rate < 50 %
  .tw-row-amber td  — amber tint when conversion rate < 70 %
  .tw-badge-yes     — green dot badge for Yes cells
  .tw-badge-no      — red dot badge for No cells
  .tw-scroll        — custom ::webkit-scrollbar styling
"""

import streamlit as st
import pandas as pd
import io
import html as _html

# ── Short column aliases for the enquiry detail table ────────────────────────
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
    "Quote Submission Date — Actual Date":                "Q. Actual",
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

# ── Shared Tailwind class strings ────────────────────────────────────────────
# Header cell: uppercase, small, bold, gray, no-wrap, bottom border
_TH = (
    "px-[14px] py-[10px] text-left text-[10.5px] font-bold uppercase "
    "tracking-[0.06em] text-gray-500 whitespace-nowrap border-b-[1.5px] border-gray-200"
)
# Body cell: padded, gray-700 text, no-wrap
_TD = "px-[14px] py-[9px] text-gray-700 whitespace-nowrap"
# Body row: bottom border, hover bg (static rows — dynamic states via .tw-row-*)
_TR = "border-b border-gray-100 last:border-b-0 hover:bg-gray-50"


def _escape(val) -> str:
    return _html.escape(str(val)) if val is not None and str(val) != "nan" else ""


def _yes_no_cell(val: str) -> str:
    v = str(val).strip()
    if v.lower() == "yes":
        return '<span class="tw-badge-yes">&#9679; Yes</span>'
    if v.lower() == "no":
        return '<span class="tw-badge-no">&#9679; No</span>'
    return _escape(val)


# ── Generic summary table ────────────────────────────────────────────────────

def render_html_table(
    df: pd.DataFrame,
    height: int = 500,
    id_col: str = None,
    raw_conv: pd.Series = None,
) -> None:
    """
    Render a styled HTML table with Tailwind utility classes.

    Parameters
    ----------
    df       : display-formatted DataFrame
    height   : max vertical height in px (table scrolls inside)
    id_col   : column whose value == "TOTAL" gets the total-row style
    raw_conv : raw float Series for conversion-rate row colouring
               (red < 50 %, amber < 70 %)
    """
    header_cells = "".join(
        f"<th class='{_TH}' title='{_escape(col)}'>{_escape(col)}</th>"
        for col in df.columns
    )

    rows_html = []
    for idx in range(len(df)):
        row = df.iloc[idx]

        # Row state class (defined in _STREAMLIT_OVERRIDES for child td targeting)
        if id_col and str(row.get(id_col, "")) == "TOTAL":
            state = "tw-row-total"
        elif raw_conv is not None:
            try:
                val = float(raw_conv.iloc[idx])
                state = "tw-row-red" if val < 50 else ("tw-row-amber" if val < 70 else "")
            except (TypeError, ValueError):
                state = ""
        else:
            state = ""

        cells = "".join(
            f"<td class='{_TD}' title='{_escape(row[col])}'>{_escape(row[col])}</td>"
            for col in df.columns
        )
        rows_html.append(f'<tr class="{_TR} {state}">{cells}</tr>')

    st.markdown(
        f"""
        <div class="border border-gray-200 rounded-xl overflow-hidden bg-white">
            <div class="tw-scroll overflow-auto" style="max-height:{height}px;">
                <table class="w-full text-[12.5px] bg-white border-collapse">
                    <thead class="sticky top-0 z-10">
                        <tr class="bg-gray-50">{header_cells}</tr>
                    </thead>
                    <tbody>{"".join(rows_html)}</tbody>
                </table>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Wide enquiry detail table ────────────────────────────────────────────────

def render_enquiry_table(df: pd.DataFrame, height: int = 600) -> None:
    """
    Render the master-data enquiry table with:
    - Short column aliases (all 19 columns without horizontal scroll)
    - Fixed proportional column widths via <colgroup>
    - Yes/No badge colouring for Quoted and Closed columns
    """
    renamed = df.rename(columns=_ENQ_ALIASES)
    cols    = [c for c in _ENQ_ALIASES.values() if c in renamed.columns]
    renamed = renamed[cols]

    widths  = _ENQ_WIDTHS[: len(cols)]
    col_els = "".join(f'<col style="width:{w}%">' for w in widths)

    header_cells = "".join(
        f"<th class='{_TH}' title='{c}'>{c}</th>" for c in renamed.columns
    )

    rows_html = []
    for idx in range(len(renamed)):
        row   = renamed.iloc[idx]
        cells = []
        for col in renamed.columns:
            raw = row[col]
            if col in _YES_NO_COLS:
                cells.append(f"<td class='px-[14px] py-[9px] whitespace-nowrap'>{_yes_no_cell(raw)}</td>")
            else:
                v = _escape(raw)
                cells.append(f"<td class='{_TD}' title='{v}'>{v}</td>")
        rows_html.append(f"<tr class='{_TR}'>{''.join(cells)}</tr>")

    st.markdown(
        f"""
        <div class="border border-gray-200 rounded-xl overflow-hidden bg-white">
            <div class="tw-scroll overflow-auto" style="max-height:{height}px; overflow-x:hidden;">
                <table class="w-full text-[12.5px] bg-white border-collapse">
                    <colgroup>{col_els}</colgroup>
                    <thead class="sticky top-0 z-10">
                        <tr class="bg-gray-50">{header_cells}</tr>
                    </thead>
                    <tbody>{"".join(rows_html)}</tbody>
                </table>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ── Legacy / fallback helpers ────────────────────────────────────────────────

def render_table(df: pd.DataFrame, height: int = 450, key: str = "table"):
    """Fallback: native Streamlit dataframe."""
    st.dataframe(df, width="stretch", height=height, hide_index=True, key=key)


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
    """Pandas-style row colouring (fallback where native df is preferred)."""
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
