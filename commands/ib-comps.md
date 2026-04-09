---
description: Build a trading comparables (peer multiples) table slide
argument-hint: "[target company]"
---

# IB Trading Comps

Build a trading comparables table showing peer companies' valuation multiples with the
target company highlighted. Uses the `render_trading_comps` template.

Load the `ib-deck-engine` skill and use `render_trading_comps`.

## What this slide shows

A peer comparables table with:
- 5-10 peer companies in the same sector as the target
- Standard multiples: Market Cap, EV, Revenue, EBITDA, EV/Rev, EV/EBITDA, Growth
- Target company highlighted with yellow background
- Mean and Median summary rows in light gray
- Right-aligned numeric columns
- Source line at bottom

## Workflow

If a target company is provided as $1, ask:
- "Which peer companies should I include?" (or suggest based on sector)
- "Which financial metrics?" (default: Market Cap, EV, Rev, EBITDA, EV/Rev, EV/EBITDA, Growth)
- "What's the source for the data?" (FactSet, Capital IQ, Bloomberg)

## Critical rules

- **Action title** — "[Target] Trades at a Discount/Premium to Sector Peers Despite [Differentiation]"
- **Target row highlighted** — set `"target_row": 0` (zero-indexed) to highlight in yellow
- **Summary rows** — use `"summary": True` for Mean/Median rows (gray background, bold)
- **Right-aligned numbers** — automatic, don't override
- **Source citation** — always include date: "Source: FactSet. Market data as of April 2026."

## Example spec

```python
r.render_trading_comps({
    "title": "Addus Trades at a Discount to Home Care Services Peers Despite Superior Growth and Margins",
    "header_text": "Selected Home Care Services Trading Comparables",
    "headers": ["Company", "Ticker", "Market Cap ($M)", "EV ($M)", "Rev ($M)", "EBITDA ($M)", "EV/Rev", "EV/EBITDA", "Rev Growth"],
    "rows": [
        {"company": "Addus HomeCare", "values": ["ADUS", "1,781", "1,820", "1,565", "175", "1.2x", "10.4x", "10.0%"]},
        {"company": "BrightSpring", "values": ["BTSG", "5,820", "8,400", "11,200", "530", "0.8x", "15.8x", "12.5%"]},
        {"company": "Pennant Group", "values": ["PNTG", "3,940", "4,200", "765", "82", "5.5x", "51.2x", "18.2%"]},
        {"company": "Mean", "values": ["", "", "", "", "", "1.8x", "18.5x", "8.9%"], "summary": True},
        {"company": "Median", "values": ["", "", "", "", "", "1.1x", "12.7x", "8.4%"], "summary": True},
    ],
    "target_row": 0,
    "source": "Source: FactSet, Capital IQ. Market data as of April 2026."
})
```
