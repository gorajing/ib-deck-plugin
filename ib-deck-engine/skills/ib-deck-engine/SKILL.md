---
name: ib-deck-engine
description: |
  Production-quality investment banking slide generation using a JSON spec → deterministic
  pixel rendering architecture. Use when the user wants to build IB pitch decks, financial
  summary slides, football fields, sensitivity grids, sources & uses tables, trading comps,
  or any structured banker presentation. Triggers on phrases like "build an IB deck",
  "create a financial summary slide", "DCF football field", "trading comps slide",
  "sources and uses", "pitch book", "discussion materials", "board presentation",
  "fairness opinion deck", or any company name combined with "pitch deck" or "deck".

  This skill solves the four critical failure modes that other AI slide tools hit:
  (1) Right-alignment inconsistent in financial tables — guaranteed by template
  (2) Bar heights not proportional to data — computed by engine
  (3) Reference line labels overlapping titles — collision-detected
  (4) Cross-model desync between DCF and LBO — single source of truth JSON

  Architecture: the LLM never writes spatial code (no Inches(), Pt(), or EMU values).
  Instead, the LLM picks the right template and fills a structured JSON spec. The
  IBRenderer Python class handles every pixel by construction.
---

# IB Deck Engine Skill

## When to use this skill

Use this skill any time the user wants to build investment banking presentations, including:
- Full pitch decks / discussion materials / board presentations
- Single slides (financial summary, football field, comps table, S&U)
- Sell-side or buy-side mandates
- Fairness opinions
- IC memos with embedded charts
- Pitch books with consistent formatting

Trigger phrases include: "build a pitch deck for [COMPANY]", "create an IB football field",
"DCF sensitivity table", "trading comps for [SECTOR]", "sources and uses slide",
"board discussion materials", "fairness opinion deck", "[COMPANY] pitch book".

## Architecture: JSON Spec → Renderer

This skill uses a separation-of-concerns architecture. The LLM (you) handles content
reasoning. A deterministic Python renderer handles pixel placement.

**Your job:**
1. Pick the right template for the slide type
2. Fill out the JSON spec for that template
3. Call `IBRenderer.render_*()` methods
4. Save the PPTX

**You never write:**
- `Inches()`, `Pt()`, `EMU()` values
- Pixel coordinates
- python-pptx shape positioning code
- Manual color hex placement

**The renderer guarantees:**
- Right-alignment on all numeric columns
- Proportional bar heights based on data ratios
- Tables are real PowerPoint table objects (not text with tabs)
- Reference line labels never overlap titles
- Source text always positioned below content, above footer
- Consistent chrome (logo, confidential mark, badge, slide number)

## Available templates

| Template | Method | Use for |
|----------|--------|---------|
| Cover | `render_cover` | Project cover slide with confidential mark and bank badge |
| Section Divider | `render_section_divider` | Full navy background with white section title |
| Table of Contents | `render_toc` | Numbered agenda with light blue bands |
| Executive Summary | `render_exec_summary` | Blue callout bar + ■ / — bullet hierarchy |
| Investment Highlights | `render_investment_highlights` | 4-card 2×2 grid with numbered headers |
| Financial Summary | `render_financial_summary` | Historical P&L with bold subtotals + italic % rows |
| Stacked Bar + Table | `render_stacked_bar_table` | Moelis revenue-by-segment pattern |
| Dual Chart | `render_dual_chart` | GS-style two charts side by side with CAGR labels |
| Football Field | `render_football_field` | Valuation summary with category pills + range bars |
| Sensitivity Grid | `render_sensitivity` | WACC × Terminal Growth → share price grid |
| Sources & Uses | `render_sources_uses` | LBO capital structure with balance check |
| Trading Comps | `render_trading_comps` | Peer multiples table with target highlighted |

See `reference/template-catalog.md` for full schema details and `reference/examples/` for working JSON specs.

## Workflow

### Step 1: Confirm what the user wants

If the user says "build an IB deck for ADUS", confirm:
- Single company sell-side pitch? Buy-side analysis? Fairness opinion?
- How many slides? (Full pitch book — ~14 slides using the 12 template types with section dividers reused — or specific slides?)
- Any specific data sources to use?

### Step 2: Get the data into the master JSON schema

The plugin does not automate SEC EDGAR extraction in this version. You have three
options for getting data into the master JSON schema:

1. **Ask the user** to paste financials or supply a CSV / existing JSON
2. **Write a short extraction script** using `edgartools` as a one-off (install
   separately: `pip install edgartools[ai]`)
3. **Use the companion case study** at github.com/gorajing/ib-deck-engine which
   has a worked ADUS extraction as a reference

The target JSON schema is documented in `reference/template-catalog.md`. Whatever
path you take, the output of this step should be a single JSON file that every
subsequent template call reads from — the "single source of truth" pattern prevents
cross-model desync.

### Step 3: Pick templates and fill specs

For each slide, pick the matching template and write a JSON spec:

```python
from ib_deck_engine import IBRenderer

r = IBRenderer()

r.render_financial_summary({
    "title": "Consistent Revenue Growth with Expanding Profitability",
    "section_header": "Historical Financial Summary ($ in thousands)",
    "headers": ["Metric", "FY2023A", "FY2024A", "FY2025A", "3Y CAGR"],
    "rows": [
        {"label": "Revenue", "values": ["1,058,651", "1,154,599", "1,422,530", "14.4%"], "style": "bold"},
        {"label": "% Growth", "values": ["11.3%", "9.1%", "23.2%", ""], "style": "pct"},
        {"label": "EBITDA", "values": ["105,082", "116,221", "155,027", "21.4%"], "style": "highlight"},
        {"label": "% Margin", "values": ["9.9%", "10.1%", "10.9%", ""], "style": "pct"},
    ],
    "source": "Source: SEC EDGAR. FY2025 10-K.",
})
```

### Step 4: Save and verify

```python
r.save("output.pptx")
```

Then verify by reading the output: confirm slide count, check that source text isn't
cut off, verify no text wrapping issues.

## Critical rules

### Action titles, not generic headers
WRONG: `"title": "Financial Summary"`
RIGHT: `"title": "Consistent Revenue Growth with Expanding EBITDA Margin Expansion"`

Every slide title must be a declarative thesis, not a label. This is the #1 IB
formatting standard. The audience should understand the slide's point from the title alone.

### Right-alignment is automatic — don't override
The templates already right-align numeric columns. You don't need to specify alignment
in the JSON spec. If you find yourself wanting to override, you're doing it wrong.

### Use real numbers, sourced
Every number on every slide must trace back to a source file (the master JSON, the DCF
model, the LBO model). Never invent numbers. If you don't have data, ask the user.

### Source citations on every slide
Every slide spec should include a `source` field. Format:
`"Source: SEC EDGAR via edgartools. FY2025 10-K filed February 24, 2026."`

### Cross-model consistency
When building both DCF and LBO models for the same company, document any assumption
differences explicitly:
- Tax rate: DCF uses effective rate, LBO uses 21% statutory (write WHY)
- Revenue growth: LBO can be more conservative (write WHY)
- These differences should be NOTED, not hidden

## Common patterns

### Pattern 1: Full pitch book (~14 slides using 12 template types + reused section dividers)
```python
r.render_cover({...})
r.render_toc({...})
r.render_exec_summary({...})
r.render_investment_highlights({...})
r.render_section_divider({"title": "Financial Performance"})
r.render_financial_summary({...})
r.render_stacked_bar_table({...})  # revenue by segment
r.render_dual_chart({...})  # revenue + EBITDA
r.render_section_divider({"title": "Valuation"})
r.render_football_field({...})
r.render_sensitivity({...})
r.render_trading_comps({...})
r.render_section_divider({"title": "LBO Analysis"})
r.render_sources_uses({...})
r.save("project_alpine.pptx")
```

See `reference/examples/full_deck.py` for a complete worked example that uses every
template and reuses `render_section_divider` for the three part breaks.

### Pattern 2: Single slide quick build
For users who want one slide, ask which template fits and just call that one method.

### Pattern 3: Update existing deck
The renderer creates new slides; it doesn't modify existing PPTX. For "update slide X
with new data," generate a fresh slide and ask the user to copy it into their deck.

## Troubleshooting

**"Right-alignment isn't working"** — You shouldn't need to set this. The renderer
does it automatically for all numeric columns in financial_summary, trading_comps,
sensitivity, and sources_uses templates.

**"Bars aren't proportional"** — Check the `values` array in your stacked_bar_table
or dual_chart spec. The renderer computes heights as `value / max_value * chart_height`.
If bars look wrong, your input data is wrong.

**"Source text is cut off"** — The renderer dynamically positions source text below
content. If it's cut off, your content is too tall. Reduce the number of rows in
the table or use a shorter chart.

**"Reference line labels overlapping"** — The football field template has built-in
collision detection. If two reference labels would overlap horizontally, the second
one bumps to a second row automatically.

**"openpyxl recovery dialog (when generating Excel separately)"** — If you're writing
your own Excel file alongside the slides, use `xlsxwriter` for new file creation.
openpyxl is only for reading/editing existing files. The `.pptx` rendering in this
plugin uses `python-pptx`, not openpyxl, and is not affected by this issue.

## Examples

See `reference/examples/` for working JSON specs you can copy as starting points:
- `financial_summary.json` — historical P&L table
- `football_field.json` — valuation summary with reference lines
- `stacked_bar_table.json` — stacked bars + data table (revenue by segment)
- `sources_uses.json` — LBO capital structure
- `trading_comps.json` — peer multiples table
- `dual_chart.json` — side-by-side bar charts with CAGR labels
- `sensitivity.json` — WACC × TGR grid
- `full_deck.py` — complete worked deck using every template

## Reference docs

- `reference/template-catalog.md` — All 12 templates with full JSON schemas
- `reference/style-guide.md` — Color palette, typography, formatting conventions
- `reference/architecture.md` — Why the renderer-first architecture produces more
  repeatable output than prompt-guided spatial code
