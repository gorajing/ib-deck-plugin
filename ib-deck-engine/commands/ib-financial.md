---
description: Build a financial summary table slide (historical P&L)
argument-hint: "[company]"
---

# IB Financial Summary

Build a single financial summary table slide using `render_financial_summary`. This is
the standard "show me 3 years of historicals with bold subtotals and italic gray % rows"
slide that appears in every IB pitch book.

Load the `ib-deck-engine` skill and use the `render_financial_summary` template.

## What this slide shows

A clean financial table with:
- 3+ historical years (with optional CAGR column)
- Bold subtotal rows: Revenue, Gross Profit, EBITDA, Net Income
- Italic gray % rows: % Growth, % Margin
- Highlighted EBITDA row (light blue background)
- Right-aligned numeric columns (decimal points stack vertically)
- Action title (declarative thesis, not "Financial Summary")
- Source citation at bottom

## Workflow

If a company is provided as $1 and a master JSON exists, load the JSON and pull historical
financials. Otherwise ask the user for the data.

## Critical rules

- **Action title is mandatory** — "Consistent Revenue Growth With Expanding EBITDA Margin Expansion" not "Financial Summary"
- **Right-alignment is automatic** — every numeric column right-aligns by default
- **Bold subtotals automatically** — set `"style": "bold"` for Revenue/GP/EBITDA/NI rows
- **Italic gray % rows automatically** — set `"style": "pct"` for growth/margin rows
- **EBITDA row highlight** — set `"style": "highlight"` for the most important row
- **Numbers as strings** — values come in as formatted strings ("1,058,651" not 1058651) so the renderer respects your formatting

## Example spec

```python
r.render_financial_summary({
    "title": "Addus Has Delivered Consistent Revenue Growth with Expanding Profitability",
    "section_header": "Historical Financial Summary ($ in thousands)",
    "headers": ["Metric", "FY2023A", "FY2024A", "FY2025A", "3Y CAGR"],
    "rows": [
        {"label": "Revenue", "values": ["1,058,651", "1,154,599", "1,422,530", "14.4%"], "style": "bold"},
        {"label": "% Growth", "values": ["11.3%", "9.1%", "23.2%", ""], "style": "pct"},
        {"label": "Gross Profit", "values": ["339,876", "375,021", "461,874", "16.6%"], "style": "bold"},
        {"label": "% Margin", "values": ["32.1%", "32.5%", "32.5%", ""], "style": "pct"},
        {"label": "EBITDA", "values": ["105,082", "116,221", "155,027", "21.4%"], "style": "highlight"},
        {"label": "% Margin", "values": ["9.9%", "10.1%", "10.9%", ""], "style": "pct"},
        {"label": "Net Income", "values": ["62,516", "73,598", "95,910", "23.8%"], "style": "bold"},
        {"label": "Diluted EPS", "values": ["$3.83", "$4.23", "$5.22", "16.7%"], "style": "normal"},
    ],
    "source": "Source: SEC EDGAR. ADUS FY2025 10-K filed February 24, 2026."
})
```
