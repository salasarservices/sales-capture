"""
Session-state based authentication for Streamlit.
Credentials are stored in st.secrets["credentials"].
"""

import streamlit as st
import bcrypt

LOGO_URL = "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"

_FEATURES = [
    ("📊", "Sales Analytics", "Live conversion and pipeline visibility"),
    ("👥", "CRE / RM Tracking", "Performance split by accountable owner"),
    ("📅", "Monthly Trends", "Fiscal-month conversion trend analysis"),
    ("🔍", "Enquiry Drilldown", "Searchable and filterable enquiry records"),
]


def _verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def login_form() -> bool:
    """
    Render the split-layout login page.
    Returns True if the user is already authenticated.
    Sets st.session_state.authenticated / .username / .role on success.
    """
    from utils.styles import inject_login_css
    inject_login_css()

    if st.session_state.get("authenticated"):
        return True

    # ── Two-column split layout ────────────────────────────────────────────
    left_col, right_col = st.columns([5, 7])

    # ── LEFT: brand panel ──────────────────────────────────────────────────
    with left_col:
        feature_items = "".join(
            f"""
            <div style="display:flex; align-items:flex-start; gap:1rem;">
                <div style="
                    width:40px; height:40px; flex-shrink:0;
                    background:rgba(255,255,255,0.12);
                    display:flex; align-items:center;
                    justify-content:center; font-size:1.15rem;
                ">{ icon }</div>
                <div>
                    <div style="color:#FFFFFF; font-weight:600; font-size:0.93rem; margin-bottom:0.15rem;">{ title }</div>
                    <div style="color:rgba(255,255,255,0.52); font-size:0.78rem; line-height:1.4;">{ desc }</div>
                </div>
            </div>
            """
            for icon, title, desc in _FEATURES
        )

        st.markdown(
            f"""<div style="
display:flex; flex-direction:column; gap:0; color:white;
min-height:calc(100vh - 6rem);
">
    <div style="margin-bottom:3.5rem;">
        <img src="{LOGO_URL}"
             style="height:48px; object-fit:contain;
                    filter:brightness(0) invert(1); opacity:0.92;">
    </div>

    <div style="margin-bottom:3rem;">
        <h1 style="
            color:#FFFFFF; font-size:2.5rem; font-weight:800;
            line-height:1.15; margin:0 0 0.75rem; letter-spacing:-0.5px;
        ">Sales Enquiry<br>Dashboard</h1>
        <p style="color:rgba(255,255,255,0.60); font-size:0.97rem; margin:0;">
            Salasar Services &nbsp;·&nbsp; Ahmedabad Branch &nbsp;·&nbsp; FY 2025-26
        </p>
    </div>

    <div style="display:flex; flex-direction:column; gap:1.5rem; flex:1;">
        {feature_items}
    </div>

    <div style="
        margin-top:3rem;
        color:rgba(255,255,255,0.28);
        font-size:0.72rem;
    ">© 2025 Salasar Services · Ahmedabad</div>
</div>""",
            unsafe_allow_html=True,
        )

    # ── RIGHT: form panel ──────────────────────────────────────────────────
    with right_col:
        # Vertical centering: spacer → heading → form
        st.markdown("<div style='height:18vh'></div>", unsafe_allow_html=True)

        # Horizontal centering via nested columns
        _, form_col, _ = st.columns([1, 7, 1])
        with form_col:
            # Logo above heading
            st.markdown(
                f"""<div style="margin-bottom:1.75rem;">
    <img src="{LOGO_URL}" style="height:44px; object-fit:contain;">
</div>
<h2 style="
    font-size:2rem; font-weight:700; color:#1E293B;
    margin:0 0 0.3rem; letter-spacing:-0.5px;
">Login</h2>
<p style="color:#64748B; margin:0 0 1.75rem; font-size:0.88rem;">
    Enter your dashboard credentials
</p>""",
                unsafe_allow_html=True,
            )

            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input(
                    "Password", type="password", placeholder="••••••••"
                )
                submitted = st.form_submit_button("SIGN IN", use_container_width=True)

        if submitted:
            try:
                user_cfg = st.secrets["credentials"][username]
            except (KeyError, Exception):
                user_cfg = None

            if user_cfg and _verify_password(password, user_cfg["password_hash"]):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = user_cfg.get("role", "viewer")
                st.rerun()
            else:
                with form_col:
                    st.error("Invalid username or password.")

    return False


def render_sidebar_branding() -> None:
    """Render standard authenticated sidebar branding and sign-out controls."""
    with st.sidebar:
        st.markdown(
            f"""
            <div style="padding: 0.9rem 0 0.5rem 0;">
                <img src="{LOGO_URL}"
                     style="height: 42px; object-fit: contain;
                            filter: brightness(0) invert(1); opacity: 0.88;
                            display: block;">
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.divider()

        role_label = "Admin" if is_admin() else "Viewer"
        st.markdown(
            f"""
            <div style="
                display:flex; align-items:center; gap:0.55rem;
                padding:0.45rem 0 0.6rem 0;
            ">
                <div style="
                    width:30px; height:30px;
                    background:rgba(255,255,255,0.11);
                    border-radius:50%;
                    display:flex; align-items:center;
                    justify-content:center; font-size:0.9rem; flex-shrink:0;
                ">👤</div>
                <div>
                    <div style="color:#FFFFFF; font-size:0.84rem; font-weight:600;">
                        {st.session_state.username}
                    </div>
                    <div style="color:rgba(255,255,255,0.46); font-size:0.69rem;">
                        {role_label}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if st.button("Sign Out", use_container_width=True):
            logout()


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
