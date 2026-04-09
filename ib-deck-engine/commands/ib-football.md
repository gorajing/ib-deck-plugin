---
description: Build a football field valuation summary slide
argument-hint: "[company]"
---

# IB Football Field

Build a single football field valuation summary slide using the `render_football_field`
template. The football field is THE signature IB valuation slide — it shows multiple
valuation methodologies as horizontal range bars with reference lines for key prices.

Load the `ib-deck-engine` skill and use the `render_football_field` template.

## What's in a football field

- **Category column** (left): pill labels for each methodology (DCF, Comps, LBO, 52-Week)
- **Methodology description** (left-center): brief assumptions for each method
- **Range bars** (center): horizontal bars showing the low-high valuation range, color-coded by category
- **Reference lines** (vertical): show important prices like current trading, offer price, DCF base case
- **Implied multiples** (right): TEV/EBITDA range for each methodology
- **X-axis price scale** (bottom): dollar tick marks

## Workflow

If a company is provided as $1, ask for valuation data. Otherwise ask:
- "What company are you valuing?"
- "What methodologies should I include?" (default: DCF perpetuity, DCF exit multiple, comps, LBO, 52-week)
- "Are there reference lines to highlight?" (current price, offer price, base case)

For each methodology, you need:
- Category label (short, fits in pill)
- Description (1-2 lines of assumptions)
- Low and high price values
- Bar color (matches category)
- Implied EV/EBITDA range

## Critical rules

- **Action title** — "Preliminary Valuation Summary Implies $X-$Y Per Share Across Methodologies"
- **Reference lines never overlap title** — collision detection is built-in
- **Price labels readable over reference lines** — built-in white background
- **Subtitle in italic gray** — "(All financials in $ per share unless otherwise stated)"
- **Source line at bottom** — cite DCF model file and FactSet/CapIQ as of date

## Example spec

```python
r.render_football_field({
    "title": "Preliminary Valuation Summary Implies $104-$174 Per Share Across Methodologies",
    "subtitle": "(All financials in $ per share unless otherwise stated)",
    "source": "Source: DCF model. FactSet consensus as of April 2026.",
    "methodologies": [
        {
            "category": "DCF\nPerpetuity",
            "category_color": "#1B365D",
            "description": "WACC: 8.5-11.0%\nTGR: 2.0-4.0%",
            "low": 104, "high": 174,
            "bar_color": "#1B365D",
            "implied_multiples": "8.5x - 15.2x"
        },
        # ... more methodologies
    ],
    "reference_lines": [
        {"price": 129, "label": "DCF Base", "color": "#1B365D"},
        {"price": 98, "label": "Current", "color": "#C00000"},
    ]
})
```

See `skills/ib-deck-engine/reference/examples/football_field.json` for a complete example.
