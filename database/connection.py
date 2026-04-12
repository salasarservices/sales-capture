"""
Database connection - direct MongoDB using pymongo.
"""

import streamlit as st
from pymongo import MongoClient
from pymongo.database import Database


def get_db() -> Database:
    """Get MongoDB database instance from streamlit secrets."""
    if "mongo" not in st.secrets:
        raise ValueError("MongoDB configuration not found in secrets")
    
    uri = st.secrets["mongo"]["uri"]
    db_name = st.secrets["mongo"]["db_name"]
    
    @st.cache_resource(show_spinner=False)
    def _connect():
        client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
        return client[db_name]
    
    return _connect()