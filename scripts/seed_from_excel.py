#!/usr/bin/env python3
"""
One-time script to import the Excel workbook into MongoDB (sync PyMongo version).

Usage:
    python scripts/seed_from_excel.py \
        --file "../Sales_Capture__Ahmedabad__2025-26.xlsx" \
        --sheet "Sales Funnel & Enquiry Capture(Apr25 To Mar26)" \
        --fy "2025-26" \
        --branch "Ahmedabad"

Set MONGODB_URI and DB_NAME in a .env file or environment variables.
"""

import argparse
import os
import sys
import logging

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient, UpdateOne
from backend.services.import_excel import load_excel

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger("seed")


def import_to_mongodb_sync(db, documents: list[dict]) -> dict:
    """Bulk upsert using PyMongo (sync). Idempotent by enquiry_no."""
    if not documents:
        return {"inserted": 0, "updated": 0, "errors": []}

    ops = [
        UpdateOne(
            {"enquiry_no": doc["enquiry_no"]},
            {"$set": doc},
            upsert=True,
        )
        for doc in documents
    ]

    result = db.enquiries.bulk_write(ops, ordered=False)
    return {
        "inserted": result.upserted_count,
        "updated": result.modified_count,
        "errors": [],
    }


def main(file_path: str, sheet_name: str, fy: str, branch: str):
    uri = os.environ.get("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.environ.get("DB_NAME", "salasar_ahmedabad")

    log.info("Connecting to MongoDB: %s", db_name)
    client = MongoClient(uri, serverSelectionTimeoutMS=10_000)
    db = client[db_name]

    # Ensure indexes
    db.enquiries.create_index("enquiry_no", unique=True)
    db.enquiries.create_index("cre_rm_accountable")
    db.enquiries.create_index("date_referred")
    db.enquiries.create_index("type_of_proposal")
    db.enquiries.create_index("business_closed")
    db.enquiries.create_index([("fy", 1), ("branch", 1)])
    log.info("Indexes ensured")

    log.info("Loading Excel: %s  (sheet: %s)", file_path, sheet_name)
    documents = load_excel(file_path, sheet_name, fy, branch)
    log.info("Parsed %d records", len(documents))

    result = import_to_mongodb_sync(db, documents)
    log.info(
        "Done — Inserted: %d, Updated: %d, Errors: %d",
        result["inserted"], result["updated"], len(result["errors"])
    )
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Seed MongoDB from Excel file")
    parser.add_argument("--file", required=True, help="Path to .xlsx file")
    parser.add_argument("--sheet", default="Sales Funnel & Enquiry Capture(Apr25 To Mar26)", help="Sheet name")
    parser.add_argument("--fy", default="2025-26", help="Financial year")
    parser.add_argument("--branch", default="Ahmedabad", help="Branch name")
    args = parser.parse_args()

    main(args.file, args.sheet, args.fy, args.branch)
