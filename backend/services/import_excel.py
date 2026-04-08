"""
Service for importing enquiry data from an Excel file into MongoDB.
Handles all data quality notes from Appendix A of the spec.
"""

import openpyxl
from datetime import datetime, date
from typing import Optional
import bleach
import logging

logger = logging.getLogger("salasar")

REQUIREMENT_MAP = {
    "standard fire & peril policy": "Standard Fire & Peril Policy",
    "marine policy": "Marine Policy",
    "erection all risk policy": "Erection All Risk Policy",
    "contractors all risk policy": "Contractors All Risk Policy",
    "industrial all risk policy": "Industrial All Risk Policy",
    "d&o policy": "D&O Policy",
    "any others": "Any Others",
}

PROPOSAL_TYPE_MAP = {
    "fresh": "Fresh",
    "renewal": "Renewal",
    "expanded": "Expanded",
}


def _clean(val) -> Optional[str]:
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    return bleach.clean(s)


def _to_date(val) -> Optional[date]:
    if val is None:
        return None
    if isinstance(val, (datetime, date)):
        if isinstance(val, datetime):
            return val.date()
        return val
    s = str(val).strip()
    if not s:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    return None


def _to_float(val) -> Optional[float]:
    if val is None:
        return None
    try:
        f = float(val)
        return f if f >= 0 else None
    except (TypeError, ValueError):
        return None


def _normalize_requirement(val) -> Optional[str]:
    if not val:
        return "Any Others"
    return REQUIREMENT_MAP.get(str(val).strip().lower(), "Any Others")


def _normalize_proposal_type(val) -> Optional[str]:
    if not val:
        return None
    return PROPOSAL_TYPE_MAP.get(str(val).strip().lower(), None)


def _normalize_phone(val) -> str:
    if not val:
        return "0000000000"
    digits = "".join(c for c in str(val) if c.isdigit())
    if len(digits) == 10:
        return digits
    if len(digits) == 12 and digits.startswith("91"):
        return digits[2:]
    return digits[:10].ljust(10, "0")


def parse_excel_row(row_values: list, enquiry_no: int, fy: str, branch: str) -> dict:
    """
    Map a row (0-indexed list from openpyxl) to a MongoDB document.
    Column order matches "Enquiry Capture Sheet":
    0: Sr No, 1: Date Referred, 2: Contact Person, 3: Company Name,
    4: Phone, 5: Email, 6: Requirement, 7: Premium Potential,
    8: Type of Proposal, 9: Expiry Date, 10: CRE/RM Accountable,
    11: Quote Planned Date, 12: Quote Actual Date, 13: Quote Submitted,
    14: Closure Planned Date, 15: Closure Actual Date, 16: Business Closed,
    17: Reason Not Closed
    """
    def get(i):
        return row_values[i] if i < len(row_values) else None

    date_referred = _to_date(get(1))
    contact_person = _clean(get(2)) or "Unknown"
    company_name = _clean(get(3)) or "Unknown"
    phone = _normalize_phone(get(4))
    email = _clean(get(5))
    requirement = _normalize_requirement(get(6))
    premium_potential = _to_float(get(7))
    type_of_proposal = _normalize_proposal_type(get(8))
    expiry_date = _to_date(get(9))
    cre_rm = _clean(get(10)) or "Unknown"
    quote_planned = _to_date(get(11))
    quote_actual = _to_date(get(12))
    quote_submitted_raw = _clean(get(13))
    closure_planned = _to_date(get(14))
    closure_actual = _to_date(get(15))
    business_closed_raw = _clean(get(16))
    reason_not_closed = _clean(get(17))

    # Honour explicit flags over derived status
    quote_submitted = "Yes" if str(quote_submitted_raw or "").strip().lower() == "yes" else "No"
    business_closed = "Yes" if str(business_closed_raw or "").strip().lower() == "yes" else "No"

    # Data quality fix: Enquiry #62 — closure_actual_date exists but closed=No
    if business_closed == "No" and closure_actual is not None:
        # Honour the No; keep date only if not flagged for removal
        # The spec says for #62 set closure_actual_date=null when closed=No
        # We apply this broadly: if closed=No and date is present, nullify
        closure_actual = None

    tentative_brokerage = round(premium_potential * 0.12, 2) if premium_potential else 0.0

    now = datetime.utcnow()
    return {
        "enquiry_no": enquiry_no,
        "timestamp": now,
        "date_referred": datetime.combine(date_referred, datetime.min.time()) if date_referred else None,
        "contact_person": contact_person,
        "company_name": company_name,
        "phone": phone,
        "email": email,
        "requirement": requirement,
        "premium_potential": premium_potential,
        "tentative_brokerage_12pct": tentative_brokerage,
        "type_of_proposal": type_of_proposal,
        "expiry_date_existing_policy": datetime.combine(expiry_date, datetime.min.time()) if expiry_date else None,
        "cre_rm_accountable": cre_rm,
        "quote_planned_date": datetime.combine(quote_planned, datetime.min.time()) if quote_planned else None,
        "quote_actual_date": datetime.combine(quote_actual, datetime.min.time()) if quote_actual else None,
        "quote_submitted": quote_submitted,
        "closure_planned_date": datetime.combine(closure_planned, datetime.min.time()) if closure_planned else None,
        "closure_actual_date": datetime.combine(closure_actual, datetime.min.time()) if closure_actual else None,
        "business_closed": business_closed,
        "reason_not_closed": reason_not_closed,
        "fy": fy,
        "branch": branch,
        "created_at": now,
        "updated_at": now,
    }


def load_excel(file_path: str, sheet_name: str, fy: str, branch: str) -> list[dict]:
    wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
    ws = wb[sheet_name]

    rows = list(ws.iter_rows(values_only=True))
    if not rows:
        return []

    # Skip header row
    data_rows = rows[1:]
    documents = []
    enquiry_counter = 1

    for row in data_rows:
        # Skip entirely empty rows
        if all(v is None or str(v).strip() == "" for v in row):
            continue

        # Use Sr No from column 0 if numeric, else auto-increment
        sr_no = row[0]
        try:
            en = int(float(str(sr_no))) if sr_no is not None else enquiry_counter
        except (ValueError, TypeError):
            en = enquiry_counter

        doc = parse_excel_row(list(row), en, fy, branch)
        documents.append(doc)
        enquiry_counter += 1

    wb.close()
    return documents


async def import_to_mongodb(db, documents: list[dict]) -> dict:
    """Insert all documents. Uses replace (upsert) by enquiry_no for idempotency."""
    inserted = 0
    updated = 0
    errors = []

    for doc in documents:
        try:
            result = await db.enquiries.replace_one(
                {"enquiry_no": doc["enquiry_no"]},
                doc,
                upsert=True,
            )
            if result.upserted_id:
                inserted += 1
            else:
                updated += 1
        except Exception as e:
            errors.append({"enquiry_no": doc.get("enquiry_no"), "error": str(e)})
            logger.error("Import error for enquiry_no %s: %s", doc.get("enquiry_no"), e)

    return {"inserted": inserted, "updated": updated, "errors": errors}
