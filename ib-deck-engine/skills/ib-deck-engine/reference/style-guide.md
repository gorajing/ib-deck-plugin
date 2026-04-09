# Style Guide

Formatting conventions and design tokens used by the IB Deck Engine templates.

## Color palette (GS-inspired default)

The default `BankStyle` in `templates.py` uses a restrained navy + gray palette
inspired by Goldman Sachs board presentation decks:

| Token | Hex | Used for |
|-------|-----|----------|
| `primary` | `#1B365D` | Main navy — titles, section headers, bar fills, pill labels |
| `primary_light` | `#3B6B9D` | Secondary accent (dual-tone sections) |
| `secondary` | `#A7C4E0` | Light blue — callouts, badge strip |
| `accent_orange` | `#E07020` | Comps / precedent bars |
| `accent_green` | `#2E8B57` | LBO / positive callouts |
| `accent_red` | `#C00000` | "Confidential" mark, negative reference lines |
| `bg` | `#EDEDED` | Slide background (cover, content slides) |
| `text` | `#1F1F1F` | Body text |
| `muted` | `#666666` | Source lines, secondary labels |
| `border` | `#BBBBBB` | Table borders |
| `row_alt` | `#F5F5F5` | Alternating row backgrounds |
| `header_bg` | `#D6E4F0` | Light blue for table headers and callout bars |
| `highlight` | `#FFF2CC` | Yellow for highlighted rows (target company in comps) |

### Distinct segment palette for stacked bars

```
#1B365D (navy)  →  #4B7BA8 (mid blue)  →  #8EB4D6 (light blue)
```

Avoid using two segment colors that are too close in value. The default palette
steps through blue lightness so segments are clearly distinguishable.

## Typography

| Element | Font | Size | Weight |
|---------|------|------|--------|
| Slide title | Calibri | 24pt | Bold |
| Subtitle / section header bar text | Calibri | 11pt | Bold |
| Body text | Calibri | 11pt | Normal |
| Table header | Calibri | 9-10pt | Bold |
| Table body | Calibri | 9-10pt | Normal |
| Bold row labels (Revenue, EBITDA, etc.) | Calibri | 10pt | Bold |
| Italic gray rows (% Growth, % Margin) | Calibri | 10pt | Italic |
| Source line | Calibri | 8pt | Italic |
| Cover title | Georgia | 36pt | Bold |
| Cover subtitle | Calibri | 18pt | Normal |

Georgia is used only on the cover slide for a slightly more classical feel.
All other text uses Calibri.

## Formatting rules enforced by the renderer

These are not optional prompts — the renderer code enforces them:

1. **Numeric columns are right-aligned.** Any column index > 0 in a financial
   table gets `PP_ALIGN.RIGHT` applied by the template function.
2. **Bar heights are proportional to data.** Computed as
   `(value / max_value) * chart_height`, never approximated.
3. **Tables are real PPT table objects.** The renderer calls
   `slide.shapes.add_table(...)` — never text boxes with tabs.
4. **Alternating row backgrounds.** Applied automatically in templates that
   have more than 4 data rows.
5. **Source text is positioned dynamically.** Templates compute the source line
   position based on where the table/chart ends, not at a fixed y.
6. **Reference line labels avoid collisions.** The football field template
   detects horizontal overlap and bumps labels to a second row.

## Action titles, not generic headers

Every slide title must be a declarative thesis. The audience should understand
the slide's point from the title alone.

| Generic (wrong) | Action title (right) |
|-----------------|----------------------|
| "Financial Summary" | "Consistent Revenue Growth With Expanding EBITDA Margin Expansion" |
| "Valuation" | "Preliminary Valuation Summary Implies $104-$174 Per Share Across Methodologies" |
| "Revenue by Segment" | "Personal Care Dominates Revenue Mix With Accelerating Growth Across All Three Segments" |
| "Investment Highlights" | "Scaled Platform With Secular Tailwinds and Proven Acquisition Engine" |
| "LBO" | "Sponsor Returns of 2.5x / 20% IRR at 12x Entry With Leverage of 4.5x" |

This isn't just a best practice — it's the #1 formatting convention in real
investment banking pitch books.

## Source citations on every slide

Every content slide should have a source line at the bottom. Format:

```
Source: SEC EDGAR via edgartools. FY2025 10-K filed February 24, 2026.
```

Or for multiple sources:

```
Source: SEC EDGAR. FactSet consensus estimates as of April 2026. Internal LBO model.
```

The source line should be 8pt italic gray, positioned just above the footer badge.

## Unit conventions

- Financial amounts: `$000s` unless otherwise stated
- Multiples: `0.0x` or `0.00x` (MOIC gets 2 decimals, never rounded up)
- Percentages: `0.0%` (one decimal) for margins and growth rates
- Dates: ISO format in JSON (`2026-04-09`), human format in slide text ("April 2026")

## Customizing for other banks

All style tokens live in the `BankStyle` dataclass at the top of `templates.py`.
Swapping banks means constructing a new `BankStyle` with different colors and
passing it to `IBRenderer(style=...)`. Bank-specific presets (Moelis, Evercore,
McKinsey) are on the roadmap.
