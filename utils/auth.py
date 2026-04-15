"""
Authentication utilities for Streamlit.
Credentials stored in st.secrets["credentials"].

Styling approach:
  • Raw <style> injection for Streamlit-internal selectors (.stApp gradient,
    [data-testid="stForm"] glassmorphism, input/button widget overrides) — these
    cannot be reached by Tailwind utility classes.
  • HTML elements rendered via st.markdown() (logo, title, error alert, footer)
    use Tailwind utility classes directly, since tw.initialize_tailwind() is
    called globally in app.py.
"""

import streamlit as st
import bcrypt

LOGO_URL = "https://ik.imagekit.io/salasarservices/Salasar-Logo-new.png"

# ── Raw CSS for Streamlit-internal selectors ─────────────────────────────────
_LOGIN_INTERNAL_CSS = """
<style>
/* ── Hide sidebar on login ──────────────────────────────────────────────────── */
[data-testid="stSidebar"],
[data-testid="stSidebarCollapsedControl"] { display: none !important; }

/* ── Full-screen gradient background (not achievable with Tailwind alone) ────── */
.stApp {
    background: linear-gradient(135deg,
        #5CC8BE 0%,
        #6BAABF 25%,
        #8A9EBB 50%,
        #A89080 75%,
        #C8956A 100%) !important;
}

.main .block-container {
    padding-top: 8vh !important;
    padding-bottom: 4vh !important;
    max-width: 100% !important;
}

/* ── Glassmorphism card (the Streamlit <form> element) ──────────────────────── */
[data-testid="stForm"] {
    background: rgba(255, 255, 255, 0.14) !important;
    backdrop-filter: blur(24px) !important;
    -webkit-backdrop-filter: blur(24px) !important;
    border: 1px solid rgba(255, 255, 255, 0.22) !important;
    border-radius: 20px !important;
    padding: 44px 40px 36px !important;
    box-shadow: 0 24px 64px rgba(0, 0, 0, 0.22) !important;
}
[data-testid="stForm"] label { display: none !important; }
[data-testid="stForm"] .stTextInput { margin-bottom: 12px; }

/* ── Input fields ────────────────────────────────────────────────────────────── */
[data-testid="stForm"] .stTextInput > div > div > input {
    background: rgba(240, 244, 248, 0.92) !important;
    border: 1px solid rgba(255, 255, 255, 0.4) !important;
    border-radius: 10px !important;
    color: #1A1F36 !important;
    padding: 14px 16px !important;
    font-size: 14px !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08) !important;
}
[data-testid="stForm"] .stTextInput > div > div > input::placeholder {
    color: #9AA3AF !important;
}
[data-testid="stForm"] .stTextInput > div > div > input:focus {
    border-color: rgba(255, 255, 255, 0.7) !important;
    background: rgba(255, 255, 255, 0.98) !important;
    box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.2) !important;
}

/* ── Sign In button ──────────────────────────────────────────────────────────── */
[data-testid="stFormSubmitButton"] > button {
    background: #2C3344 !important;
    color: #FFFFFF !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 15px !important;
    padding: 15px !important;
    width: 100% !important;
    margin-top: 6px !important;
    box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    letter-spacing: 0.3px;
    transition: all 0.25s ease;
}
[data-testid="stFormSubmitButton"] > button:hover {
    background: #1E2535 !important;
    transform: translateY(-1px);
    box-shadow: 0 8px 22px rgba(0, 0, 0, 0.3);
}
</style>
"""


def _verify_password(plain: str, hashed: str) -> bool:
    """Verify a plain-text password against a bcrypt hash."""
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False


def is_authenticated() -> bool:
    """Return True if the current session has passed authentication."""
    return st.session_state.get("authenticated", False)


def is_admin() -> bool:
    """Return True if the current user holds the admin role."""
    return st.session_state.get("role") == "admin"


def require_auth() -> None:
    """Gate: show login form and stop execution if not authenticated."""
    if not is_authenticated():
        login_form()
        st.stop()


def login_form() -> bool:
    """Render the glassmorphism login form.

    CSS for Streamlit-internal widget selectors is injected as raw HTML.
    Content HTML (logo, title, error alert, footer) uses Tailwind classes.
    """
    if st.session_state.get("authenticated"):
        return True

    st.markdown(_LOGIN_INTERNAL_CSS, unsafe_allow_html=True)

    # Two side gutters + narrow centred card column
    _, card_col, _ = st.columns([2, 1.5, 2])

    with card_col:
        with st.form("login_form", clear_on_submit=True):

            # Logo — Tailwind: centered, bottom margin
            st.markdown(
                f'<div class="text-center mb-5">'
                f'<img src="{LOGO_URL}" alt="Salasar" '
                f'class="w-[250px]" '
                f'style="filter:brightness(0) invert(1);opacity:0.96;">'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Title — Tailwind: centered, white, semibold, bottom margin
            st.markdown(
                '<h1 class="text-center text-white text-xl font-bold mb-6 tracking-wide m-0" '
                'style="text-shadow:0 2px 6px rgba(0,0,0,0.15);">'
                'Sales Capture Dashboard - Ahmedabad</h1>',
                unsafe_allow_html=True,
            )

            # Inputs (styled via _LOGIN_INTERNAL_CSS targeting [data-testid="stForm"] inputs)
            username  = st.text_input("Username", placeholder="Username")
            password  = st.text_input("Password", placeholder="Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)

            # Error alert from previous attempt — Tailwind: translucent red bg/border, white text
            if st.session_state.get("_login_error"):
                st.markdown(
                    f'<div class="mt-[10px] px-4 py-3 rounded-[10px] text-white text-[13px] text-center" '
                    f'style="background:rgba(255,100,100,0.18);border:1px solid rgba(255,100,100,0.28);">'
                    f'{st.session_state["_login_error"]}</div>',
                    unsafe_allow_html=True,
                )

            # Footer — Tailwind: centered, muted white, small, top border
            st.markdown(
                '<div class="text-center text-[11px] mt-7 pt-4" '
                'style="color:rgba(255,255,255,0.5);border-top:1px solid rgba(255,255,255,0.15);">'
                '&copy; Salasar Services (Insurance Brokers) Pvt. Ltd 2026</div>',
                unsafe_allow_html=True,
            )

        # Handle submission after the form block
        if submitted:
            st.session_state.pop("_login_error", None)
            if not username or not password:
                st.session_state["_login_error"] = "Please enter both username and password"
                st.rerun()
            else:
                try:
                    user_cfg = st.secrets["credentials"].get(username)
                except Exception:
                    user_cfg = None

                if user_cfg and _verify_password(password, user_cfg.get("password_hash", "")):
                    st.session_state["authenticated"] = True
                    st.session_state["username"]      = username
                    st.session_state["role"]          = user_cfg.get("role", "viewer")
                    st.session_state.pop("_login_error", None)
                    st.rerun()
                else:
                    st.session_state["_login_error"] = "Invalid username or password"
                    st.rerun()

    return False


def logout() -> None:
    """Clear session state and rerun to show the login form."""
    for key in ["authenticated", "username", "role"]:
        st.session_state.pop(key, None)
    st.rerun()
