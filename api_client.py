"""
API client for Streamlit - calls Django REST API instead of direct MongoDB.
"""

import streamlit as st
import requests
from typing import Optional

API_BASE_URL = "http://localhost:8000/api/v1"


def get_auth_header() -> Optional[dict]:
    """Get Authorization header from session state."""
    token = st.session_state.get("access_token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return None


def api_get(endpoint: str, params: dict = None) -> dict:
    """Make GET request to API."""
    headers = get_auth_header() or {}
    response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def api_post(endpoint: str, data: dict = None) -> dict:
    """Make POST request to API."""
    headers = get_auth_header() or {}
    response = requests.post(f"{API_BASE_URL}{endpoint}", headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()


def api_put(endpoint: str, data: dict = None) -> dict:
    """Make PUT request to API."""
    headers = get_auth_header() or {}
    response = requests.put(f"{API_BASE_URL}{endpoint}", headers=headers, json=data, timeout=30)
    response.raise_for_status()
    return response.json()


def api_delete(endpoint: str) -> dict:
    """Make DELETE request to API."""
    headers = get_auth_header() or {}
    response = requests.delete(f"{API_BASE_URL}{endpoint}", headers=headers, timeout=30)
    return response


# ---------------------------------------------------------------------------
# Auth endpoints
# ---------------------------------------------------------------------------

def login(username: str, password: str) -> dict:
    """Login and store tokens in session state."""
    response = api_post("/auth/login", {"username": username, "password": password})
    st.session_state["access_token"] = response["access"]
    st.session_state["refresh_token"] = response["refresh"]
    st.session_state["user"] = response["user"]
    st.session_state["authenticated"] = True
    return response


def logout():
    """Logout and clear session."""
    try:
        refresh = st.session_state.get("refresh_token")
        if refresh:
            api_post("/auth/logout", {"refresh": refresh})
    except Exception:
        pass
    st.session_state.clear()


def refresh_access_token() -> bool:
    """Refresh access token using refresh token."""
    refresh = st.session_state.get("refresh_token")
    if not refresh:
        return False
    try:
        response = api_post("/auth/refresh", {"refresh": refresh})
        st.session_state["access_token"] = response["access"]
        return True
    except Exception:
        logout()
        return False


# ---------------------------------------------------------------------------
# Analytics endpoints
# ---------------------------------------------------------------------------

def fetch_kpis(fy: str = "2025-26", branch: str = "Ahmedabad") -> dict:
    """Get KPI summary."""
    return api_get("/analytics/kpis", {"fy": fy, "branch": branch})


def fetch_summary_sales(fy: str = "2025-26", branch: str = "Ahmedabad") -> list:
    """Get Summary: Sales Capture (View D)."""
    return api_get("/analytics/summary-sales", {"fy": fy, "branch": branch})


def fetch_summary_conversion(fy: str = "2025-26", branch: str = "Ahmedabad") -> list:
    """Get Summary: Conversion Ratio (View E)."""
    return api_get("/analytics/summary-conversion", {"fy": fy, "branch": branch})


def fetch_business_conversion(fy: str = "2025-26") -> list:
    """Get Business Conversion Ratio (View C) - monthly."""
    return api_get("/analytics/business-conversion", {"fy": fy})


def fetch_funnel_metrics(fy: str = "2025-26", branch: str = "Ahmedabad", 
                         cre_rm: list = None, type: list = None, month: list = None) -> dict:
    """Get Sales Funnel (View B) metrics."""
    params = {"fy": fy, "branch": branch}
    if cre_rm:
        params["cre_rm"] = cre_rm
    if type:
        params["type"] = type
    if month:
        params["month"] = month
    return api_get("/analytics/sales-funnel", params)


def fetch_filter_options(fy: str = "2025-26", branch: str = "Ahmedabad") -> dict:
    """Get distinct filter options for frontend."""
    return api_get("/analytics/filter-options", {"fy": fy, "branch": branch})


# ---------------------------------------------------------------------------
# Enquiry endpoints
# ---------------------------------------------------------------------------

def fetch_enquiries(fy: str = "2025-26", branch: str = "Ahmedabad",
                   page: int = 1, page_size: int = 25,
                   cre_rm: list = None, type: list = None,
                   month: list = None, company: str = None) -> dict:
    """Get paginated enquiries."""
    params = {"fy": fy, "branch": branch, "page": page, "page_size": page_size}
    if cre_rm:
        params["cre_rm"] = cre_rm
    if type:
        params["type"] = type
    if month:
        params["month"] = month
    if company:
        params["company"] = company
    return api_get("/enquiries/", params)


def create_enquiry(data: dict) -> dict:
    """Create new enquiry."""
    return api_post("/enquiries/", data)


def update_enquiry(enquiry_id: str, data: dict) -> dict:
    """Update enquiry."""
    return api_put(f"/enquiries/{enquiry_id}/", data)


def delete_enquiry(enquiry_id: str):
    """Soft delete enquiry."""
    return api_delete(f"/enquiries/{enquiry_id}/")


# ---------------------------------------------------------------------------
# User endpoints (admin only)
# ---------------------------------------------------------------------------

def create_user(username: str, password: str, role: str = "viewer") -> dict:
    """Create new user (admin only)."""
    return api_post("/users/", {"username": username, "password": password, "role": role})


# ---------------------------------------------------------------------------
# Export helpers
# ---------------------------------------------------------------------------

def export_to_csv(data: list, filename: str):
    """Export data to CSV."""
    import pandas as pd
    df = pd.DataFrame(data)
    return df.to_csv(index=False).encode("utf-8")