---
description: Build a complete IB pitch deck using the 12-template library
argument-hint: "[company ticker or name]"
---

# IB Deck — Full Pitch Book Workflow

Orchestrates a complete IB pitch deck using the 12 templates in the IB Deck Engine
library. The typical deck is ~14 slides (12 distinct template types plus three reused
section dividers between the Financial, Valuation, and LBO sections).

This command is a **workflow guide**, not an automated pipeline. It walks Claude
through the steps to pick templates, fill JSON specs, and call the renderer. The
user supplies (or Claude helps assemble) the underlying financial data — this
version does not include an autonomous SEC EDGAR extractor.

## Workflow

Load the `ib-deck-engine` skill to access the template library.

### Step 1: Confirm the deal

If a company name/ticker is provided as $1, use it. Otherwise ask:
- "What company would you like to build a pitch deck for?"
- "Sell-side or buy-side mandate?"
- "Do you already have the financials, or should we work through them together?"

### Step 2: Assemble the master JSON

Get the underlying financial data into the master JSON schema documented in
`skills/ib-deck-engine/reference/template-catalog.md`. Options:

- User supplies existing JSON / CSV / financials
- Manual entry during the conversation
- One-off extraction script using `edgartools` (not bundled with this plugin in
  v0.1.0 — see the companion repo at github.com/gorajing/ib-deck-engine for a
  reference extraction)

The JSON should include: 3 years of historical IS/BS/CF, segment revenue if
available, debt detail, and diluted share count.

### Step 3: Build the deck

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

- Confirm slide count
- Spot-check source text on each content slide
- Save as `{ticker}_pitch_deck.pptx`
- Report the file path to the user

## Critical rules

- **Action titles only** — never "Financial Summary," always "Consistent Revenue Growth With Expanding Margins"
- **Every number sourced** — trace each value to a source file or note "Estimated"
- **Cross-model consistency** — DCF and LBO should use the same revenue, EBITDA, share count. Document any intentional differences (e.g., LBO using statutory vs effective tax rate).
- **Right-alignment is handled by the templates** — don't override it in the JSON spec

## Example: ADUS

```
/ib-deck ADUS
```

Walks through building a pitch book for Addus HomeCare Corp. A complete worked
example (including the ADUS master JSON and the generated PPTX) lives at the
companion repo: github.com/gorajing/ib-deck-engine.
