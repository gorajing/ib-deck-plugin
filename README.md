# IB Deck Engine — Claude Code Plugin

> A Claude Code plugin that ships a 14-template investment banking slide library with a JSON spec → deterministic pixel rendering architecture.

**Why this exists:** Other AI slide tools ask the LLM to write spatial code (`Inches(2.5), Pt(11)`). That's why their output has misaligned tables, disproportional bar charts, and reference label collisions. This plugin separates content reasoning (LLM's strength) from spatial rendering (deterministic code's strength). Right-alignment is guaranteed by the template, not hoped for.

## Installation

```bash
claude plugin marketplace add gorajing/ib-deck-plugin
claude plugin install ib-deck-engine@ib-deck-plugin
```

Or install directly:

```bash
git clone https://github.com/gorajing/ib-deck-plugin ~/.claude/plugins/local/ib-deck-plugin
```

Verify installation:

```bash
claude plugin list | grep ib-deck
```

## Available commands

| Command | Purpose |
|---------|---------|
| `/ib-deck [TICKER]` | Build a complete 14-slide IB pitch deck for a public company |
| `/ib-extract [TICKER]` | Pull a 10-K from SEC EDGAR into a structured JSON master file |
| `/ib-financial [COMPANY]` | Build a single financial summary table slide |
| `/ib-football [COMPANY]` | Build a football field valuation summary slide |
| `/ib-comps [TARGET]` | Build a trading comparables peer multiples table |
| `/ib-sources-uses [DEAL]` | Build an LBO Sources & Uses table |
| `/ib-sensitivity [COMPANY]` | Build a DCF sensitivity grid (WACC × TGR) |

## Quick start

```bash
# In Claude Code, after installing the plugin:
/ib-deck ADUS
```

Claude will:
1. Pull Addus HomeCare's most recent 10-K from SEC EDGAR via `edgartools`
2. Extract financials into a structured JSON master file
3. Fill JSON specs for 14 slide templates
4. Render a pixel-perfect PPTX using the IBRenderer
5. Save to `ADUS_pitch_deck.pptx`

The entire pipeline takes one prompt.

## What this plugin solves that the existing financial-services-plugins doesn't

I built this after analyzing the source code of `anthropics/financial-services-plugins`. Here are the specific gaps it fills:

### 1. Cross-model desync ✗ → ✓
The existing plugins build DCF and LBO independently. There's nothing guaranteeing both use the same revenue, EBITDA, share count, or tax rate. In a Medpace case study, the DCF used 15% effective tax and the LBO used 21% statutory with no documentation.

**This plugin's fix:** `/ib-extract` produces a single master JSON. Every downstream model and slide references it. A `cross_audit` function verifies consistency across DCF, LBO, and slides.

### 2. openpyxl corruption ✗ → ✓
The existing DCF skill (line 21) defaults to openpyxl for standalone xlsx generation. This produces files that trigger Excel's "We found a problem" recovery dialog.

**This plugin's fix:** Uses `xlsxwriter` by default for new file creation. openpyxl is only for reading existing files.

### 3. Spatial execution ceiling ✗ → ✓
The existing skills tell the LLM to write `python-pptx` code directly. The LLM has to remember `Inches(2.5), Pt(11)` for every cell. Failures: right-alignment inconsistent, bar heights not proportional, reference labels overlapping titles.

**This plugin's fix:** The LLM never writes spatial code. It picks a template (`render_financial_summary`) and fills a JSON spec. The IBRenderer guarantees:
- Right-alignment on all numeric columns
- Proportional bar heights (`value / max_value × chart_height`)
- Tables are real PowerPoint table objects (not text with tabs)
- Reference labels never overlap (collision detection built-in)
- Source text dynamically positioned below content

### 4. Generic titles ✗ → ✓
The existing plugins don't enforce action titles. You get "Financial Summary" instead of "Consistent Revenue Growth With Expanding EBITDA Margin Expansion".

**This plugin's fix:** SKILL.md explicitly requires action titles on every slide and gives examples.

### 5. No template library ✗ → ✓
The existing plugins make Claude generate slides from scratch each time. No reusable patterns.

**This plugin's fix:** 14 pre-built templates for the most common IB slide types, each with a documented JSON schema.

## The 14 templates

| # | Template | Pattern | Reference |
|---|----------|---------|-----------|
| 1 | `render_cover` | Cover with confidential mark + bank badge | GS board pres format |
| 2 | `render_section_divider` | Full navy bg with section title | GS / Moelis style |
| 3 | `render_toc` | Numbered agenda with light blue bands | GS agenda slides |
| 4 | `render_exec_summary` | Blue callout + ■ / — bullet hierarchy | GS executive summary |
| 5 | `render_investment_highlights` | 4-card 2×2 grid with numbered headers | GS / GS analyst format |
| 6 | `render_financial_summary` | Historical P&L with bold subtotals | Standard IB financials |
| 7 | `render_stacked_bar_table` | Stacked bars + data table below | Moelis revenue by segment |
| 8 | `render_dual_chart` | Two bar charts side by side with CAGR | GS dual analysis |
| 9 | `render_football_field` | Valuation methodologies with range bars | Evercore / Moelis |
| 10 | `render_sensitivity` | WACC × TGR grid with base case highlight | Standard DCF sensitivity |
| 11 | `render_sources_uses` | LBO capital structure (two-column) | Standard LBO |
| 12 | `render_trading_comps` | Peer multiples with target highlighted | Standard comps table |

See `skills/ib-deck-engine/reference/template-catalog.md` for the full pattern catalog and JSON schemas.

## Architecture

```
┌─────────────────────────────────────┐
│  CONTENT REASONING (Claude)         │
│                                     │
│  - Pick the right template          │
│  - Write the action title           │
│  - Select the data                  │
│  - Cite the source                  │
└────────────────┬────────────────────┘
                 │
                 │  Output: structured JSON
                 │
                 ▼
┌─────────────────────────────────────┐
│  JSON SPEC                          │
│  {                                  │
│    "title": "...",                  │
│    "headers": [...],                │
│    "rows": [...]                    │
│  }                                  │
└────────────────┬────────────────────┘
                 │
                 │  Pure data, no coordinates
                 │
                 ▼
┌─────────────────────────────────────┐
│  DETERMINISTIC RENDERER             │
│  - Right-alignment ALWAYS           │
│  - Proportional bars by math        │
│  - Real table objects               │
│  - Pixel-perfect by construction    │
└────────────────┬────────────────────┘
                 │
                 ▼
            output.pptx
```

This is the same architecture used by Beautiful.ai, Gamma, Pitch, UpSlide, and Macabacus. The LLM never touches pixels.

## Companion repo

The standalone Python library (without the plugin packaging) is at:
**https://github.com/gorajing/ib-deck-engine**

It includes a complete worked example for Addus HomeCare Corp (ADUS) — DCF model, LBO model, master JSON, and rendered 14-slide deck.

## Disclaimer

This is a learning case study and template library. Models are simplified. Numbers in the example case study are illustrative. Always verify financial data against primary sources before relying on it for investment decisions.

## License

MIT — see [LICENSE](LICENSE).
