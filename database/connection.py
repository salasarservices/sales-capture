"""
Cached PyMongo client for Streamlit.
Reads connection details from st.secrets (mapped to .streamlit/secrets.toml).
"""

import streamlit as st
from pymongo import MongoClient
from pymongo.database import Database


@st.cache_resource(show_spinner=False)
def get_db() -> Database:
    uri = st.secrets["mongo"]["uri"]
    db_name = st.secrets["mongo"]["db_name"]
    client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
    return client[db_name]
