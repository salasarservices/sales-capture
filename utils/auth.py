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
    LEFT  : dark navy brand card — logo + heading (single st.markdown block)
    RIGHT : light gray form panel — logo, Login heading, form
    Returns True if already authenticated.
    """
    from utils.styles import inject_login_css
    inject_login_css()

    if st.session_state.get("authenticated"):
        return True

    left_col, right_col = st.columns([5, 7])

    # ── LEFT : single-block brand card ───────────────────────────────────
    # Everything in ONE st.markdown() call → only one Streamlit wrapper div
    with left_col:
        st.markdown(
            f'<div class="login-brand-card">'
            f'<img src="{LOGO_URL}" class="login-brand-logo">'
            f'<h1 class="login-brand-heading">Sales Enquiry<br>Dashboard</h1>'
            f'<p class="login-brand-sub">Ahmedabad &nbsp;&middot;&nbsp; FY 2025-26</p>'
            f'</div>',
            unsafe_allow_html=True,
        )

    # ── RIGHT : form panel ────────────────────────────────────────────────
    with right_col:
        st.markdown('<div style="height:18vh;"></div>', unsafe_allow_html=True)

        _, form_col, _ = st.columns([1, 8, 1])
        with form_col:
            st.markdown(f'<img src="{LOGO_URL}" style="height:36px;object-fit:contain;display:block;margin-bottom:1.25rem;">', unsafe_allow_html=True)
            st.markdown('<h2 style="font-size:1.85rem;font-weight:700;color:#1E293B;margin:0 0 0.2rem;letter-spacing:-0.3px;">Login</h2>', unsafe_allow_html=True)
            st.markdown('<p style="color:#64748B;font-size:0.83rem;margin:0 0 1.5rem;">Enter your dashboard credentials</p>', unsafe_allow_html=True)

            with st.form("login_form"):
                st.text_input("Username", placeholder="Enter username", key="_login_user")
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
