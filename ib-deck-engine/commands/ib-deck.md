---
description: Build a complete investment banking pitch deck for a public company
argument-hint: "[company ticker or name]"
---

# IB Deck — Full Pitch Book

Build a complete 14-slide IB pitch deck for the specified company using the IB Deck Engine
template library. The architecture: extract data → fill JSON specs → deterministic rendering.

## Workflow

Load the `ib-deck-engine` skill to access the template library and follow this workflow:

### Step 1: Confirm the deal

If a company name/ticker is provided as $1, use it. Otherwise ask:
- "What company would you like to build a pitch deck for?"
- "Sell-side or buy-side mandate?"
- "Any specific assumptions to use (or should I use reasonable defaults)?"

### Step 2: Extract financial data

For public US companies, use `edgartools` to pull the most recent 10-K:
- Revenue, COGS, gross profit, operating income, EBITDA, net income (3 years)
- Balance sheet (cash, AR, debt, equity)
- Cash flow statement (CFO, CapEx, financing)
- Segment revenue if available
- Diluted share count
- Save as `{ticker}_master.json` — single source of truth

### Step 3: Build the 14-slide deck

Use the IBRenderer templates in this order:

1. **Cover** (`render_cover`) — Project codename + bank name + date
2. **Table of Contents** (`render_toc`) — 4 numbered agenda items
3. **Executive Summary** (`render_exec_summary`) — Blue callout + 3 main points with sub-bullets
4. **Investment Highlights** (`render_investment_highlights`) — 4-card 2×2 grid
5. **Section Divider** (`render_section_divider`) — "Review of Financial Performance"
6. **Financial Summary** (`render_financial_summary`) — Historical P&L with margins
7. **Revenue by Segment** (`render_stacked_bar_table`) — Stacked bars + data table
8. **Revenue + EBITDA** (`render_dual_chart`) — Side-by-side bar charts with CAGR
9. **Section Divider** (`render_section_divider`) — "Preliminary Valuation Analysis"
10. **Football Field** (`render_football_field`) — Valuation methodologies with range bars
11. **Sensitivity** (`render_sensitivity`) — WACC × Terminal Growth grid
12. **Trading Comps** (`render_trading_comps`) — Peer multiples table
13. **Section Divider** (`render_section_divider`) — "LBO Analysis"
14. **Sources & Uses** (`render_sources_uses`) — Capital structure with balance check

### Step 4: Verify and deliver

- Confirm 14 slides generated
- Verify source text on each content slide
- Save as `{ticker}_pitch_deck.pptx`
- Report the file path to the user

## Critical rules

- **Action titles only** — never "Financial Summary," always "Consistent Revenue Growth With Expanding Margins"
- **Every number sourced** — trace each value to a source file or note "Estimated"
- **Cross-model consistency** — DCF and LBO must use the same revenue, EBITDA, share count
- **Right-alignment automatic** — handled by templates, don't override

## Example: ADUS

```
/ib-deck ADUS
```

Builds a complete 14-slide pitch book for Addus HomeCare Corp using SEC EDGAR data.
See `skills/ib-deck-engine/reference/examples/full_deck.py` for the full worked example.
