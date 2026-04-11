"""
Database connection - now uses Django API via api_client.
Kept for backward compatibility - queries now route through api_client.py.
"""

# This module is now a compatibility wrapper.
# All actual database operations go through api_client.py which calls Django API.
# This file is kept for backward compatibility with existing imports.

from api_client import fetch_kpis, fetch_summary_sales, fetch_summary_conversion

def get_db():
    """
    Returns a dict-like object for backward compatibility.
    Actual queries are handled by api_client.
    """
    return None  # Not used anymore - queries go through api_client