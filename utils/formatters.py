"""
Number formatting utilities — Indian numbering system (lakhs / crores).
"""


def _indian_commas(n: int) -> str:
    """Format integer with Indian comma grouping: 1,23,45,678."""
    s = str(abs(n))
    if len(s) <= 3:
        return ("-" if n < 0 else "") + s
    # Last 3 digits, then groups of 2
    result = s[-3:]
    s = s[:-3]
    while s:
        result = s[-2:] + "," + result
        s = s[:-2]
    return ("-" if n < 0 else "") + result


def format_inr(value, short: bool = False) -> str:
    """
    Format a number as Indian Rupees.
    short=True → use Cr / L abbreviation for large numbers.
    """
    if value is None:
        return "—"
    try:
        value = float(value)
    except (TypeError, ValueError):
        return "—"

    if short:
        if abs(value) >= 10_00_000:
            return f"₹{value / 10_00_000:.2f} Cr"
        if abs(value) >= 1_00_000:
            return f"₹{value / 1_00_000:.1f} L"

    return "₹" + _indian_commas(int(round(value)))


def format_pct(value, decimals: int = 1) -> str:
    if value is None:
        return "—"
    try:
        return f"{float(value):.{decimals}f}%"
    except (TypeError, ValueError):
        return "—"


def format_count(value) -> str:
    if value is None:
        return "—"
    try:
        return str(int(value))
    except (TypeError, ValueError):
        return "—"
