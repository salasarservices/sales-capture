"""
Styled dataframe helpers and CSV export button.
"""

import streamlit as st
import pandas as pd
import io


def render_table(df: pd.DataFrame, height: int = 450, key: str = "table"):
    """Render a dataframe with sticky header and row hover."""
    st.dataframe(df, use_container_width=True, height=height, hide_index=True, key=key)


def export_csv_button(df: pd.DataFrame, filename: str = "export.csv", label: str = "Export CSV"):
    """Render a download button for CSV export."""
    buf = io.StringIO()
    df.to_csv(buf, index=False)
    st.download_button(
        label=label,
        data=buf.getvalue(),
        file_name=filename,
        mime="text/csv",
        key=f"dl_{filename}",
    )


def highlight_conversion_row(df: pd.DataFrame, conv_col: str = "Conversion %") -> pd.DataFrame.style:
    """
    Apply colour highlighting to monthly conversion table.
    < 50% → red background, < 70% → amber, TOTAL row → bold.
    """
    def style_row(row):
        styles = [""] * len(row)
        if row.get("Month") == "TOTAL":
            return ["font-weight: bold; background-color: #F1F5F9"] * len(row)
        val = row.get(conv_col, 100)
        try:
            val = float(val)
        except (TypeError, ValueError):
            return styles
        if val < 50:
            bg = "background-color: #FEE2E2"  # red-100
        elif val < 70:
            bg = "background-color: #FEF3C7"  # amber-100
        else:
            bg = ""
        return [bg] * len(row)

    return df.style.apply(style_row, axis=1)


def highlight_totals_row(df: pd.DataFrame, id_col: str = "CRE / RM") -> pd.DataFrame.style:
    """Bold and shade the TOTAL row."""
    def style_row(row):
        if row.get(id_col) == "TOTAL":
            return ["font-weight: bold; background-color: #F1F5F9"] * len(row)
        return [""] * len(row)
    return df.style.apply(style_row, axis=1)
