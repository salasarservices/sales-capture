"""
Management command to seed data from Excel.
Mirrors the original scripts/seed_from_excel.py logic.
"""

import openpyxl
from datetime import datetime, date
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.database import get_collection
import bleach


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


def _clean(val):
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    return bleach.clean(s)


def _to_date(val):
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


def _to_float(val):
    if val is None:
        return None
    try:
        f = float(val)
        return f if f >= 0 else None
    except (TypeError, ValueError):
        return None


def _normalize_requirement(val):
    if not val:
        return "Any Others"
    return REQUIREMENT_MAP.get(str(val).strip().lower(), "Any Others")


def _normalize_proposal_type(val):
    if not val:
        return None
    return PROPOSAL_TYPE_MAP.get(str(val).strip().lower(), None)


def _normalize_phone(val):
    if not val:
        return "0000000000"
    digits = "".join(c for c in str(val) if c.isdigit())
    if len(digits) == 10:
        return digits
    if len(digits) == 12 and digits.startswith("91"):
        return digits[2:]
    return digits[:10].ljust(10, "0")


def parse_excel_row(row_values: list, enquiry_no: int, fy: str, branch: str) -> dict:
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

    quote_submitted = "Yes" if str(quote_submitted_raw or "").strip().lower() == "yes" else "No"
    business_closed = "Yes" if str(business_closed_raw or "").strip().lower() == "yes" else "No"

    if business_closed == "No" and closure_actual is not None:
        closure_actual = None

    tentative_brokerage = round(premium_potential * 0.12, 2) if premium_potential else 0.0

    now = timezone.now()
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


class Command(BaseCommand):
    help = "Import enquiry data from Excel file into MongoDB"

    def add_arguments(self, parser):
        parser.add_argument("--file", required=True, help="Path to Excel file")
        parser.add_argument("--sheet", default="Enquiry Capture Sheet", help="Sheet name")
        parser.add_argument("--fy", default="2025-26", help="Financial year")
        parser.add_argument("--branch", default="Ahmedabad", help="Branch name")

    def handle(self, *args, **options):
        file_path = options["file"]
        sheet_name = options["sheet"]
        fy = options["fy"]
        branch = options["branch"]

        self.stdout.write(f"Loading {file_path}...")

        try:
            wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
            ws = wb[sheet_name]
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error loading file: {e}"))
            return

        rows = list(ws.iter_rows(values_only=True))
        if not rows:
            self.stdout.write(self.style.ERROR("No data found"))
            return

        data_rows = rows[1:]
        collection = get_collection("enquiries")
        inserted = 0
        updated = 0
        errors = []

        for idx, row in enumerate(data_rows):
            if all(v is None or str(v).strip() == "" for v in row):
                continue

            sr_no = row[0]
            try:
                en = int(float(str(sr_no))) if sr_no is not None else idx + 1
            except (ValueError, TypeError):
                en = idx + 1

            try:
                doc = parse_excel_row(list(row), en, fy, branch)
                result = collection.replace_one(
                    {"enquiry_no": doc["enquiry_no"]},
                    doc,
                    upsert=True,
                )
                if result.upserted_id:
                    inserted += 1
                else:
                    updated += 1
            except Exception as e:
                errors.append({"enquiry_no": en, "error": str(e)})

        wb.close()

        self.stdout.write(self.style.SUCCESS(
            f"Import complete: {inserted} inserted, {updated} updated"
        ))
        if errors:
            self.stdout.write(self.style.WARNING(f"{len(errors)} errors occurred"))
            for err in errors[:5]:
                self.stdout.write(f"  - {err}")