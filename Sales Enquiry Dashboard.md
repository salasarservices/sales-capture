

# Sales Dashboard — Ahmedabad FY 2025-26
### Technical Specification: Python + MongoDB + GitHub

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Data Architecture & MongoDB Schema](#2-data-architecture--mongodb-schema)
3. [Business Logic & Derived Calculations](#3-business-logic--derived-calculations)
4. [Dashboard Views & Visualizations](#4-dashboard-views--visualizations)
5. [Backend: Python API Design](#5-backend-python-api-design)
6. [Frontend: UI/UX Specification](#6-frontend-uiux-specification)
7. [Security Protocols](#7-security-protocols)
8. [Project File Structure](#8-project-file-structure)
9. [Environment & Dependency Setup](#9-environment--dependency-setup)

---

## 1. Project Overview

### Context
Salasar Services (Ahmedabad branch) tracks a sales pipeline — from raw enquiry capture through quote submission, closure, and post-sale analysis. The Excel workbook contains **326 live records** (FY Apr 2025 – Mar 2026) across five interrelated views. The dashboard must ingest master data into MongoDB, auto-compute all summary and analytics views, and render them in a browser-based UI.

### Source Workbook → Dashboard Mapping

| Excel Sheet | Dashboard View | Data Source |
|---|---|---|
| `Enquiry Capture Sheet` | Master Data (raw, write-enabled) | MongoDB `enquiries` collection |
| `Sales Funnel & Enquiry Capture` | Sales Funnel Detail View | Computed from `enquiries` |
| `Business Conversion Ratio` | Business Conversion Ratio | Computed from `enquiries` |
| `Summary(Sales Capture 25-26)` | Summary: Sales Capture | Computed from `enquiries` |
| `Summary(Conversion Ratio 25-26)` | Summary: Conversion Ratio | Computed from `enquiries` |

---

## 2. Data Architecture & MongoDB Schema

### 2.1 Database: `salasar_ahmedabad`

#### Collection: `enquiries` (Master Data)
Every row from "Enquiry Capture Sheet" maps to one document.

```json
{
  "_id": "ObjectId (auto)",
  "enquiry_no": 1,
  "timestamp": "ISODate",
  "date_referred": "ISODate",
  "contact_person": "string",
  "company_name": "string",
  "phone": "string",
  "email": "string",
  "requirement": "string",
  "premium_potential": 46000.0,
  "type_of_proposal": "Fresh | Renewal | Expanded",
  "expiry_date_existing_policy": "ISODate | null",
  "cre_rm_accountable": "string",
  "tentative_brokerage_12pct": 5520.0,
  "quote_planned_date": "ISODate | null",
  "quote_actual_date": "ISODate | null",
  "quote_submitted": "Yes | No",
  "closure_planned_date": "ISODate | null",
  "closure_actual_date": "ISODate | null",
  "business_closed": "Yes | No",
  "reason_not_closed": "string | null",
  "fy": "2025-26",
  "branch": "Ahmedabad",
  "created_at": "ISODate",
  "updated_at": "ISODate"
}
```

#### Enumerated Values

| Field | Allowed Values |
|---|---|
| `type_of_proposal` | `Fresh`, `Renewal`, `Expanded` |
| `quote_submitted` | `Yes`, `No` |
| `business_closed` | `Yes`, `No` |
| `requirement` | `Standard Fire & Peril Policy`, `Marine Policy`, `Erection All Risk Policy`, `Contractors All Risk Policy`, `Industrial All Risk Policy`, `D&O Policy`, `Any Others` |

#### Collection: `users`
```json
{
  "_id": "ObjectId",
  "username": "string (unique)",
  "password_hash": "bcrypt hash",
  "role": "admin | viewer",
  "created_at": "ISODate"
}
```

#### MongoDB Indexes
```javascript
// enquiries collection
db.enquiries.createIndex({ "enquiry_no": 1 }, { unique: true })
db.enquiries.createIndex({ "cre_rm_accountable": 1 })
db.enquiries.createIndex({ "date_referred": 1 })
db.enquiries.createIndex({ "type_of_proposal": 1 })
db.enquiries.createIndex({ "business_closed": 1 })
db.enquiries.createIndex({ "fy": 1, "branch": 1 })

// users collection
db.users.createIndex({ "username": 1 }, { unique: true })
```

---

## 3. Business Logic & Derived Calculations

All calculated fields below are derived at the API/aggregation layer — never stored as duplicates.

---

### 3.1 Field Derivations

#### Tentative Brokerage (12%)
```
tentative_brokerage_12pct = premium_potential × 0.12
```
- This is automatically computed on every insert/update, not a user-input field.
- Zero if `premium_potential` is null.

#### Quote Submission Status
```
quote_submitted = "Yes"  if quote_actual_date IS NOT NULL and IS a valid date
quote_submitted = "No"   otherwise
```
Note from data: Some records have `quote_actual_date` but `quote_submitted = "No"` (human override). Honour the explicit field.

#### Business Closed Status
```
business_closed = "Yes"  if closure_actual_date IS NOT NULL and business_closed flag = "Yes"
business_closed = "No"   if business_closed flag = "No"
```
Note: One record (Enquiry #62) has a `closure_date` but is marked `No` ("Lost To Existing Broker — please remove closure date, it's lost; by mistake clicked"). The explicit `business_closed = "No"` field takes precedence.

---

### 3.2 View B — Sales Funnel & Enquiry Capture

This view extends the master data with the computed brokerage column. Columns are identical to the master data plus:
- `tentative_brokerage_12pct` (computed)

Sorting: by `date_referred` ascending, then `enquiry_no` ascending.

**Month Grouping Logic:**
```python
month = date_referred.month  # integer 1–12
fiscal_period = f"{calendar.month_abbr[month]}'{str(year)[2:]}"
# e.g., April 2025 → "Apr'25"
```

---

### 3.3 View C — Business Conversion Ratio

Aggregated **monthly** view. Each month covers Apr 2025 – Mar 2026 fiscal year.

| Column | Formula |
|---|---|
| `month_label` | e.g., `April'25`, `May'25`, … `March'26` |
| `no_of_enquiries` | `COUNT(enquiries WHERE fiscal_month = M)` |
| `business_converted` | `COUNT(enquiries WHERE fiscal_month = M AND business_closed = 'Yes')` |
| `percentage_converted` | `business_converted / no_of_enquiries` (→ display as %) |
| **Totals row** | Sum of enquiries, sum of converted, overall ratio |

**Month ordering for FY 2025-26:**
```
April'25, May'25, June'25, July'25, August'25, September'25,
October'25, November'25, December'25, January'26, February'26, March'26
```

**Fiscal month derivation:**
```python
FISCAL_MONTHS = {4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep',
                 10:'Oct', 11:'Nov', 12:'Dec', 1:'Jan', 2:'Feb', 3:'Mar'}

def fiscal_label(dt):
    yr_suffix = '25' if dt.month >= 4 else '26'
    return f"{FISCAL_MONTHS[dt.month]}'{yr_suffix}"
```

---

### 3.4 View D — Summary: Sales Capture

Aggregated **per CRE/RM** (sales person).

| Column | Formula |
|---|---|
| `cre_rm_accountable` | Sales person name |
| `total_enquiries` | `COUNT(*)` grouped by person |
| `business_converted` | `COUNT WHERE business_closed = 'Yes'` |
| `total_premium_converted` | `SUM(premium_potential) WHERE business_closed = 'Yes'` |
| `business_not_converted` | `COUNT WHERE business_closed = 'No'` |
| `pct_not_converted` | `business_not_converted / total_enquiries` (→ %) |

---

### 3.5 View E — Summary: Conversion Ratio (by Proposal Type)

Aggregated **per CRE/RM × proposal type** (Fresh / Renewal / Expanded).

For each person, compute three sub-groups:

#### Fresh Business Sub-Group
| Column | Formula |
|---|---|
| `fresh_total` | `COUNT WHERE type_of_proposal = 'Fresh'` |
| `fresh_converted` | `COUNT WHERE type = 'Fresh' AND business_closed = 'Yes'` |
| `fresh_premium` | `SUM(premium_potential) WHERE type = 'Fresh' AND closed = 'Yes'` |
| `fresh_brokerage` | `SUM(tentative_brokerage_12pct) WHERE type = 'Fresh' AND closed = 'Yes'` |
| `fresh_pct` | `fresh_converted / fresh_total` (0 if fresh_total = 0) |

#### Renewal Business Sub-Group
Same logic with `type_of_proposal = 'Renewal'`.

#### Expanded Business Sub-Group
Same logic with `type_of_proposal = 'Expanded'`.

#### Per-Person Totals
| Column | Formula |
|---|---|
| `total_enquiries` | fresh_total + renewal_total + expanded_total |
| `total_premium_converted` | fresh_premium + renewal_premium + expanded_premium |
| `total_brokerage_converted` | fresh_brokerage + renewal_brokerage + expanded_brokerage |
| `total_not_converted` | SUM of not-converted across all types |
| `pct_not_converted` | `total_not_converted / total_enquiries` (→ %) |

**Note from Excel analysis:** `Percentage Not Converted` in View E shows `100` (not `1.0`) for some rows — this is displayed as a whole number percentage (multiply by 100 before display).

---

## 4. Dashboard Views & Visualizations

### 4.1 Layout — Four Tab Navigation

```
[ Summary: Conversion Ratio ]  [ Summary: Sales Capture ]  [ Business Conversion Ratio ]  [ Sales Funnel & Enquiry Capture ]
```

Display order (left to right) mirrors the requirement sequence: a → b → c → d.

---

### Tab A — Summary: Conversion Ratio

**Chart 1: Stacked Bar — Converted vs Not Converted by CRE/RM**
- X axis: CRE/RM names
- Y axis: Number of enquiries
- Stacks: Converted (green) | Not Converted (red)
- Tooltip: count + percentage

**Chart 2: Grouped Bar — Proposal Type Breakdown per Person**
- For each person, show three grouped bars: Fresh / Renewal / Expanded
- Y axis: Number converted

**Table: Summary Conversion Ratio**
- Columns: CRE/RM | Total | Fresh (Total / Conv / Premium / Brokerage / %) | Renewal (...) | Expanded (...) | Overall (Total Premium | Total Brokerage | Not Conv | % Not Conv)
- Sortable columns
- Row totals highlighted

**KPI Cards (top row):**
- Total Enquiries (FY)
- Total Converted
- Overall Conversion Rate %
- Total Premium (Converted)
- Total Brokerage (Converted)

---

### Tab B — Summary: Sales Capture

**Chart: Horizontal Bar — Premium Converted by CRE/RM**
- X axis: Total premium (₹)
- Bars coloured by conversion rate (gradient: red→green)

**Chart: Pie — Share of Enquiries per CRE/RM**

**Table: Sales Capture Summary**
- Columns: CRE/RM | Total Enquiries | Converted | Total Premium Converted | Not Converted | % Not Converted
- Sortable, with totals row

---

### Tab C — Business Conversion Ratio

**Chart: Dual-Axis Line + Bar**
- Bar (left axis): No. of Enquiries per Month
- Line (right axis): Conversion Rate % per Month
- X axis: Monthly fiscal labels (Apr'25 → Mar'26)
- Reference line: Annual average conversion rate

**Table: Monthly Conversion Table**
- Columns: Month | No. of Enquiries | Business Converted | Conversion %
- Totals row at bottom
- Highlight months with conversion < 70% in amber, < 50% in red

---

### Tab D — Sales Funnel & Enquiry Capture

**Chart: Funnel Visualization**
```
Total Enquiries
    ↓
Quote Submitted (Yes)
    ↓
Business Closed (Yes)
```
- Count and % at each stage
- Drop-off % between stages

**Filters (top of tab):**
- Filter by Month (multi-select)
- Filter by CRE/RM (multi-select)
- Filter by Proposal Type (multi-select: Fresh / Renewal / Expanded)
- Filter by Requirement/Product type
- Search by Company Name

**Table: Enquiry Detail**
- Columns: No. | Date | Enquiry No. | Contact | Company | Requirement | Premium | Proposal Type | CRE/RM | Brokerage | Quote Planned | Quote Actual | Submitted? | Closure Planned | Closure Actual | Closed? | Reason
- Paginated (25 rows/page)
- Exportable to CSV

---

### Global Elements

**Top Header:**
- Salasar Services logo/name
- Branch: Ahmedabad | FY: 2025-26
- Last Updated timestamp (from MongoDB)

**Global Filter Bar (persists across tabs):**
- Financial Year selector (for future multi-year support)
- Quick date range picker

---

## 5. Backend: Python API Design

### Framework: FastAPI

### 5.1 Directory Structure (Backend)
```
backend/
├── main.py                    # FastAPI app entry point
├── config.py                  # Env vars, DB connection string
├── database.py                # MongoDB Motor async client
├── models/
│   ├── enquiry.py             # Pydantic model (EnquiryCreate, EnquiryOut)
│   └── user.py                # Pydantic model (UserCreate, UserOut)
├── routers/
│   ├── auth.py                # Login, token refresh
│   ├── enquiries.py           # CRUD for master data
│   ├── summary_sales.py       # View D aggregation endpoint
│   ├── summary_conversion.py  # View E aggregation endpoint
│   ├── business_conversion.py # View C aggregation endpoint
│   └── sales_funnel.py        # View B / funnel metrics
├── services/
│   ├── aggregations.py        # All MongoDB aggregation pipelines
│   └── import_excel.py        # One-time seed from Excel
├── security/
│   ├── auth.py                # JWT creation/validation
│   ├── hashing.py             # bcrypt password utils
│   └── middleware.py          # Rate limiting, CORS, logging
└── tests/
    ├── test_auth.py
    ├── test_enquiries.py
    └── test_aggregations.py
```

### 5.2 API Endpoints

#### Authentication
```
POST   /api/v1/auth/login           # Returns JWT access + refresh tokens
POST   /api/v1/auth/refresh         # Refresh access token
POST   /api/v1/auth/logout          # Invalidate refresh token
```

#### Master Data (Enquiries)
```
GET    /api/v1/enquiries            # List with filters & pagination
POST   /api/v1/enquiries            # Create new enquiry
GET    /api/v1/enquiries/{id}       # Get single enquiry
PUT    /api/v1/enquiries/{id}       # Update enquiry
DELETE /api/v1/enquiries/{id}       # Soft delete (admin only)
POST   /api/v1/enquiries/import     # Bulk import from Excel (admin only)
GET    /api/v1/enquiries/export     # Export filtered data as CSV
```

#### Aggregated Views
```
GET    /api/v1/analytics/summary-sales            # View D
GET    /api/v1/analytics/summary-conversion       # View E
GET    /api/v1/analytics/business-conversion      # View C (monthly)
GET    /api/v1/analytics/sales-funnel             # View B + funnel metrics
GET    /api/v1/analytics/kpis                     # Top-level KPI cards
```

#### Query Parameters (shared)
```
?fy=2025-26          # Financial year filter
?branch=Ahmedabad    # Branch filter (future multi-branch)
?cre_rm=Name         # Filter by sales person
?month=Apr-25        # Single month filter
?type=Fresh          # Proposal type filter
?from_date=YYYY-MM-DD
?to_date=YYYY-MM-DD
?page=1&limit=25     # Pagination
?sort=date_referred&order=asc
```

### 5.3 Key MongoDB Aggregation Pipeline — Summary Sales Capture

```python
pipeline = [
    {"$match": {"fy": fy, "branch": branch}},
    {
        "$group": {
            "_id": "$cre_rm_accountable",
            "total_enquiries": {"$sum": 1},
            "business_converted": {
                "$sum": {"$cond": [{"$eq": ["$business_closed", "Yes"]}, 1, 0]}
            },
            "total_premium_converted": {
                "$sum": {
                    "$cond": [
                        {"$eq": ["$business_closed", "Yes"]},
                        {"$ifNull": ["$premium_potential", 0]},
                        0
                    ]
                }
            },
            "business_not_converted": {
                "$sum": {"$cond": [{"$eq": ["$business_closed", "No"]}, 1, 0]}
            }
        }
    },
    {
        "$addFields": {
            "pct_not_converted": {
                "$cond": [
                    {"$gt": ["$total_enquiries", 0]},
                    {"$divide": ["$business_not_converted", "$total_enquiries"]},
                    0
                ]
            }
        }
    },
    {"$sort": {"_id": 1}}
]
```

### 5.4 Key MongoDB Aggregation Pipeline — Business Conversion Ratio (Monthly)

```python
pipeline = [
    {"$match": {"fy": fy}},
    {
        "$group": {
            "_id": {
                "month": {"$month": "$date_referred"},
                "year": {"$year": "$date_referred"}
            },
            "no_of_enquiries": {"$sum": 1},
            "business_converted": {
                "$sum": {"$cond": [{"$eq": ["$business_closed", "Yes"]}, 1, 0]}
            }
        }
    },
    {
        "$addFields": {
            "percentage_converted": {
                "$cond": [
                    {"$gt": ["$no_of_enquiries", 0]},
                    {"$divide": ["$business_converted", "$no_of_enquiries"]},
                    0
                ]
            }
        }
    },
    {"$sort": {"_id.year": 1, "_id.month": 1}}
]
```

### 5.5 Pydantic Model — EnquiryCreate

```python
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import date
from enum import Enum

class ProposalType(str, Enum):
    fresh = "Fresh"
    renewal = "Renewal"
    expanded = "Expanded"

class ClosedStatus(str, Enum):
    yes = "Yes"
    no = "No"

class RequirementType(str, Enum):
    sfp = "Standard Fire & Peril Policy"
    marine = "Marine Policy"
    ear = "Erection All Risk Policy"
    car = "Contractors All Risk Policy"
    iar = "Industrial All Risk Policy"
    do = "D&O Policy"
    others = "Any Others"

class EnquiryCreate(BaseModel):
    date_referred: date
    contact_person: str = Field(..., min_length=1, max_length=200)
    company_name: str = Field(..., min_length=1, max_length=300)
    phone: str = Field(..., pattern=r'^\d{10}$')
    email: Optional[EmailStr] = None
    requirement: RequirementType
    premium_potential: Optional[float] = Field(None, ge=0)
    type_of_proposal: ProposalType
    expiry_date_existing_policy: Optional[date] = None
    cre_rm_accountable: str = Field(..., min_length=1, max_length=200)
    quote_planned_date: Optional[date] = None
    quote_actual_date: Optional[date] = None
    quote_submitted: ClosedStatus = ClosedStatus.no
    closure_planned_date: Optional[date] = None
    closure_actual_date: Optional[date] = None
    business_closed: ClosedStatus = ClosedStatus.no
    reason_not_closed: Optional[str] = Field(None, max_length=500)

    @validator('tentative_brokerage_12pct', pre=True, always=True)
    def compute_brokerage(cls, v, values):
        premium = values.get('premium_potential')
        return round(premium * 0.12, 2) if premium else 0.0

    class Config:
        use_enum_values = True
```

---

## 6. Frontend: UI/UX Specification

### Framework Recommendation: React + Recharts + TailwindCSS

### 6.1 Design System

| Element | Specification |
|---|---|
| Primary Colour | `#1E3A5F` (Salasar navy) |
| Accent/Success | `#22C55E` (green — converted) |
| Warning | `#F59E0B` (amber — at risk) |
| Danger | `#EF4444` (red — not converted/lost) |
| Background | `#F8FAFC` |
| Card Background | `#FFFFFF` |
| Typography | Inter / Roboto, 14px body |
| Border Radius | 8px cards, 4px inputs |
| Shadow | `0 1px 3px rgba(0,0,0,0.1)` |

### 6.2 Responsive Breakpoints

| Breakpoint | Behaviour |
|---|---|
| Desktop (≥ 1280px) | 4-column KPI row, side-by-side charts |
| Tablet (768–1279px) | 2-column KPI row, stacked charts |
| Mobile (< 768px) | Single column, simplified table with horizontal scroll |

### 6.3 Number Formatting

| Type | Format |
|---|---|
| Currency (INR) | `₹1,23,45,678` (Indian comma notation) |
| Large numbers | `₹1.23 Cr` for values ≥ 10,00,000 |
| Percentages | `78.4%` (1 decimal place) |
| Counts | Integer, no decimals |

### 6.4 Table UX Standards

- Sticky header on scroll
- Column sorting (click header)
- Row hover highlight
- Empty state: "No records found for selected filters"
- Loading skeleton rows during API fetch
- Totals row pinned to bottom (visually distinct — bold, light grey background)
- Export button (CSV) top-right of each table

### 6.5 Chart UX Standards

- All charts have titles and axis labels
- Tooltips on hover with formatted values
- Legend below chart
- "No data" placeholder when all values are zero
- Responsive (resizes with container)
- Loading spinner during fetch

---

## 7. Security Protocols

### 7.1 Authentication & Authorisation

- **JWT tokens** (access token: 15 min TTL, refresh token: 7 days TTL)
- Tokens signed with `HS256` + strong secret from environment variable
- Refresh tokens stored in MongoDB `sessions` collection; invalidated on logout
- Role-based access: `admin` (full CRUD + import) vs `viewer` (read-only)
- Login endpoint: 5 failed attempts → 15-minute lockout (stored in MongoDB `login_attempts`)
- Passwords hashed with `bcrypt` (cost factor ≥ 12)

### 7.2 Input Validation & Injection Prevention

- All inputs validated via **Pydantic** models before any DB operation
- MongoDB queries use parameterised operators (`$eq`, `$in`, `$match`) — never string concatenation
- `company_name`, `contact_person`, and free-text fields stripped of HTML/script tags with `bleach`
- Phone validated against `^\d{10}$` regex
- Email validated by `pydantic.EmailStr`
- `premium_potential` validated as `float ≥ 0`
- Dates validated as ISO `date` — no raw string date comparisons in queries
- Filename in Excel import validated; only `.xlsx` accepted; max 10 MB

```python
# Example: safe MongoDB query pattern
async def get_enquiries(cre_rm: Optional[str] = None):
    filter_query = {}
    if cre_rm:
        # Sanitise — no operators injected
        safe_name = bleach.clean(cre_rm)
        filter_query["cre_rm_accountable"] = {"$eq": safe_name}
    return await db.enquiries.find(filter_query).to_list(None)
```

### 7.3 HTTP Security

- **HTTPS only** in production (enforce `SECURE_COOKIES = True`)
- CORS: whitelist only the frontend domain
- HTTP security headers (via `secure` middleware):
  - `Strict-Transport-Security: max-age=31536000`
  - `X-Content-Type-Options: nosniff`
  - `X-Frame-Options: DENY`
  - `Content-Security-Policy: default-src 'self'`
  - `Referrer-Policy: strict-origin-when-cross-origin`
- Rate limiting: 100 requests/minute per IP (via `slowapi`)
- API keys or JWT required on all non-public endpoints

### 7.4 Data Handling

- PII fields (`phone`, `email`) stored as plain text in MongoDB but never logged in application logs
- Log files must not contain any document content — only HTTP method, endpoint, status code, and timestamp
- Export (CSV) requires `admin` role
- Bulk import (`POST /enquiries/import`) requires `admin` role + validates entire payload before any writes (all-or-nothing transaction)
- MongoDB connection string in `.env` file, never committed to Git (`.gitignore` enforced)
- Secrets managed via environment variables; never hardcoded

### 7.5 Dependency Security

```
# requirements.txt — pin exact versions
fastapi==0.111.0
motor==3.4.0           # Async MongoDB driver
pydantic[email]==2.7.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bleach==6.1.0
slowapi==0.1.9
python-multipart==0.0.9
openpyxl==3.1.2
python-dotenv==1.0.1
uvicorn==0.29.0
```

- Run `pip audit` or `safety check` in CI pipeline to detect known CVEs
- Dependabot enabled on GitHub repository

### 7.6 Git & Deployment Security

- `.env` and `*.env` in `.gitignore`
- Pre-commit hook: reject commits containing secrets (`detect-secrets`)
- Branch protection: `main` requires PR + review
- GitHub Actions CI: lint → test → `safety check` → build
- MongoDB Atlas IP whitelist: allow only deployment server IP

---

## 8. Project File Structure

```
salasar-dashboard/
├── .env.example                   # Template for env vars (no real secrets)
├── .gitignore
├── README.md
├── docker-compose.yml             # Local dev (MongoDB + backend + frontend)
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── requirements.txt
│   ├── models/
│   │   ├── enquiry.py
│   │   └── user.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── enquiries.py
│   │   ├── summary_sales.py
│   │   ├── summary_conversion.py
│   │   ├── business_conversion.py
│   │   └── sales_funnel.py
│   ├── services/
│   │   ├── aggregations.py
│   │   └── import_excel.py
│   ├── security/
│   │   ├── auth.py
│   │   ├── hashing.py
│   │   └── middleware.py
│   └── tests/
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_enquiries.py
│       └── test_aggregations.py
│
├── frontend/
│   ├── package.json
│   ├── tailwind.config.js
│   ├── public/
│   │   └── index.html
│   └── src/
│       ├── App.jsx
│       ├── api/
│       │   ├── client.js          # Axios instance with JWT interceptor
│       │   ├── auth.js
│       │   └── analytics.js
│       ├── components/
│       │   ├── Layout/
│       │   │   ├── Header.jsx
│       │   │   ├── TabNav.jsx
│       │   │   └── FilterBar.jsx
│       │   ├── KPICard.jsx
│       │   ├── DataTable.jsx
│       │   ├── charts/
│       │   │   ├── StackedBarChart.jsx
│       │   │   ├── GroupedBarChart.jsx
│       │   │   ├── LineBarCombo.jsx
│       │   │   ├── FunnelChart.jsx
│       │   │   └── PieChart.jsx
│       │   └── common/
│       │       ├── LoadingSkeleton.jsx
│       │       ├── EmptyState.jsx
│       │       └── ExportButton.jsx
│       ├── pages/
│       │   ├── Login.jsx
│       │   ├── SummaryConversion.jsx
│       │   ├── SummarySales.jsx
│       │   ├── BusinessConversion.jsx
│       │   └── SalesFunnel.jsx
│       ├── hooks/
│       │   ├── useAnalytics.js
│       │   └── useAuth.js
│       └── utils/
│           ├── formatters.js      # INR formatting, % formatting
│           └── fiscalMonth.js     # Apr'25 → Mar'26 ordering helpers
│
└── scripts/
    ├── seed_from_excel.py         # One-time import script
    └── create_admin_user.py       # CLI tool for first admin user
```

---

## 9. Environment & Dependency Setup

### 9.1 `.env.example`
```env
# MongoDB
MONGODB_URI=mongodb+srv://<user>:<password>@<cluster>.mongodb.net/salasar_ahmedabad
DB_NAME=salasar_ahmedabad

# JWT
JWT_SECRET_KEY=<generate-with: openssl rand -hex 32>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# App
APP_ENV=development     # development | production
ALLOWED_ORIGINS=http://localhost:3000
LOG_LEVEL=INFO

# Admin seed (first run only)
INITIAL_ADMIN_USERNAME=admin
INITIAL_ADMIN_PASSWORD=<strong-password>
```

### 9.2 One-Time Excel Seed Command
```bash
cd backend
python scripts/seed_from_excel.py \
  --file "../Sales_Capture__Ahmedabad__2025-26.xlsx" \
  --sheet "Enquiry Capture Sheet" \
  --fy "2025-26" \
  --branch "Ahmedabad"
```

### 9.3 Start Local Dev
```bash
# Start MongoDB (via Docker Compose)
docker-compose up -d mongodb

# Backend
cd backend && uvicorn main:app --reload --port 8000

# Frontend
cd frontend && npm install && npm start
```

### 9.4 Run Tests
```bash
cd backend && pytest tests/ -v --cov=. --cov-report=html
```

---

## Appendix A — Excel Data Quality Notes

1. **Enquiry #52** (`Divine Tubes Private Limited`): `reason_not_closed` is blank for a "No" closure — acceptable, store as null.
2. **Enquiry #62** (`Gujarat Credo Alumina`): Has a `closure_actual_date` but explicitly marked `No` with note "Lost To Existing Broker — please remove closure date entry, its lost by mistake clicked". During import, set `business_closed = 'No'` and `closure_actual_date = null`.
3. **Enquiry #100** (`DRA _ BPCL`): `quote_submitted = "No"` despite a `quote_actual_date` — honour the explicit flag, store `quote_submitted = 'No'`.
4. **Enquiry #166** and **#190**: `premium_potential` is null/blank — store as `null`, exclude from premium sums, count as zero brokerage.
5. **Some `type_of_proposal` values** for enquiries #93 onwards are blank in Excel — treat as null, flag in UI as "Unknown", and exclude from type-based groupings (but include in totals).
6. **Duplicate company entries** (e.g., Ghanshyam Metal Udyog, LCC Projects) are intentional — each row = a distinct enquiry for a potentially different policy or transaction.
7. **Dates appearing in FY 2026-27** (e.g., `closure_actual_date = 2026-12-31`, `2026-04-06`) — store as-is; these are actual closure dates beyond the enquiry FY. Filter-by-month logic must use `date_referred` (not closure date) for fiscal month assignment.

---

## Appendix B — Validation Checklist Before Go-Live

- [ ] All 326 enquiry records imported without errors
- [ ] Business Conversion Ratio view totals match Excel: 408 enquiries, 320 converted, 78.4%
- [ ] Summary Sales Capture totals per person match Excel (e.g., Tara Prakash Sharma: 222 enquiries, 210 converted)
- [ ] Tentative brokerage (12%) computed correctly for sample records
- [ ] JWT login and role-based access tested (admin vs viewer)
- [ ] Rate limiting tested (> 100 req/min returns 429)
- [ ] CORS rejects requests from unlisted origins
- [ ] MongoDB injection attempt returns 422 (Pydantic validation error)
- [ ] Export CSV tested for admin; blocked for viewer
- [ ] All charts render correctly with real data
- [ ] INR formatting uses Indian numbering system (lakhs/crores)
- [ ] Funnel chart shows correct drop-off between stages
- [ ] `safety check` passes with zero known CVEs