---
description: Build an LBO Sources & Uses table slide
argument-hint: "[deal name or target]"
---

# IB Sources & Uses

Build a Sources & Uses table for an LBO transaction. Two-column layout with Sources on
the left, Uses on the right, totals at the bottom, and a balance check.

Load the `ib-deck-engine` skill and use `render_sources_uses`.

## What this slide shows

- **Sources column** (left): Term Loan B, Revolver, Sponsor Equity, etc. with $ and %
- **Uses column** (right): Enterprise Value, Advisory Fees, Financing Fees, etc.
- **Totals**: Bold totals at the bottom of each column
- **Balance check**: Highlighted callout at the bottom verifying Sources = Uses

## Workflow

If a deal name is provided as $1, ask for capital structure assumptions:
- Entry EV (or LTM EBITDA × multiple)
- Term Loan B size and pricing (e.g., SOFR + 450)
- Revolver capacity
- Sponsor equity (the plug)
- Advisory fees % (typically 1.5%)
- Financing fees % (typically 2.0% of debt)

## Critical rules

- **Sources MUST equal Uses** — the balance check formula proves it
- **Action title** — "Preliminary LBO Capital Structure Sources Total $X With $Y Sponsor Equity"
- **Subtitle with key metrics** — leverage ratio, equity %
- **All amounts in thousands** — pass as integers, renderer formats with commas
- **Total rows have `"total": True`** — gets bold + top border
- **Balance check string** — "Balance Check: Sources = Uses = $X,XXX,XXX ✓"

## Example spec

```python
r.render_sources_uses({
    "title": "Preliminary LBO Capital Structure Sources Total Capitalization of $1,902M",
    "subtitle": "Based on 12.0x LTM EBITDA of $155M | 4.5x leverage | 63% sponsor equity contribution",
    "source": "Source: LBO model. Transaction assumptions illustrative.",
    "sources": [
        {"label": "Term Loan B (SOFR + 450)", "amount": 700000, "pct": "36.8%"},
        {"label": "Revolver (undrawn)", "amount": 0, "pct": "0.0%"},
        {"label": "Sponsor Equity", "amount": 1202229, "pct": "63.2%"},
        {"label": "Total Sources", "amount": 1902229, "pct": "100.0%", "total": True},
    ],
    "uses": [
        {"label": "Enterprise Value", "amount": 1860324, "pct": "97.8%"},
        {"label": "Advisory Fees (1.5%)", "amount": 27905, "pct": "1.5%"},
        {"label": "Financing Fees (2.0%)", "amount": 14000, "pct": "0.7%"},
        {"label": "Total Uses", "amount": 1902229, "pct": "100.0%", "total": True},
    ],
    "balance_check": "Balance Check: Sources = Uses = $1,902,229K ✓"
})
```
