"""
Global Streamlit theme helpers for a modern dashboard look.
"""

import streamlit as st


PRIMARY = "#183b62"      # deep blue
SECONDARY = "#2b7a9a"    # steel blue
ACCENT = "#ef7f45"       # salasar-inspired orange accent
BG = "#f3f6fb"           # app background
CARD = "#ffffff"         # card background
MUTED = "#64748b"        # muted text
BORDER = "#dbe4ef"       # subtle border


def apply_theme() -> None:
    """Inject app-wide CSS tweaks to make the dashboard look production-grade."""
    st.markdown(
        f"""
        <style>
            .stApp {{
                background: linear-gradient(180deg, {BG} 0%, #edf2f9 100%);
            }}

            [data-testid="stSidebar"] {{
                background: linear-gradient(180deg, #143252 0%, {PRIMARY} 55%, #245077 100%);
                border-right: 1px solid rgba(255,255,255,0.08);
            }}

            [data-testid="stSidebar"] * {{
                color: #f8fafc;
            }}

            .block-container {{
                padding-top: 1.15rem;
                padding-bottom: 1.5rem;
            }}

            h1, h2, h3 {{
                color: {PRIMARY};
                letter-spacing: -0.01em;
            }}

            .salasar-hero {{
                background: linear-gradient(120deg, {PRIMARY} 0%, #1f4f7c 55%, {ACCENT} 180%);
                color: white;
                border-radius: 16px;
                padding: 1rem 1.25rem;
                margin-bottom: 1rem;
                border: 1px solid rgba(255,255,255,0.16);
                box-shadow: 0 10px 26px rgba(24, 59, 98, 0.22);
            }}

            .salasar-hero h3 {{
                color: #ffffff;
            }}

            .salasar-hero p {{
                color: #e8eff9;
                margin: 0;
            }}

            .salasar-kpi-card {{
                background: {CARD};
                border: 1px solid {BORDER};
                border-left: 5px solid {ACCENT};
                border-radius: 14px;
                padding: 0.9rem 0.95rem;
                box-shadow: 0 5px 14px rgba(15, 23, 42, 0.06);
                min-height: 94px;
            }}

            .salasar-kpi-label {{
                font-size: 0.74rem;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                color: {MUTED};
                margin-bottom: 0.3rem;
                font-weight: 600;
            }}

            .salasar-kpi-value {{
                font-size: 1.35rem;
                font-weight: 700;
                color: {PRIMARY};
                line-height: 1.15;
            }}

            div[data-testid="stDataFrame"] {{
                border: 1px solid {BORDER};
                border-radius: 12px;
                overflow: hidden;
                box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04);
                background: #ffffff;
            }}

            [data-testid="stExpander"],
            [data-testid="stVerticalBlockBorderWrapper"]:has([data-testid="stMetric"]) {{
                border: 1px solid {BORDER};
                border-radius: 12px;
                background: #ffffff;
            }}

            .stMultiSelect div[data-baseweb="select"],
            .stTextInput input {{
                border-radius: 10px !important;
                border: 1px solid #c8d3e2 !important;
            }}

            button[kind="primary"] {{
                background: linear-gradient(90deg, {PRIMARY}, {SECONDARY}) !important;
                border: 0 !important;
                border-radius: 10px !important;
            }}

            .stDownloadButton button {{
                border-radius: 10px !important;
                border: 1px solid {PRIMARY} !important;
                color: {PRIMARY} !important;
                background: #f8fbff !important;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero(title: str, subtitle: str) -> None:
    st.markdown(
        f"""
        <div class="salasar-hero">
            <h3 style="margin:0;">{title}</h3>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )