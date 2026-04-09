# IB Deck Engine — Claude Code Plugin

[![Tests](https://github.com/gorajing/ib-deck-plugin/actions/workflows/tests.yml/badge.svg)](https://github.com/gorajing/ib-deck-plugin/actions/workflows/tests.yml)

> A Claude Code plugin with a 12-template investment banking slide library built on a renderer-first architecture: the LLM fills structured JSON specs and a deterministic Python renderer handles every pixel.

**The core idea:** separate content reasoning (LLM's strength) from spatial rendering (deterministic code's strength). The LLM never writes `Inches()`, `Pt()`, or EMU values. It picks a template and passes data. The renderer guarantees right-alignment, proportional chart bars, and collision-free label placement by construction.

This plugin is an alternative architecture worth considering alongside [`anthropics/financial-services-plugins`](https://github.com/anthropics/financial-services-plugins). Different tradeoffs, smaller scope, tighter guarantees on the things it does cover.

## Status

**Version 0.1.0 — early prototype.** What's shipped today is the 12-template rendering library and slash-command workflows that guide Claude through filling the JSON specs. It's installable and runnable. Extraction, full model building, and cross-model auditing are workflow guides (not automated pipelines) in this version — see [Roadmap](#roadmap) for what's coming.

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

Each command loads the `ib-deck-engine` skill, which walks Claude through picking the right template, filling a JSON spec from your data, and calling the renderer. The commands are workflow guides — not autonomous pipelines.

| Command | Purpose |
|---------|---------|
| `/ib-deck [TICKER]` | Walk through building a complete IB pitch deck (orchestrates multiple templates) |
| `/ib-extract [TICKER]` | Guided workflow: extract 10-K data into the master JSON schema the templates expect |
| `/ib-financial [COMPANY]` | Build a single financial summary table slide |
| `/ib-football [COMPANY]` | Build a football field valuation summary slide |
| `/ib-comps [TARGET]` | Build a trading comparables peer multiples table |
| `/ib-sources-uses [DEAL]` | Build an LBO Sources & Uses table |
| `/ib-sensitivity [COMPANY]` | Build a DCF sensitivity grid (WACC × TGR) |

## Quick start

After installing the plugin and restarting Claude Code:

```
/ib-financial ADUS
```

Claude will load the skill, ask for the historical financials (or pull them from a JSON you provide), fill out the `render_financial_summary` JSON spec, and call the renderer. The output is a single PPTX slide with right-aligned numerics, bold subtotals, italic gray % rows, and a navy section header — rendered by deterministic Python code, not by the model guessing coordinates.

## The 12 templates

| # | Template | Pattern | Reference |
|---|----------|---------|-----------|
| 1 | `render_cover` | Cover with confidential mark + bank badge | GS board presentation format |
| 2 | `render_section_divider` | Full navy background with section title | GS / Moelis style |
| 3 | `render_toc` | Numbered agenda with light blue bands | GS agenda slides |
| 4 | `render_exec_summary` | Blue callout + ■ / — bullet hierarchy | GS executive summary |
| 5 | `render_investment_highlights` | 4-card 2×2 grid with numbered headers | GS highlights format |
| 6 | `render_financial_summary` | Historical P&L with bold subtotals | Standard IB financials |
| 7 | `render_stacked_bar_table` | Stacked bars + data table below | Moelis revenue by segment |
| 8 | `render_dual_chart` | Two bar charts side by side with CAGR | GS dual analysis |
| 9 | `render_football_field` | Valuation methodologies with range bars | Evercore / Moelis valuation |
| 10 | `render_sensitivity` | WACC × TGR grid with base case highlight | Standard DCF sensitivity |
| 11 | `render_sources_uses` | LBO capital structure (two-column) | Standard LBO |
| 12 | `render_trading_comps` | Peer multiples with target highlighted | Standard comps table |

See `skills/ib-deck-engine/reference/template-catalog.md` for the full pattern catalog.

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
                 │  Output: structured JSON spec
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
│  - Right-alignment of numeric cells │
│  - Bar heights computed from data   │
│  - Real PPT table objects           │
│  - Layout rules enforced in code    │
└────────────────┬────────────────────┘
                 │
                 ▼
            output.pptx
```

The LLM never writes `Inches()`, `Pt()`, `RGBColor()`, or pixel coordinates. Layout rules live in the renderer functions, enforced by code.

This is the same pattern used by Beautiful.ai, Gamma, and UpSlide: layout is a function of data, not a prompt-time decision.

## Tests

Determinism is the core promise of the architecture, so every template has a test that verifies it:

```bash
python -m pytest tests/ -v
```

13 tests pass:
- 12 per-template determinism tests (each template rendered twice, normalized content hashes compared)
- 1 stability test (`render_financial_summary` rendered 10 times, all 10 content hashes identical)

The tests use a [normalized PPTX hash](tests/normalize.py) that strips volatile ZIP metadata (creation timestamps, last-modified fields) before hashing, so only the parts of the output that affect appearance are compared.

This is the evidence trail for the "fixed input, repeated renders, identical output" claim. If any of those tests fail, the architecture's core promise is broken.

## What this architecture optimizes for

**Repeatability.** Same input → same output. The renderer doesn't depend on what the LLM felt like typing in any particular run.

**Evaluability.** "Did the LLM pick the right template and fill the right data?" is a simpler test than "did the LLM write correct python-pptx code for this specific slide?"

**Maintainability.** New templates are code, not prompts. They can be reviewed, versioned, and tested.

**Lower failure surface.** Every pixel decision the LLM doesn't make is a pixel decision that can't be wrong.

## What this plugin does not do (yet)

Being honest about the scope of v0.1.0:

- **No end-to-end SEC EDGAR extraction.** `/ib-extract` is a guided workflow that instructs Claude on the target JSON schema. A fully automated extraction command is on the roadmap.
- **No Excel model generation.** The companion standalone repo includes DCF and LBO `xlsx` build scripts for the ADUS case study, but they're not wired into the plugin as commands yet.
- **No cross-model audit command.** A programmatic 20-check audit exists in the companion repo for the ADUS case study. Making it a `/ib-audit` slash command is on the roadmap.
- **No Office JS / in-PowerPoint support.** The renderer is python-pptx. It produces `.pptx` files from outside PowerPoint. An Office JS port would be needed for Cowork / in-PowerPoint use.
- **Only 12 templates.** Real IB decks use ~25-30 patterns. See the [roadmap](#roadmap) for what's coming next.

## Roadmap

v0.2.0 goals:
- Expand template library to 20+ (add precedent transactions, multi-chart dashboard, share price chart, debt schedule, value creation bridge, process timeline, buyer universe grid)
- Automated `/ib-extract` that calls `edgartools` and produces the master JSON
- Automated `/ib-dcf-model` and `/ib-lbo-model` using xlsxwriter
- `/ib-audit` cross-model consistency check

v0.3.0 goals:
- Bank style variants (Moelis, Evercore, McKinsey presets)
- MCP server wrapper so the renderer works in Claude Desktop and Cowork
- Determinism test expansion to every template
- GitHub Pages gallery

## Companion repo

The standalone Python library (without the plugin packaging) and the complete ADUS case study artifacts live at **[gorajing/ib-deck-engine](https://github.com/gorajing/ib-deck-engine)**. That repo includes the DCF model (401 formulas), LBO model (244 formulas), master JSON extraction example, and a 14-slide rendered ADUS deck.

## Disclaimer

This is a learning project and early prototype. Models in the companion case study are simplified. Example numbers are illustrative. Always verify financial data against primary sources before relying on it for any investment decision.

## License

MIT — see [LICENSE](LICENSE).
