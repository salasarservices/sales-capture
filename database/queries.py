"""
Database queries - direct MongoDB access.
All original aggregation logic preserved.
"""

import sys
import os
import pandas as pd
from typing import Optional

# Import aggregations from original backend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from backend.services.aggregations import (
    summary_sales_pipeline,
    business_conversion_pipeline,
    summary_conversion_pipeline,
    sales_funnel_pipeline,
    kpi_pipeline,
    FISCAL_MONTH_ORDER,
    FISCAL_LABELS,
)

FY = "2025-26"
BRANCH = "Ahmedabad"


def fetch_kpis(
    db,
    fy: str = FY,
    branch: str = BRANCH,
    cre_rms: Optional[list] = None,
    proposal_types: Optional[list] = None,
    requirements: Optional[list] = None,
    months: Optional[list] = None,
) -> dict:
    """Fetch KPI summary from MongoDB."""
    extra_match = {}
    if cre_rms:
        extra_match["cre_rm_accountable"] = {"$in": cre_rms}
    if proposal_types:
        extra_match["type_of_proposal"] = {"$in": proposal_types}
    if requirements:
        extra_match["requirement"] = {"$in": requirements}
    if months:
        extra_match["$expr"] = {"$in": [{"$month": "$date_referred"}, months]}
    pipeline = kpi_pipeline(fy, branch, extra_match=extra_match if extra_match else None)
    result = list(db.enquiries.aggregate(pipeline))
    if not result:
        return {
            "total_enquiries": 0,
            "total_converted": 0,
            "overall_conversion_rate": 0.0,
            "total_premium_converted": 0.0,
            "total_brokerage_converted": 0.0,
        }
    r = result[0]
    r.pop("_id", None)
    return r


def fetch_summary_sales(
    db,
    fy: str = FY,
    branch: str = BRANCH,
    cre_rms: Optional[list] = None,
    proposal_types: Optional[list] = None,
    requirements: Optional[list] = None,
    months: Optional[list] = None,
) -> pd.DataFrame:
    """Fetch Summary: Sales Capture (View D)."""
    extra_match = {}
    if cre_rms:
        extra_match["cre_rm_accountable"] = {"$in": cre_rms}
    if proposal_types:
        extra_match["type_of_proposal"] = {"$in": proposal_types}
    if requirements:
        extra_match["requirement"] = {"$in": requirements}
    if months:
        extra_match["$expr"] = {"$in": [{"$month": "$date_referred"}, months]}
    pipeline = summary_sales_pipeline(fy, branch, extra_match=extra_match if extra_match else None)
    rows = list(db.enquiries.aggregate(pipeline))
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows)
    df.rename(columns={"_id": "CRE / RM"}, inplace=True)
    df.rename(columns={
        "total_enquiries": "Total Enquiries",
        "business_converted": "Converted",
        "total_premium_converted": "Premium Converted (₹)",
        "business_not_converted": "Not Converted",
        "pct_not_converted": "% Not Converted",
    }, inplace=True)
    
    # Totals row
    totals = {
        "CRE / RM": "TOTAL",
        "Total Enquiries": df["Total Enquiries"].sum(),
        "Converted": df["Converted"].sum(),
        "Premium Converted (₹)": df["Premium Converted (₹)"].sum(),
        "Not Converted": df["Not Converted"].sum(),
        "% Not Converted": (
            df["Not Converted"].sum() / df["Total Enquiries"].sum() * 100
            if df["Total Enquiries"].sum() > 0 else 0.0
        ),
    }
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
    return df


def fetch_business_conversion(
    db,
    fy: str = FY,
    branch: str = BRANCH,
    cre_rms: Optional[list] = None,
    proposal_types: Optional[list] = None,
    requirements: Optional[list] = None,
    months: Optional[list] = None,
) -> pd.DataFrame:
    """Fetch Business Conversion Ratio (View C) - monthly."""
    extra_match = {"branch": branch}
    if cre_rms:
        extra_match["cre_rm_accountable"] = {"$in": cre_rms}
    if proposal_types:
        extra_match["type_of_proposal"] = {"$in": proposal_types}
    if requirements:
        extra_match["requirement"] = {"$in": requirements}
    if months:
        extra_match["$expr"] = {"$in": [{"$month": "$date_referred"}, months]}
    pipeline = business_conversion_pipeline(fy, extra_match=extra_match if extra_match else None)
    rows = list(db.enquiries.aggregate(pipeline))
    
    # Build a complete 12-month scaffold
    scaffold = {
        m: {"no_of_enquiries": 0, "business_converted": 0, "percentage_converted": 0.0}
        for m in FISCAL_MONTH_ORDER
    }
    
    for r in rows:
        m = r["_id"]["month"]
        if m in scaffold:
            scaffold[m] = {
                "no_of_enquiries": r["no_of_enquiries"],
                "business_converted": r["business_converted"],
                "percentage_converted": r["percentage_converted"],
            }
    
    records = []
    for month_num in FISCAL_MONTH_ORDER:
        d = scaffold[month_num]
        records.append({
            "Month": FISCAL_LABELS[month_num],
            "No. of Enquiries": d["no_of_enquiries"],
            "Business Converted": d["business_converted"],
            "Conversion %": round(d["percentage_converted"], 1),
        })
    
    df = pd.DataFrame(records)
    
    # Totals row
    total_enq = df["No. of Enquiries"].sum()
    total_conv = df["Business Converted"].sum()
    totals = {
        "Month": "TOTAL",
        "No. of Enquiries": total_enq,
        "Business Converted": total_conv,
        "Conversion %": round(total_conv / total_enq * 100, 1) if total_enq > 0 else 0.0,
    }
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
    return df


def fetch_summary_conversion(
    db,
    fy: str = FY,
    branch: str = BRANCH,
    cre_rms: Optional[list] = None,
    proposal_types: Optional[list] = None,
    requirements: Optional[list] = None,
    months: Optional[list] = None,
) -> pd.DataFrame:
    """Fetch Summary: Conversion Ratio (View E)."""
    extra_match = {}
    if cre_rms:
        extra_match["cre_rm_accountable"] = {"$in": cre_rms}
    if proposal_types:
        extra_match["type_of_proposal"] = {"$in": proposal_types}
    if requirements:
        extra_match["requirement"] = {"$in": requirements}
    if months:
        extra_match["$expr"] = {"$in": [{"$month": "$date_referred"}, months]}
    pipeline = summary_conversion_pipeline(fy, branch, extra_match=extra_match if extra_match else None)
    rows = list(db.enquiries.aggregate(pipeline))
    if not rows:
        return pd.DataFrame()
    
    df = pd.DataFrame(rows)
    df.rename(columns={"_id": "CRE / RM"}, inplace=True)
    
    # Totals row
    num_cols = [c for c in df.columns if c != "CRE / RM"]
    totals = {"CRE / RM": "TOTAL"}
    for c in num_cols:
        if c in df.columns:
            totals[c] = df[c].sum()
    
    # Recalculate percentage columns in totals row
    def safe_pct(num, den):
        return round(num / den * 100, 1) if den > 0 else 0.0
    
    totals["fresh_pct"] = safe_pct(totals.get("fresh_converted", 0), totals.get("fresh_total", 0))
    totals["renewal_pct"] = safe_pct(totals.get("renewal_converted", 0), totals.get("renewal_total", 0))
    totals["expanded_pct"] = safe_pct(totals.get("expanded_converted", 0), totals.get("expanded_total", 0))
    totals["pct_not_converted"] = safe_pct(totals.get("total_not_converted", 0), totals.get("total_enquiries", 0))
    
    df = pd.concat([df, pd.DataFrame([totals])], ignore_index=True)
    return df


def fetch_funnel_metrics(db, fy: str = FY, branch: str = BRANCH,
                         extra_match: Optional[dict] = None) -> dict:
    """Fetch Sales Funnel (View B) metrics."""
    pipeline = sales_funnel_pipeline(fy, branch, extra_match)
    result = list(db.enquiries.aggregate(pipeline))
    if not result:
        return {"total_enquiries": 0, "quote_submitted": 0, "business_closed": 0}
    r = result[0]
    r.pop("_id", None)
    return r


def fetch_enquiries(
    db,
    fy: str = FY,
    branch: str = BRANCH,
    months: Optional[list] = None,
    cre_rms: Optional[list] = None,
    proposal_types: Optional[list] = None,
    requirements: Optional[list] = None,
    company_search: str = "",
    page: int = 1,
    page_size: int = 25,
) -> tuple[pd.DataFrame, int]:
    """Return (paginated DataFrame, total_count)."""
    match: dict = {"fy": fy, "branch": branch}
    
    if months:
        match["$expr"] = {"$in": [{"$month": "$date_referred"}, months]}
    if cre_rms:
        match["cre_rm_accountable"] = {"$in": cre_rms}
    if proposal_types:
        match["type_of_proposal"] = {"$in": proposal_types}
    if requirements:
        match["requirement"] = {"$in": requirements}
    if company_search:
        import re
        match["company_name"] = {"$regex": re.escape(company_search), "$options": "i"}
    
    total = db.enquiries.count_documents(match)
    skip = (page - 1) * page_size
    
    cursor = (
        db.enquiries
        .find(match)
        .sort([("enquiry_no", 1)])
        .skip(skip)
        .limit(page_size)
    )
    
    rows = list(cursor)
    if not rows:
        return pd.DataFrame(), total
    
    df = pd.DataFrame(rows)
    df.drop(columns=["_id", "timestamp", "created_at", "updated_at", "fy", "branch"], errors="ignore", inplace=True)
    
    # Column names — exact headings from master Excel sheet
    col_map = {
        "date_referred": "Date (When The Proposal Referred To The Company)",
        "enquiry_no": "Enquiry No.",
        "contact_person": "Name of the Contact Person",
        "company_name": "Company Name",
        "phone": "Phone No.",
        "email": "E-Mail",
        "requirement": "Requirement",
        "premium_potential": "Premium Potential",
        "type_of_proposal": "Type Of Proposal",
        "expiry_date_existing_policy": "Expiry Date Of Existing Policy (If Renewal)",
        "cre_rm_accountable": "CRE(Expanded) / RM(New) Accountable",
        "tentative_brokerage_12pct": "Tentative Brokerage (12%)",
        "quote_planned_date": "Quote Submission Date — Planned Date",
        "quote_actual_date": "Quote Submission Date — Actual Date",
        "quote_submitted": "Quote Submitted",
        "closure_planned_date": "Actual Closure Date — Planned Date",
        "closure_actual_date": "Actual Closure Date — Actual Date",
        "business_closed": "Business Closed",
        "reason_not_closed": "Reason For Sales Not Closed",
    }
    df.rename(columns=col_map, inplace=True)
    
    # Enforce Excel column order
    ordered_cols = [c for c in col_map.values() if c in df.columns]
    df = df[ordered_cols]
    
    # Format date columns as DD-MM-YYYY strings
    date_cols = [
        "Date (When The Proposal Referred To The Company)",
        "Expiry Date Of Existing Policy (If Renewal)",
        "Quote Submission Date — Planned Date",
        "Quote Submission Date — Actual Date",
        "Actual Closure Date — Planned Date",
        "Actual Closure Date — Actual Date",
    ]
    for col in date_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce").dt.strftime("%d-%m-%Y")
    
    return df, total


def fetch_filter_options(db, fy: str = FY, branch: str = BRANCH) -> dict:
    """Get distinct filter options for frontend."""
    base = {"fy": fy, "branch": branch}
    cre_rms = sorted([x for x in db.enquiries.distinct("cre_rm_accountable", base) if x])
    proposal_types = sorted([x for x in db.enquiries.distinct("type_of_proposal", base) if x])
    requirements = sorted([x for x in db.enquiries.distinct("requirement", base) if x])
    return {
        "cre_rms": cre_rms,
        "proposal_types": proposal_types,
        "requirements": requirements,
    }
