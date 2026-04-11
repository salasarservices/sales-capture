"""
Database queries - now uses Django API instead of direct MongoDB.
Keeps all original function signatures and logic intact.
"""

import pandas as pd
from typing import Optional
from api_client import (
    fetch_kpis as api_fetch_kpis,
    fetch_summary_sales as api_fetch_summary_sales,
    fetch_summary_conversion as api_fetch_summary_conversion,
    fetch_business_conversion as api_fetch_business_conversion,
    fetch_funnel_metrics as api_fetch_funnel_metrics,
    fetch_filter_options as api_fetch_filter_options,
    fetch_enquiries as api_fetch_enquiries,
)

FY = "2025-26"
BRANCH = "Ahmedabad"

FISCAL_MONTH_ORDER = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]
FISCAL_LABELS = {
    4: "Apr'25", 5: "May'25", 6: "Jun'25", 7: "Jul'25",
    8: "Aug'25", 9: "Sep'25", 10: "Oct'25", 11: "Nov'25",
    12: "Dec'25", 1: "Jan'26", 2: "Feb'26", 3: "Mar'26"
}


def fetch_kpis(db=None, fy: str = FY, branch: str = BRANCH) -> dict:
    """Fetch KPI summary from API. db parameter kept for backward compatibility."""
    return api_fetch_kpis(fy, branch)


def fetch_summary_sales(db=None, fy: str = FY, branch: str = BRANCH) -> pd.DataFrame:
    """Fetch Summary: Sales Capture (View D) from API."""
    rows = api_fetch_summary_sales(fy, branch)
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


def fetch_business_conversion(db=None, fy: str = FY) -> pd.DataFrame:
    """Fetch Business Conversion Ratio (View C) - monthly from API."""
    rows = api_fetch_business_conversion(fy)
    
    # Build a complete 12-month scaffold
    if not rows:
        records = []
        for month_num in FISCAL_MONTH_ORDER:
            records.append({
                "Month": FISCAL_LABELS[month_num],
                "No. of Enquiries": 0,
                "Business Converted": 0,
                "Conversion %": 0.0,
            })
        df = pd.DataFrame(records)
    else:
        # API already returns full 12 months
        df = pd.DataFrame(rows)
        df.rename(columns={
            "Month": "Month",
            "No. of Enquiries": "No. of Enquiries",
            "Business Converted": "Business Converted",
            "Conversion %": "Conversion %",
        }, inplace=True)
    
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


def fetch_summary_conversion(db=None, fy: str = FY, branch: str = BRANCH) -> pd.DataFrame:
    """Fetch Summary: Conversion Ratio (View E) from API."""
    rows = api_fetch_summary_conversion(fy, branch)
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


def fetch_funnel_metrics(fy: str = FY, branch: str = BRANCH,
                         extra_match: Optional[dict] = None) -> dict:
    """Fetch Sales Funnel (View B) metrics from API."""
    cre_rm = extra_match.get("cre_rm") if extra_match else None
    type_ = extra_match.get("type") if extra_match else None
    month = extra_match.get("month") if extra_match else None
    
    return api_fetch_funnel_metrics(fy, branch, cre_rm, type_, month)


def fetch_enquiries(
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
    """Return (paginated DataFrame, total_count) from API."""
    result = api_fetch_enquiries(
        fy=fy,
        branch=branch,
        page=page,
        page_size=page_size,
        cre_rm=cre_rms,
        type=proposal_types,
        month=months,
        company=company_search,
    )
    
    total = result.get("count", 0)
    results = result.get("results", [])
    
    if not results:
        return pd.DataFrame(), total
    
    df = pd.DataFrame(results)
    df.drop(columns=["_id", "timestamp", "created_at", "updated_at", "fy", "branch"], errors="ignore", inplace=True)
    
    # Column names — exact headings from master Excel sheet, in Excel column order
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
    
    # Format all date columns as DD-MM-YYYY strings
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


def fetch_filter_options(fy: str = FY, branch: str = BRANCH) -> dict:
    """Get distinct filter options for frontend from API."""
    return api_fetch_filter_options(fy, branch)