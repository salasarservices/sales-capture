"""
Table rendering helpers — pure native Streamlit st.dataframe(), zero custom CSS.
"""

import streamlit as st
import pandas as pd
import io

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


def render_html_table(
    df: pd.DataFrame,
    height: int = 500,
    id_col: str = None,
    raw_conv: pd.Series = None,
) -> None:
    """Render a data table using native st.dataframe()."""
    st.dataframe(df, use_container_width=True, height=height, hide_index=True)


def render_enquiry_table(df: pd.DataFrame, height: int = 600) -> None:
    """Render the enquiry detail table using native st.dataframe()."""
    renamed = df.rename(columns=_ENQ_ALIASES)
    cols = [c for c in _ENQ_ALIASES.values() if c in renamed.columns]
    st.dataframe(renamed[cols], use_container_width=True, height=height, hide_index=True)


def render_table(df: pd.DataFrame, height: int = 450, key: str = "table"):
    """Native Streamlit dataframe (legacy fallback)."""
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
