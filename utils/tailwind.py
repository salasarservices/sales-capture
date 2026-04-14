"""Tailwind helpers for Streamlit via st_tailwind."""

from __future__ import annotations

import streamlit as st

try:
    import st_tailwind as tw
    from st_tailwind import tw_wrap
except ImportError:  # graceful fallback when dependency is unavailable
    tw = None
    tw_wrap = None


def initialize_tailwind() -> None:
    """Initialize Tailwind runtime once per session."""
    if tw is None:
        return
    if not st.session_state.get("_tailwind_initialized"):
        tw.initialize_tailwind()
        st.session_state["_tailwind_initialized"] = True


def tw_button(label: str, *, classes: str, **kwargs):
    """Render a Tailwind-styled Streamlit button with fallback."""
    if tw_wrap is None:
        return st.button(label, **kwargs)
    return tw_wrap(st.button, classes=classes)(label, **kwargs)
