"""
Sidebar component — solid navy-blue background with glassmorphism overlay.
4 nav cards in pastel colours, UPPERCASE labels with image icons.

Styling approach:
  • Streamlit-internal selectors ([data-testid="stSidebar"], .stRadio, .stButton)
    require raw <style> injection — Tailwind cannot reach them.
  • The card HTML itself uses Tailwind utility classes (flex, items-center, gap,
    rounded-xl, shadow, tracking, transition, translate, border, etc.).
  • Per-card background colour is dynamic (set inline) since it varies per card.
  • Active-state border/shadow/lift is toggled by a conditional Tailwind class string.
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

PILL_COLORS = {
    "Master Data (From April 25 to March 26)": {"bg": "#C4B5FD", "text": "#3B0764"},
}

# ── Raw CSS for Streamlit internals Tailwind cannot target ───────────────────
_SIDEBAR_CSS = """
<style>
/* ── Hide auto page navigation ─────────────────────────────────────────────── */
[data-testid="stSidebarNav"],
[data-testid="stSidebarNavItems"],
[data-testid="stSidebarNavSeparator"],
section[data-testid="stSidebar"] nav { display: none !important; }

/* ── Sidebar shell: solid navy + glassmorphism overlay ──────────────────────── */
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

/* ── Hide the hidden radio widget ───────────────────────────────────────────── */
[data-testid="stSidebar"] .stRadio { display: none !important; }

/* ── Sign-out button ────────────────────────────────────────────────────────── */
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
"""

# ── Tailwind class strings for card elements ─────────────────────────────────
# Base card: flex row, align-center, gap, padding, rounded, shadow, font, transition
_CARD_BASE = (
    "flex items-center gap-[11px] px-4 py-[14px] rounded-xl cursor-default "
    "text-[11px] font-bold text-[#1A1F36] tracking-[0.7px] "
    "shadow-md border-[1.5px] border-transparent "
    "transition-all duration-200 ease-in-out"
)
# Extra classes applied when card is the active page
_CARD_ACTIVE = "border-white/55 shadow-xl -translate-y-0.5"


def render_sidebar() -> None:
    """Render the sidebar with logo, nav cards, and sign-out button."""

    # Inject raw CSS for Streamlit internals (outside sidebar context so it applies globally)
    st.markdown(_SIDEBAR_CSS, unsafe_allow_html=True)

    with st.sidebar:
        # Logo + divider
        st.markdown(
            '<div class="text-center px-5 pt-7 pb-4">'
            '<img src="https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png" '
            'alt="Salasar" style="height:44px;filter:brightness(0) invert(1);opacity:0.95;">'
            '</div>'
            '<hr style="border:none;border-top:1px solid rgba(255,255,255,0.15);margin:0 16px 20px;">',
            unsafe_allow_html=True,
        )

        # Initialise page state
        if "current_page" not in st.session_state:
            st.session_state.current_page = "Business Conversion Ratio"

        current_page = st.session_state.get("current_page", "Business Conversion Ratio")

        # Hidden radio — Streamlit needs this to trigger reruns on navigation
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

        # Build all card HTML in a single call (avoids stray </div> artefacts)
        cards_html = '<div class="flex flex-col gap-[10px] px-[14px]">'
        for key, label, icon_url, bg, pill in NAV_ITEMS:
            is_active = key == st.session_state.get("current_page")
            active_cls = _CARD_ACTIVE if is_active else ""

            pill_html = ""
            if pill:
                pc = PILL_COLORS.get(key, {"bg": "#DDD", "text": "#333"})
                pill_html = (
                    f'<span class="inline-block py-[2px] px-[9px] rounded-full '
                    f'text-[10px] font-semibold tracking-[0.3px] w-fit" '
                    f'style="background:{pc["bg"]};color:{pc["text"]};">{pill}</span>'
                )

            cards_html += (
                f'<div class="{_CARD_BASE} {active_cls}" style="background:{bg};">'
                    f'<img class="w-[22px] h-[22px] flex-shrink-0 object-contain" src="{icon_url}" alt="">'
                    f'<div class="flex flex-col gap-[5px] leading-snug">'
                        f'<span>{label}</span>'
                        f'{pill_html}'
                    f'</div>'
                f'</div>'
            )
        cards_html += '</div>'

        st.html(cards_html)

        # Spacer before sign-out
        st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

        if st.button("Sign out", use_container_width=True):
            from utils.auth import logout
            logout()


def navigate_to_page(page_name: str) -> None:
    """Programmatically navigate to a page and rerun."""
    st.session_state.current_page = page_name
    st.rerun()


def get_current_page() -> str:
    """Return the currently active page key."""
    return st.session_state.get("current_page", "Business Conversion Ratio")
