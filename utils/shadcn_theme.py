"""
Shadcn UI theming for Salasar Sales Dashboard.
Injects CSS custom properties following shadcn/ui theming conventions.
Reference: https://ui.shadcn.com/docs/theming

Brand colors are mapped to shadcn CSS variable names using HSL format.
"""

import streamlit as st

# ── Shadcn CSS variable block ────────────────────────────────────────────────
# All values are HSL components (no hsl() wrapper) — shadcn convention.
# Usage in CSS: background-color: hsl(var(--background))
_SHADCN_VARS_CSS = """
<style>
/* ═══════════════════════════════════════════════════════════════════════════
   SHADCN/UI DESIGN TOKENS — SALASAR BRAND PALETTE
   Based on: https://ui.shadcn.com/docs/theming
   Each variable holds space-separated HSL components (no hsl() wrapper).
   Usage: color: hsl(var(--primary))
═══════════════════════════════════════════════════════════════════════════ */

:root {
  /* Core surfaces */
  --background:              210 17% 98%;   /* #F8F9FA */
  --foreground:              229 35% 16%;   /* #1A1F36 */

  /* Card */
  --card:                    0 0% 100%;     /* #FFFFFF */
  --card-foreground:         229 35% 16%;   /* #1A1F36 */

  /* Popover */
  --popover:                 0 0% 100%;
  --popover-foreground:      229 35% 16%;

  /* Primary — Salasar navy blue */
  --primary:                 210 75% 37%;   /* #185FA5 */
  --primary-foreground:      210 17% 98%;   /* #F8F9FA */

  /* Secondary — light blue surface */
  --secondary:               218 33% 95%;   /* #EFF2F7 */
  --secondary-foreground:    229 35% 16%;   /* #1A1F36 */

  /* Muted — subtle backgrounds / disabled */
  --muted:                   218 33% 95%;   /* #EFF2F7 */
  --muted-foreground:        220 9% 46%;    /* #6B7280 */

  /* Accent — amber for currency / revenue */
  --accent:                  36 86% 55%;    /* #EF9F27 */
  --accent-foreground:       229 35% 16%;   /* #1A1F36 */

  /* Destructive — negative / red */
  --destructive:             0 57% 41%;     /* #A32D2D */
  --destructive-foreground:  210 17% 98%;

  /* Border / Input / Ring */
  --border:                  220 14% 91%;   /* #E5E7EB */
  --input:                   220 14% 91%;
  --ring:                    210 75% 37%;   /* #185FA5 */

  /* Border radius scale */
  --radius:                  0.5rem;        /* 8px — matches card-radius token */

  /* ── Extended brand tokens (beyond base shadcn set) ─────────────────── */

  /* Dark navy — header / deep brand backgrounds */
  --brand-navy:              210 91% 17%;   /* #042C53 */
  --brand-navy-foreground:   211 80% 88%;   /* #B5D4F4 */

  /* Medium navy — active states, chart primary series */
  --brand-navy-mid:          210 75% 37%;   /* #185FA5 */

  /* Light navy tint — info / volume KPI surface */
  --brand-navy-tint:         211 73% 94%;   /* #E6F1FB */
  --brand-navy-tint-border:  211 73% 83%;   /* #B5D4F4 */
  --brand-navy-tint-text:    211 79% 27%;   /* #0C447C */

  /* Success / growth */
  --success:                 161 69% 37%;   /* #1D9E75 */
  --success-foreground:      210 17% 98%;
  --success-tint:            97 43% 91%;    /* #EAF3DE */
  --success-tint-text:       96 72% 24%;    /* #27500A */

  /* Warning — amber / premium */
  --warning:                 36 86% 55%;    /* #EF9F27 */
  --warning-foreground:      229 35% 16%;
  --warning-tint:            37 86% 92%;    /* #FAEEDA */
  --warning-tint-text:       34 88% 28%;    /* #633806 */

  /* Chart series */
  --chart-fresh:             210 75% 37%;   /* #185FA5 */
  --chart-renewal:           161 69% 37%;   /* #1D9E75 */
  --chart-expanded:          36 86% 55%;    /* #EF9F27 */
  --chart-bar-fill:          211 73% 83%;   /* #B5D4F4 */
}
</style>
"""


def inject_shadcn_theme() -> None:
    """
    Inject shadcn/ui CSS custom properties into the Streamlit app.

    Call this once per page after st.set_page_config().  The variables are
    available to all subsequent st.markdown() blocks via hsl(var(--token)).
    """
    st.markdown(_SHADCN_VARS_CSS, unsafe_allow_html=True)
