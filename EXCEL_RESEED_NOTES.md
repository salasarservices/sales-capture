# Excel Re-seed Notes

## What We Know

### Source File
`C:\Users\Aritro\Desktop\Sales Capture (Ahmedabad) 2025-26.xlsx`

### Correct Sheet Name
From the screenshot, the main data sheet is:
**`Sales Funnel & Enquiry Capture(Apr25 To Mar26)`**
(NOT "Enquiry Capture Sheet" which is what the seed script defaults to)

---

## Data Discrepancy Found

| Month | Sheet | Dashboard (MongoDB) |
|---|---|---|
| Apr'25 | 45 enquiries, 44 converted (98%) | 1 enquiry, 1 converted (100%) |
| May'25 | 45 enquiries, 27 converted (60%) | 1 enquiry, 1 converted (100%) |
| Jun'25 | 45, 27 (60%) | 27, 26 (96.3%) |
| Jan'26 | 1, **20 (2000%)** ← impossible | 20, 20 (100%) |
| **TOTAL** | **408, 320 (78%)** | **239, 236 (98.7%)** |

**MongoDB is missing ~169 records** — it was seeded once and never updated.

---

## Google Sheet Formula Errors (Already Identified)

1. **Jan, Feb, Mar '26 show 2000% conversion** — impossible.
   - The `Count(Q)` formula for Business Converted is not applying the year filter correctly for those months.
   - It counts converted records across all years instead of just 2026.

2. **Apr–Dec all show exactly 45 enquiries** — suspiciously uniform.
   - Likely the month filter in the Google Sheet is not working and returning cached/all-data.

---

## What Needs To Be Done

### Step 1 — Re-seed MongoDB

Run in your terminal:

```bash
cd C:\Users\Aritro\sales-capture

python scripts/seed_from_excel.py \
  --file "C:\Users\Aritro\Desktop\Sales Capture (Ahmedabad) 2025-26.xlsx" \
  --sheet "Sales Funnel & Enquiry Capture(Apr25 To Mar26)" \
  --fy "2025-26" \
  --branch "Ahmedabad"
```

> If the sheet name has spaces or special characters, wrap it in quotes exactly as above.

### Step 2 — Verify Record Count

After seeding, check the count matches what the sheet shows (should be ~408 or actual row count).

### Step 3 — If Sheet Name Is Wrong

Open the Excel file, note the EXACT sheet tab name and replace `--sheet` value accordingly.

---

## Seed Script Location
`C:\Users\Aritro\sales-capture\scripts\seed_from_excel.py`

The script is **idempotent** — running it again will upsert (update existing + insert new) by `enquiry_no`, so no duplicates will be created.

---

## After Re-seed — Dashboard Notes To Add (Pending)

Once data is verified, error/warning notes need to be added to each dashboard page for any discrepancies found in the master sheet. This is still pending until the Excel file can be read and analyzed.

Pages that need notes:
- `pages/business_conversion.py`
- `pages/sales_capture.py`
- `pages/conversion_ratio.py`
- `pages/master_data.py`
