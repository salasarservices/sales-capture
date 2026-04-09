"""
Session-state based authentication for Streamlit.
Credentials stored in st.secrets["credentials"].

IMPORTANT — HTML rendering rules for Streamlit st.markdown():
  · Never indent HTML content 4+ spaces  → triggers markdown code-block
  · Never use <!-- --> HTML comments      → confuses markdown parser
  · Keep each st.markdown() call a single compact line or use explicit <br>
"""

import streamlit as st
import bcrypt

LOGO_URL = "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"

_FEATURES = [
    ("📊", "Sales Analytics",    "Live conversion and pipeline visibility"),
    ("👥", "CRE / RM Tracking",  "Performance split by accountable owner"),
    ("📅", "Monthly Trends",     "Fiscal-month conversion trend analysis"),
    ("🔍", "Enquiry Drilldown",  "Searchable and filterable enquiry records"),
]


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


# ─────────────────────────────────────────────────────────────────────────────
#  LOGIN FORM
# ─────────────────────────────────────────────────────────────────────────────

def login_form() -> bool:
    """
    Render the split-layout login page.
    LEFT  : dark navy brand panel — logo, heading, feature list
    RIGHT : light gray form panel — logo, Login heading, form
    Returns True if already authenticated.
    """
    from utils.styles import inject_login_css
    inject_login_css()

    if st.session_state.get("authenticated"):
        return True

    left_col, right_col = st.columns([5, 7])

    # ── LEFT : brand panel ────────────────────────────────────────────────
    with left_col:
        # Logo — white-filtered for dark bg (single-line, no indent)
        st.markdown(f'<img src="{LOGO_URL}" style="height:42px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.88;display:block;margin-bottom:2.75rem;">', unsafe_allow_html=True)

        # Main heading (single line — avoids 4-space code-block trigger)
        st.markdown('<h1 style="color:#FFFFFF;font-size:2.35rem;font-weight:800;line-height:1.18;margin:0 0 0.65rem;letter-spacing:-0.5px;">Sales Enquiry<br>Dashboard</h1>', unsafe_allow_html=True)

        # Sub-heading
        st.markdown('<p style="color:rgba(255,255,255,0.55);font-size:0.90rem;margin:0 0 2.75rem;line-height:1.5;">Salasar Services &nbsp;&middot;&nbsp; Ahmedabad Branch &nbsp;&middot;&nbsp; FY 2025-26</p>', unsafe_allow_html=True)

        # Feature tiles — one st.markdown per tile, all single-line
        for icon, title, desc in _FEATURES:
            st.markdown(
                f'<div style="display:flex;align-items:flex-start;gap:0.85rem;margin-bottom:1.15rem;">'
                f'<div style="width:38px;height:38px;flex-shrink:0;background:rgba(255,255,255,0.11);display:flex;align-items:center;justify-content:center;font-size:1.05rem;">{icon}</div>'
                f'<div><div style="color:#FFFFFF;font-weight:600;font-size:0.88rem;margin-bottom:0.12rem;">{title}</div>'
                f'<div style="color:rgba(255,255,255,0.48);font-size:0.75rem;line-height:1.45;">{desc}</div></div></div>',
                unsafe_allow_html=True,
            )

        # Footer
        st.markdown('<p style="color:rgba(255,255,255,0.22);font-size:0.69rem;margin-top:3rem;">© 2025 Salasar Services · Ahmedabad</p>', unsafe_allow_html=True)

    # ── RIGHT : form panel ────────────────────────────────────────────────
    with right_col:
        # Vertical spacer
        st.markdown('<div style="height:13vh;"></div>', unsafe_allow_html=True)

        _, form_col, _ = st.columns([1, 8, 1])
        with form_col:
            # Logo — original colours (single line)
            st.markdown(f'<img src="{LOGO_URL}" style="height:38px;object-fit:contain;display:block;margin-bottom:1.4rem;">', unsafe_allow_html=True)

            # "Login" heading (single line)
            st.markdown('<h2 style="font-size:1.85rem;font-weight:700;color:#1E293B;margin:0 0 0.2rem;letter-spacing:-0.3px;">Login</h2>', unsafe_allow_html=True)

            # Subtext (single line)
            st.markdown('<p style="color:#64748B;font-size:0.83rem;margin:0 0 1.5rem;">Enter your dashboard credentials</p>', unsafe_allow_html=True)

            with st.form("login_form"):
                st.text_input("Username", placeholder="Enter username",    key="_login_user")
                st.text_input("Password", placeholder="••••••••", type="password", key="_login_pass")
                submitted = st.form_submit_button("SIGN IN", use_container_width=True)

        if submitted:
            username = st.session_state.get("_login_user", "")
            password = st.session_state.get("_login_pass", "")
            try:
                user_cfg = st.secrets["credentials"][username]
            except (KeyError, Exception):
                user_cfg = None

            if user_cfg and _verify_password(password, user_cfg["password_hash"]):
                st.session_state.authenticated = True
                st.session_state.username      = username
                st.session_state.role          = user_cfg.get("role", "viewer")
                st.rerun()
            else:
                with form_col:
                    st.error("Invalid username or password.")

    return False


# ─────────────────────────────────────────────────────────────────────────────
#  AUTHENTICATED SIDEBAR BRANDING
# ─────────────────────────────────────────────────────────────────────────────

def render_sidebar_branding() -> None:
    """Render logo + user info + sign-out in the sidebar (authenticated pages)."""
    with st.sidebar:
        # Logo — white-filtered (single line, no indent)
        st.markdown(f'<img src="{LOGO_URL}" style="height:40px;object-fit:contain;filter:brightness(0) invert(1);opacity:0.88;display:block;margin:0.75rem 0 0.5rem;">', unsafe_allow_html=True)
        st.divider()

        role_label = "Admin" if is_admin() else "Viewer"
        # User info row (single line)
        st.markdown(
            f'<div style="display:flex;align-items:center;gap:0.55rem;padding:0.45rem 0 0.6rem;">'
            f'<div style="width:30px;height:30px;background:rgba(255,255,255,0.11);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:0.9rem;flex-shrink:0;">👤</div>'
            f'<div><div style="color:#FFFFFF;font-size:0.84rem;font-weight:600;">{st.session_state.get("username","")}</div>'
            f'<div style="color:rgba(255,255,255,0.46);font-size:0.69rem;">{role_label}</div></div></div>',
            unsafe_allow_html=True,
        )

        if st.button("Sign Out", use_container_width=True):
            logout()


# ─────────────────────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────────────────────

def require_auth():
    """Call at the top of every page. Stops rendering if not logged in."""
    if not st.session_state.get("authenticated"):
        login_form()
        st.stop()


def is_admin() -> bool:
    return st.session_state.get("role") == "admin"


def logout():
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()
