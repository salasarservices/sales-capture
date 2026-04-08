"""
Fiscal year / month helpers for FY 2025-26 (April–March).
"""

FISCAL_MONTH_ORDER = [4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3]

FISCAL_LABELS = {
    4: "Apr'25", 5: "May'25", 6: "Jun'25",  7: "Jul'25",
    8: "Aug'25", 9: "Sep'25", 10: "Oct'25", 11: "Nov'25",
    12: "Dec'25", 1: "Jan'26", 2: "Feb'26",  3: "Mar'26",
}

# Reverse: label → month number (for filter mapping)
LABEL_TO_MONTH = {v: k for k, v in FISCAL_LABELS.items()}


def month_label_to_int(label: str) -> int:
    """Convert 'Apr\\'25' → 4."""
    return LABEL_TO_MONTH.get(label, 0)


def all_fiscal_labels() -> list[str]:
    return [FISCAL_LABELS[m] for m in FISCAL_MONTH_ORDER]
