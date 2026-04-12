================================================================================
SALASAR SERVICES — SALES ANALYTICS DASHBOARD
UI DESIGN INSTRUCTION SET: IDEA 1
Metric-First Layout with Sidebar Filters (Streamlit)
================================================================================
Version: 1.0  |  Date: April 2026  |  Prepared for: Open Code Implementation
================================================================================


────────────────────────────────────────────────────────────────────────────────
SECTION 1: DESIGN CONCEPT
────────────────────────────────────────────────────────────────────────────────

Name            : Metric-First Layout with Sidebar Filters
Aesthetic       : Enterprise-clean — flat surfaces, no gradients, high
                  information density, corporate trust
Page structure  : Persistent left sidebar (filters + nav) · Full-width main
                  area (header strip → KPI row → chart area)
Target user     : Branch managers and admin reviewing FY conversion performance
                  across CRE/RM team
Primary action  : Filter by RM / month / product / proposal type → charts and
                  KPIs update instantly
Framework       : Streamlit · layout="wide" · Plotly for all charts · pandas
                  for data layer


DESIGN PHILOSOPHY — 4 RULES
------------------------------

Rule 1: Data is the hero
  No decorative chrome. Every visual element either encodes data or helps the
  user navigate to data. Remove anything that doesn't do one of these two jobs.

Rule 2: Colour encodes meaning
  Blue   = volume / quantity
  Green  = positive performance
  Amber  = currency / revenue
  Gray   = neutral / structural
  Never use colour decoratively.

Rule 3: Filters are always visible
  The sidebar is always in view. Users should never have to hunt for filter
  controls. Active filter state is always reflected in the header context bar.

Rule 4: KPIs anchor every page
  The 5-metric KPI strip is the first thing rendered on every module page.
  It gives instant orientation before the user reads any chart.


────────────────────────────────────────────────────────────────────────────────
SECTION 2: PAGE-LEVEL LAYOUT
────────────────────────────────────────────────────────────────────────────────

STREAMLIT CONFIG
-----------------
st.set_page_config(
    layout="wide",
    page_title="Salasar Analytics",
    page_icon="📊"
)

Sidebar width   : 220px (Streamlit default wide sidebar — do not override)
Main content    : Flows in remaining viewport. No max-width cap.
Page gutter     : Streamlit default padding — do not add extra via st.markdown hacks
Vertical rhythm : Header strip → 16px gap → KPI strip → 20px gap → chart area
                  Use st.divider() only between major sections


MAIN AREA — THREE ZONES
--------------------------

Zone A — Header context bar
  Height    : ~52px fixed
  Background: #042C53 (dark navy)
  Content   : App name · active branch · active FY · today's date · user badge
  Method    : Rendered via st.markdown(unsafe_allow_html=True)
              NOT a native Streamlit component

Zone B — KPI strip
  Height    : ~90px
  Structure : Five metric cards in st.columns(5)
  Component : st.metric(label, value, delta) per column
  Behaviour : Reacts to sidebar filter state

Zone C — Chart area
  Height    : Fills remaining viewport
  Structure : Varies by active nav page. Typically st.columns([1.4, 1])
              (chart left, supporting panel right)
              Each chart wrapped in a bordered container card


SIDEBAR — FIVE ZONES
-----------------------

S1 — Brand block
  Salasar logo (PNG, transparent bg, max-height 36px)
  App title: 13px / weight 500
  User name + role badge below logo

S2 — Context selectors (global — resets all filters on change)
  st.selectbox("Branch", branch_list)
  st.selectbox("Financial year", fy_list)

S3 — Drill-down filters
  Label: st.caption("Filters") above the block
  Controls (see Section 6 for full specs):
    · CRE/RM multiselect
    · Month range slider
    · Product multiselect
    · Proposal type multiselect

S4 — Navigation
  st.radio() styled as nav list (see Section 5 — Components)
  Four items: Summary Conversion · Summary Sales ·
              Business Conversion · Sales Funnel

S5 — Footer
  st.button("Sign out") at bottom
  IRDA license text: 10px muted gray below sign-out button


────────────────────────────────────────────────────────────────────────────────
SECTION 3: COLOUR TOKENS
────────────────────────────────────────────────────────────────────────────────

PRIMARY BRAND COLOURS
----------------------
#042C53   Header background, sidebar nav active background
#185FA5   Primary action, active nav item, chart primary series
#E6F1FB   Blue tint surface (info/volume metric card background)
#B5D4F4   Blue tint border, lighter chart fills
#0C447C   Blue text on blue-tint surface (KPI value)
#378ADD   Blue subtitle text on dark header

SUCCESS / GROWTH COLOURS
--------------------------
#1D9E75   Positive delta indicator, Renewal series colour
#EAF3DE   Green tint surface (conversion/rate metric card background)
#3B6D11   Green label text on green-tint surface
#27500A   Green value text on green-tint surface (KPI value)

REVENUE / CURRENCY COLOURS
----------------------------
#EF9F27   Premium and brokerage chart accent colour
#FAEEDA   Amber tint surface (revenue metric card background)
#854F0B   Amber label text on amber-tint surface
#633806   Amber value text on amber-tint surface (KPI value)

NEUTRAL SURFACES
-----------------
#F8F9FA   Page background         → backgroundColor in config.toml
#EFF2F7   Secondary surface       → secondaryBackgroundColor in config.toml
#FFFFFF   Card background (white)
#E5E7EB   Default card border (0.5px)

TEXT COLOURS
-------------
#1A1F36   Primary text (headings, values)     → textColor in config.toml
#6B7280   Secondary text (labels, body)
#9CA3AF   Tertiary text (captions, axis labels)
#A32D2D   Negative delta (red)

BORDER COLOURS
---------------
#E5E7EB   Default card borders (0.5px)
#B5D4F4   Info-tinted borders
#C0DD97   Success-tinted borders


────────────────────────────────────────────────────────────────────────────────
SECTION 4: TYPOGRAPHY SCALE
────────────────────────────────────────────────────────────────────────────────

Font family     : font = "sans serif" in config.toml (system UI sans)
                  Do NOT load external fonts — keep load time fast

Scale:
  Page title      18px · weight 500 · colour #B5D4F4 (on dark header)
  Section heading 14px · weight 500 · colour #1A1F36
  KPI value       24px · weight 500 · colour from KPI ramp (see tint rule below)
  KPI label       12px · weight 400 · colour #6B7280
  KPI delta       12px · weight 400 · #3B6D11 (positive) / #A32D2D (negative)
  Body / caption  13px · weight 400 · colour #6B7280
  Chart axis      11px · weight 400 · colour #9CA3AF

Two weights only: 400 (regular) and 500 (medium/bold).
Never use 600 or 700 — too heavy against the page.
Sentence case always. Never ALL CAPS or Title Case.


────────────────────────────────────────────────────────────────────────────────
SECTION 5: SPACING & RADIUS TOKENS
────────────────────────────────────────────────────────────────────────────────

Card radius         : 8px
Badge / pill radius : 20px (fully rounded)
Card padding        : 16px top/bottom · 18px left/right
KPI strip gap       : 10px between each metric card
Chart container pad : 14px all sides inside the bordered card wrapper
Section vertical gap: 20px between zones A → B → C
Chart height (main) : 360px for primary charts
Chart height (sub)  : 240px for supporting/secondary charts


────────────────────────────────────────────────────────────────────────────────
SECTION 6: COMPONENT SPECIFICATIONS
────────────────────────────────────────────────────────────────────────────────

A. HEADER CONTEXT BAR
-----------------------
Background      : #042C53 — injected via st.markdown(unsafe_allow_html=True)
Left content    :
  · App name: "Salasar Services — Sales analytics"
    18px / weight 500 / colour #B5D4F4
  · Context line: "[Branch] · [FY] · [Date]"
    11px / weight 400 / colour #378ADD
Right content   :
  · Role badge (e.g. "Admin")
    Background #0C447C · text #B5D4F4 · 11px · border-radius 20px · padding 3px 10px
  · Status badge (e.g. "Live")
    Background #0F6E56 · text #9FE1CB · same size as role badge
Height          : 52px. No bottom border.


B. KPI METRIC STRIP
---------------------
Streamlit call  : st.metric(label, value, delta) inside st.columns(5)

KPI tint rule (background by metric type):
  Volume metrics      → #E6F1FB (blue tint)
  Rate / count metrics→ #EAF3DE (green tint)
  Currency metrics    → #FAEEDA (amber tint)

Override card backgrounds via:
  st.markdown() with [data-testid="metric-container"] CSS selector
  Apply per-column position class or per-metric wrapper div

Delta behaviour : Positive = green (#3B6D11). Negative = red (#A32D2D).
                  Use Streamlit built-in delta colour — do not override.

Currency format : Prefix ₹ · Suffix Cr · Always 2 decimal places
                  Python: f"₹{val:.2f} Cr"

Five KPI cards (left to right):
  Card 1 — Total enquiries      → Blue tint · label "Total enquiries"
  Card 2 — Total converted      → Green tint · label "Total converted"
  Card 3 — Conversion rate      → Green tint · label "Conversion rate"
  Card 4 — Premium converted    → Amber tint · label "Premium converted" · ₹ Cr
  Card 5 — Brokerage converted  → Amber tint · label "Brokerage converted" · ₹ Cr


C. CHART CONTAINER CARD
--------------------------
Wrapper         : st.container(border=True)
Background      : #FFFFFF (white)
Border          : 0.5px solid #E5E7EB
Border radius   : 8px
Padding         : 14px all sides
Chart title     : 14px / weight 500 · left-aligned
                  Use st.markdown("**Chart title**") inside container
                  Never use Plotly layout.title
Chart subtitle  : 12px muted · use st.caption("description")
Plotly theme    : template="plotly_white" on all charts
                  Override axis line colour to #E5E7EB
                  Remove outer frame: fig.update_layout(showlegend=True,
                  plot_bgcolor='white', paper_bgcolor='white')


D. SIDEBAR NAVIGATION
-----------------------
Component       : st.radio("", options, label_visibility="collapsed")
CSS override    : Style as vertical nav list via st.markdown injection

Active state    :
  Background    #E6F1FB
  Text colour   #185FA5
  Font weight   500
  Left border   3px solid #185FA5
  Border radius 0 (flat left) / 6px (right) — single-side border, no full radius

Inactive state  :
  Background    transparent
  Text colour   #6B7280
  Font weight   400

Hover state     :
  Background    #EFF2F7
  Text colour   #1A1F36

Icon            : 16px inline SVG icon left of each label
                  Simple shape: bar chart / line / funnel per page
                  Colour inherits from text colour

Nav items (in order):
  · Summary Conversion
  · Summary Sales
  · Business Conversion
  · Sales Funnel


────────────────────────────────────────────────────────────────────────────────
SECTION 7: CHART SPECIFICATIONS BY PAGE
────────────────────────────────────────────────────────────────────────────────

PAGE 1 — SUMMARY: CONVERSION RATIO
--------------------------------------
Layout          : st.columns([1.4, 1]) — stacked bar left, grouped bar right

Left chart — Stacked bar
  Type          : px.bar with barmode="stack"
  X axis        : CRE/RM name (categorical) · sorted by total enquiries desc
  Y axis        : Count of enquiries · no axis title (use chart subtitle instead)
  Series        :
    Fresh       → #185FA5
    Renewal     → #1D9E75
    Expanded    → #EF9F27
  Legend        : Horizontal below chart · 11px font · 10px square markers
  Tooltip       : RM name · proposal type · count · % of total
                  Background #FFFFFF · border 1px #E5E7EB
  Plotly call   :
    fig = px.bar(df, x="rm_name", y="count", color="proposal_type",
                 barmode="stack", height=360,
                 color_discrete_map={"Fresh":"#185FA5","Renewal":"#1D9E75",
                 "Expanded":"#EF9F27"}, template="plotly_white")

Right chart — Grouped bar
  Type          : px.bar with barmode="group"
  Same data, axes and colours as stacked bar above
  Use for side-by-side comparison of proposal types per RM
  Height        : 360px


PAGE 2 — SUMMARY: SALES CAPTURE
-----------------------------------
Layout          : st.columns([1, 1]) — horizontal bar left, donut right
                  st.dataframe below spanning full width

Left chart — Horizontal bar (premium per CRE/RM)
  Type          : px.bar with orientation='h'
  X axis        : Premium amount (₹ Cr) · no axis title
  Y axis        : CRE/RM name · sorted highest to lowest
  Series colour : Single colour #185FA5
  Value labels  : Show at bar end · 11px · #1A1F36
  Height        : 360px
  Plotly call   :
    fig = px.bar(df, x="premium_cr", y="rm_name", orientation='h',
                 height=360, template="plotly_white",
                 color_discrete_sequence=["#185FA5"])
    fig.update_traces(texttemplate='₹%{x:.2f} Cr', textposition='outside')

Right chart — Donut (premium share by proposal type)
  Type          : px.pie with hole=0.55
  Values        : Premium ₹ Cr per proposal type
  Names         : Proposal type
  Hole          : 55% · Centre label = total premium (₹ Cr)
  Colours       : Fresh #185FA5 · Renewal #1D9E75 · Expanded #EF9F27
  Height        : 360px
  Plotly call   :
    fig = px.pie(df, values="premium_cr", names="proposal_type",
                 hole=0.55, height=360,
                 color_discrete_map={"Fresh":"#185FA5","Renewal":"#1D9E75",
                 "Expanded":"#EF9F27"})
    fig.add_annotation(text=f"₹{total:.1f} Cr", x=0.5, y=0.5,
                       font_size=14, showarrow=False)

Summary table (below charts)
  Component     : st.dataframe(df, hide_index=True, use_container_width=True)
  Columns       : RM Name · Enquiries · Premium (₹ Cr) · Brokerage (₹ Cr)
                  · Conversion Rate (%)
  Column widths : Fixed. Alternating row highlight via column_config.


PAGE 3 — BUSINESS CONVERSION RATIO
--------------------------------------
Layout          : Single full-width chart

Chart — Dual-axis line
  Library       : plotly.graph_objects + make_subplots
  X axis        : Month (Apr → Mar) · 12 data points
                  Tick every month · 3-letter abbreviation (Apr, May … Mar)
  Left Y axis   : Enquiry volume (bar) · colour fill #B5D4F4 · label "Enquiries"
  Right Y axis  : Conversion rate % (line) · colour #185FA5
                  Line weight 2px · markers at each data point (circle, 6px)
  Reference line: Dashed horizontal at annual average conversion rate
                  Colour #9CA3AF · dash="dash"
                  Right-edge label: "Avg XX.X%"
  Annotations   : Annotate peak month and lowest month with callout labels
                  Font 11px · #6B7280
  Height        : 400px
  Plotly call   :
    from plotly.subplots import make_subplots
    import plotly.graph_objects as go
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Bar(x=df.month, y=df.enquiries,
                         marker_color="#B5D4F4", name="Enquiries"),
                  secondary_y=False)
    fig.add_trace(go.Scatter(x=df.month, y=df.conv_rate,
                             line=dict(color="#185FA5", width=2),
                             mode="lines+markers", name="Conv. rate %"),
                  secondary_y=True)
    fig.add_hline(y=avg_rate, line_dash="dash",
                  line_color="#9CA3AF", secondary_y=True)


PAGE 4 — SALES FUNNEL & ENQUIRY CAPTURE
-----------------------------------------
Layout          : Funnel chart top · filter row below · data table below

Funnel chart
  Type          : px.funnel
  Stages        : Enquired → Quoted → Negotiated → Converted
  Values        : Count at each stage
  Colours       : Single blue ramp dark→light top→bottom
                  #042C53 · #185FA5 · #85B7EB · #E6F1FB
  Height        : 280px
  Plotly call   :
    fig = px.funnel(df_funnel, x="count", y="stage",
                    color_discrete_sequence=["#042C53","#185FA5",
                    "#85B7EB","#E6F1FB"], height=280,
                    template="plotly_white")

Inline filter row (above table)
  Layout        : st.columns([1, 1, 1, 1, 2])
  Controls      : Month select · RM select · Product select ·
                  Type select · Search text input
  Style         : Compact — label_visibility="collapsed" on all controls

Data table
  Component     : st.dataframe(df, use_container_width=True, hide_index=True)
  Columns       : Date · Company · Product · CRE/RM · Proposal Type ·
                  Premium (₹ Cr) · Status
  Status badges :
    Converted   → Green pill  (background #EAF3DE · text #27500A)
    Pending     → Amber pill  (background #FAEEDA · text #633806)
    Lost        → Red pill    (background #FCEBEB · text #791F1F)
  Badge render  : via st.dataframe column_config or HTML in styled df
  Row count     : st.caption(f"{len(df_filtered)} records") below table

Export button
  st.download_button("Export CSV", data=df.to_csv(index=False),
                     file_name="enquiries.csv", mime="text/csv")
  Position: right-aligned above the data table using st.columns([8, 1])


────────────────────────────────────────────────────────────────────────────────
SECTION 8: FILTER CONTROLS
────────────────────────────────────────────────────────────────────────────────

All controls placed inside with st.sidebar:

Branch
  st.selectbox("Branch", branch_list)
  Single select · Default = first branch in user's scope

Financial year
  st.selectbox("Financial year", fy_list)
  Options: ["FY 2024-25", "FY 2025-26"]
  Default = current FY

CRE/RM
  st.multiselect("CRE/RM", rm_list, default=rm_list)
  Default = all selected
  Show count badge when subset is selected: e.g. "3 of 7 selected"

Month range
  st.select_slider("Month range",
                   options=["Apr","May","Jun","Jul","Aug","Sep",
                            "Oct","Nov","Dec","Jan","Feb","Mar"],
                   value=("Apr", "Mar"))
  Default = Apr–Mar (full FY)

Product
  st.multiselect("Product", product_list, default=product_list)
  Default = all selected

Proposal type
  st.multiselect("Proposal type",
                 ["Fresh", "Renewal", "Expanded"],
                 default=["Fresh", "Renewal", "Expanded"])
  Default = all selected

Reset button
  st.button("Reset filters")
  Resets all multiselects and month slider to defaults
  Does NOT reset Branch or FY

Active filter indicator
  Show below reset button:
  st.caption("3 filters active") when any filter deviates from default
  Hide caption when all filters are at default


FILTER STATE MANAGEMENT
-------------------------
Storage         : Use st.session_state for all filter values
                  Initialise defaults:
                    if "filters_init" not in st.session_state:
                        st.session_state.rm_filter = rm_list
                        st.session_state.month_range = ("Apr", "Mar")
                        ... etc
                    st.session_state.filters_init = True

Data filtering  : All chart data derived from a single df_filtered dataframe
                  Apply all filter conditions ONCE at top of each page render
                  before any chart or metric calls

Caching         : @st.cache_data on all data loading functions
                  Do NOT cache filtered data — must recalculate on each run

Context bar     : Header must always reflect active branch and FY from
                  session_state — never hardcoded values


────────────────────────────────────────────────────────────────────────────────
SECTION 9: CONFIGURATION FILES
────────────────────────────────────────────────────────────────────────────────

.streamlit/config.toml
-----------------------
[theme]
primaryColor = "#185FA5"
backgroundColor = "#F8F9FA"
secondaryBackgroundColor = "#EFF2F7"
textColor = "#1A1F36"
font = "sans serif"

[server]
headless = true

[browser]
gatherUsageStats = false


GLOBAL CSS INJECTION
---------------------
Place at top of app.py, called once on every run:

hide_streamlit_style = """
<style>
  #MainMenu, footer, header { visibility: hidden; }
  .block-container { padding-top: 1rem; }
  [data-testid="stSidebar"] {
    background-color: #FFFFFF;
    border-right: 0.5px solid #E5E7EB;
  }
  [data-testid="metric-container"] {
    background: #EFF2F7;
    border-radius: 8px;
    padding: 12px;
  }
  div[data-testid="stRadio"] label {
    padding: 6px 10px;
    border-radius: 6px;
    cursor: pointer;
  }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

Note: Apply per-card metric tinting by targeting nth-child positions of
[data-testid="metric-container"] or by wrapping each metric in a custom
st.markdown div with inline style.


requirements.txt
-----------------
streamlit>=1.32
pandas>=2.0
plotly>=5.18
openpyxl>=3.1
python-dateutil


PROJECT FILE STRUCTURE
------------------------
app.py                              ← main entry point, global CSS, session init
pages/
    1_Summary_Conversion.py
    2_Summary_Sales.py
    3_Business_Conversion.py
    4_Sales_Funnel.py
.streamlit/
    config.toml
utils/
    data_loader.py                  ← @st.cache_data functions only
    chart_helpers.py                ← reusable Plotly figure builders
    filters.py                      ← filter state init and df_filtered builder
assets/
    salasar_logo.png                ← transparent background, max 36px height


────────────────────────────────────────────────────────────────────────────────
SECTION 10: ACCESSIBILITY & PERFORMANCE CHECKLIST
────────────────────────────────────────────────────────────────────────────────

[ ] All colour pairs meet WCAG AA contrast (minimum 4.5:1 for body text)
[ ] Status meanings conveyed by BOTH colour AND label/icon — never colour alone
[ ] Chart tooltips include all data dimensions — do not rely on legend colour only
[ ] All data loading behind @st.cache_data — target <1 second filter re-render
[ ] Currency values always formatted as ₹XX.XX Cr — never raw float
[ ] Empty state handled — if df_filtered is empty, show:
    st.info("No data matches the current filters.")
[ ] Admin-only controls gated by role check from st.session_state
[ ] Export button available on Sales Funnel page for CSV download
[ ] Page titles set correctly via st.set_page_config per page file
[ ] No hardcoded branch/FY values — always read from session_state


================================================================================
END OF INSTRUCTION SET
================================================================================