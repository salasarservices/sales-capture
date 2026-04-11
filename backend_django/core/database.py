"""
MongoDB connection for Django.
Uses pymongo directly (no ORM) - keeps existing logic intact.
"""

import os
from pymongo import MongoClient
from pymongo.database import Database
from django.conf import settings

_client = None
_db = None


def get_mongo_client() -> MongoClient:
    """Get or create MongoDB client (singleton)."""
    global _client
    if _client is None:
        _client = MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=10000)
    return _client


def get_mongo_db() -> Database:
    """Get MongoDB database instance."""
    global _db
    if _db is None:
        client = get_mongo_client()
        _db = client[settings.DB_NAME]
    return _db


def get_collection(name: str):
    """Get a MongoDB collection by name."""
    db = get_mongo_db()
    return db[name]