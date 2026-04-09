---
description: Build a DCF sensitivity grid (WACC × Terminal Growth → Implied Share Price)
argument-hint: "[company]"
---

# IB Sensitivity Grid

Build a DCF sensitivity table showing how implied share price changes with WACC and
terminal growth rate assumptions. Base case is highlighted in blue.

Load the `ib-deck-engine` skill and use `render_sensitivity`.

## What this slide shows

- **Row headers**: WACC values (e.g., 8.5% to 11.0%)
- **Column headers**: Terminal Growth Rate values (e.g., 2.0% to 4.0%)
- **Grid cells**: Implied share price for each (WACC, TGR) combination
- **Base case cell**: Highlighted with light blue background
- **Axis labels**: "WACC →" on left, "Terminal Growth Rate →" on top
- **Source citation** at bottom

## Workflow

If a company is provided as $1 and a DCF model exists, pull sensitivity values from
the DCF model. Otherwise ask the user for the values.

## Critical rules

- **Action title** — "DCF Sensitivity Analysis Across WACC and Terminal Growth Rate Assumptions" or similar
- **Base case must be highlighted** — set `base_row` and `base_col` (zero-indexed)
- **Values are pre-formatted strings** — "$129" not 129
- **Each cell should recalculate** — every grid cell should reflect a different (WACC, TGR) combination
- **Row and column counts must be ODD** — guarantees a true center cell for base case (5×5 or 7×5 are standard)

## Example spec

```python
r.render_sensitivity({
    "title": "DCF Sensitivity Analysis Across WACC and Terminal Growth Rate Assumptions",
    "table_label": "Implied Share Price ($)",
    "row_axis_label": "WACC →",
    "col_axis_label": "Terminal Growth Rate →",
    "data": {
        "row_headers": ["8.5%", "9.0%", "9.5%", "9.9%", "10.5%", "11.0%"],
        "col_headers": ["2.0%", "2.5%", "3.0%", "3.5%", "4.0%"],
        "values": [
            ["$147", "$159", "$174", "$194", "$220"],
            ["$136", "$146", "$158", "$174", "$194"],
            ["$126", "$135", "$145", "$157", "$173"],
            ["$119", "$127", "$129", "$145", "$158"],
            ["$111", "$118", "$125", "$134", "$145"],
            ["$104", "$110", "$117", "$125", "$134"],
        ],
        "base_row": 3,
        "base_col": 2,
    },
    "source": "Source: DCF model. Base case assumes 9.9% WACC, 3.0% terminal growth."
})
```
