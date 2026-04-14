"""
Sidebar component — solid RGB(22, 85, 171) with glassmorphism overlay.
4 nav cards in pastel colors, UPPERCASE labels with image icons.
"""

import streamlit as st


# Nav items: (page_key, display_label, icon_url, pastel_bg, pill_text)
NAV_ITEMS = [
    (
        "Business Conversion Ratio",
        "BUSINESS CONVERSION RATIO",
        "https://ik.imagekit.io/salasarservices/sales-capture/ratio.png",
        "#DBEAFE",
        None,
    ),
    (
        "Sales Capture Summary",
        "SALES CAPTURE SUMMARY",
        "https://ik.imagekit.io/salasarservices/sales-capture/summary.png",
        "#DCFCE7",
        None,
    ),
    (
        "Conversion Ratio Summary",
        "CONVERSION RATIO SUMMARY",
        "https://ik.imagekit.io/salasarservices/sales-capture/conversion.png",
        "#FEF9C3",
        None,
    ),
    (
        "Master Data (From April 25 to March 26)",
        "MASTER DATA",
        "https://ik.imagekit.io/salasarservices/sales-capture/database.png",
        "#EDE9FE",
        "Apr 25 – Mar 26",
    ),
]

# Pill badge colors paired with each card
PILL_COLORS = {
    "Master Data (From April 25 to March 26)": {"bg": "#C4B5FD", "text": "#3B0764"},
}


def render_sidebar():
    """Render the sidebar."""

    # Global CSS — applied outside sidebar context so it takes effect everywhere
    st.markdown("""
        <style>
        /* ── Hide Streamlit's automatic page navigation ── */
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"],
        section[data-testid="stSidebar"] nav {
            display: none !important;
        }

        /* ── Sidebar base: solid RGB(22,85,171) + glass overlay ── */
        [data-testid="stSidebar"] {
            background: rgba(22, 85, 171, 0.96) !important;
            backdrop-filter: blur(20px) saturate(1.4);
            -webkit-backdrop-filter: blur(20px) saturate(1.4);
            border-right: 1px solid rgba(255, 255, 255, 0.12) !important;
            box-shadow: 4px 0 32px rgba(0, 0, 0, 0.28) !important;
        }
        [data-testid="stSidebar"] > div:first-child {
            background: transparent !important;
            padding-top: 0 !important;
        }

        /* ── Hide the Streamlit radio widget entirely ── */
        [data-testid="stSidebar"] .stRadio {
            display: none !important;
        }

        /* ── Logo ── */
        .sb-logo {
            text-align: center;
            padding: 28px 20px 18px;
        }
        .sb-logo img {
            height: 44px;
            filter: brightness(0) invert(1);
            opacity: 0.95;
        }

        /* ── Divider ── */
        .sb-divider {
            border: none;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            margin: 0 16px 20px;
        }

        /* ── Nav cards container ── */
        .sb-nav {
            display: flex;
            flex-direction: column;
            gap: 10px;
            padding: 0 14px;
        }

        /* ── Individual card ── */
        .sb-card {
            padding: 14px 16px;
            border-radius: 12px;
            cursor: default;
            font-size: 11px;
            font-weight: 700;
            color: #1A1F36;
            letter-spacing: 0.7px;
            display: flex;
            align-items: center;
            gap: 11px;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.10);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
            border: 1.5px solid transparent;
        }
        .sb-card.active {
            border-color: rgba(255, 255, 255, 0.55);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.18);
            transform: translateY(-2px);
        }

        /* ── Icon image ── */
        .sb-icon {
            width: 22px;
            height: 22px;
            flex-shrink: 0;
            object-fit: contain;
        }

        /* ── Label + pill wrapper ── */
        .sb-label-row {
            display: flex;
            flex-direction: column;
            gap: 5px;
            line-height: 1.3;
        }

        /* ── Pill badge ── */
        .sb-pill {
            display: inline-block;
            padding: 2px 9px;
            border-radius: 20px;
            font-size: 10px;
            font-weight: 600;
            letter-spacing: 0.3px;
            width: fit-content;
        }

        /* ── Sign out button ── */
        [data-testid="stSidebar"] .stButton > button {
            background: rgba(255, 255, 255, 0.10) !important;
            border: 1px solid rgba(255, 255, 255, 0.20) !important;
            border-radius: 10px !important;
            color: rgba(255, 255, 255, 0.85) !important;
            font-size: 13px !important;
            font-weight: 500 !important;
            transition: background 0.2s ease !important;
            margin-top: 6px !important;
        }
        [data-testid="stSidebar"] .stButton > button:hover {
            background: rgba(255, 255, 255, 0.20) !important;
            border-color: rgba(255, 255, 255, 0.35) !important;
        }
        </style>
    """, unsafe_allow_html=True)

    with st.sidebar:
        # Logo
        st.markdown("""
            <div class="sb-logo">
                <img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" alt="Salasar">
            </div>
            <hr class="sb-divider">
        """, unsafe_allow_html=True)

        # State: default to first page
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Business Conversion Ratio"

        current_page = st.session_state.get("current_page", "Business Conversion Ratio")

        # Hidden radio for state (Streamlit needs this for reruns)
        page_keys = [key for key, *_ in NAV_ITEMS]
        selected = st.radio(
            "nav",
            page_keys,
            index=page_keys.index(current_page) if current_page in page_keys else 0,
            label_visibility="collapsed",
            key="nav_radio",
        )
        if selected:
            st.session_state.current_page = selected

        # Build all card HTML in a single markdown call to avoid orphan </div> text
        cards_html = '<div class="sb-nav">'
        for key, label, icon_url, bg, pill in NAV_ITEMS:
            active_cls = "active" if key == st.session_state.get("current_page") else ""
            pill_html = ""
            if pill:
                pc = PILL_COLORS.get(key, {"bg": "#DDD", "text": "#333"})
                pill_html = (
                    f'<span class="sb-pill" style="background:{pc["bg"]};color:{pc["text"]};">'
                    f"{pill}</span>"
                )
            cards_html += f"""
                <div class="sb-card {active_cls}" style="background:{bg};">
                    <img class="sb-icon" src="{icon_url}" alt="">
                    <div class="sb-label-row">
                        <span>{label}</span>
                        {pill_html}
                    </div>
                </div>
            """
        cards_html += '</div>'
        st.html(cards_html)

        # Spacer
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

        # Sign out at bottom
        if st.button("Sign out", use_container_width=True):
            from utils.auth import logout
            logout()


def navigate_to_page(page_name: str):
    """Navigate to a specific page."""
    st.session_state.current_page = page_name
    st.rerun()


def get_current_page() -> str:
    """Get the current page name."""
    return st.session_state.get("current_page", "Business Conversion Ratio")
