# IB Slide Layout Catalog

Extracted from real bank decks: Goldman Sachs (PowerSchool), Moelis (Avangrid), Evercore (Diversey).

Every complex IB slide is a **multi-zone composition** — never a single chart or single table.

---

## ZONE SYSTEM

Real IB slides use a grid system. The content area (below title, above footer) is divided into zones:

```
┌──────────────────────────────────────────────┐
│  TITLE (action title, 1-2 lines)             │
│  CALLOUT BAR (optional, full-width)          │
├──────────────────────────────────────────────┤
│                                              │
│  CONTENT ZONES (2-4 zones arranged in grid)  │
│                                              │
├──────────────────────────────────────────────┤
│  SOURCE / FOOTNOTES                          │
│  FOOTER (bank name, confidential, page #)    │
└──────────────────────────────────────────────┘
```

---

## LAYOUT PATTERNS (15 distinct types)

### 1. SINGLE TABLE (Simple)
**Example:** Moelis Key Terms, GS Financial Summary
```
┌──────────────────────┐
│  Table (full width)  │
└──────────────────────┘
```
Already built in engine v1.

---

### 2. CHART + OVERLAID DATA TABLE
**Example:** GS Slide 11 (Share Price Performance Since IPO)
```
┌─────────────────────────────────────┐
│  Line Chart (full width)            │
│           ┌──────────┐              │
│           │ Mini-table│ (overlaid)  │
│           │ Perf (%)  │             │
│           └──────────┘              │
│                          end labels │
└─────────────────────────────────────┘
```
- Multi-series line chart spanning full content width
- Small summary table OVERLAID in top-right corner of chart
- End-point labels on right edge (20.3%, 15.2%, etc.)
- Legend centered below chart

---

### 3. CHART + SIDEBAR STATS
**Example:** GS Slide 12 (Stock Price Range Bound)
```
┌───────────────────┬─────────────┐
│  Line Chart       │ Stats Table │
│  (60% width)      │ (VWAPs)     │
│  w/ annotations   │ Right-align │
│  52wk H/L callout │             │
│  ┌──────────┐     │             │
│  │ Mini-tbl │     │             │
│  │ Avg Vol  │     │             │
│  └──────────┘     │             │
└───────────────────┴─────────────┘
```
- Chart with annotation callouts (52-week high/low lines + labels)
- Right sidebar: VWAP statistics table (metric name left, $ value right)
- Mini-table embedded INSIDE the chart area (trading volume)

---

### 4. DUAL CHARTS SIDE-BY-SIDE
**Example:** GS Slide 13 (NTM EV/Revenue + EV/EBITDA)
```
┌────────────────┬────────────────┐
│  Line Chart 1  │  Line Chart 2  │
│  EV/Revenue    │  EV/EBITDA     │
│  ┌─────┐       │  ┌─────┐       │
│  │table│       │  │table│       │
│  └─────┘       │  └─────┘       │
│     end labels │     end labels │
└────────────────┴────────────────┘
```
- Two charts, equal width (50/50)
- Each has its own overlaid mini-table
- Each has end-point labels
- Shared x-axis time range and source line

---

### 5. TABLE TOP + DUAL CHARTS BOTTOM
**Example:** GS Slide 14 (Research Analyst Views)
```
┌──────────────────────────────────┐
│  Dense Table (Date, Analyst,     │
│  Rating, Target, Rev, EBITDA...) │
│  Median/High/Low summary rows   │
├────────────────┬─────────────────┤
│  Line Chart    │  Stacked Bar    │
│  Price + TP    │  Buy/Hold/Sell  │
└────────────────┴─────────────────┘
```
- 3-zone layout: full-width table top, two charts bottom
- Table has Median/High/Low/Variance summary rows
- Bottom-left: price vs target price line chart
- Bottom-right: ratings distribution stacked bar

---

### 6. LIST LEFT + CARD GRID RIGHT
**Example:** GS Slide 16 (Investment Highlights)
```
┌──────────────────┬──────────────┐
│  Stacked thesis  │  2×2 Card    │
│  point bars (9)  │  Grid with   │
│  (rounded rects) │  icons       │
│  w/ left borders │  (colored)   │
│                  │              │
└──────────────────┴──────────────┘
```
- Left: 9 horizontal rounded rectangle bars with thesis statements
- Right: 2×2 grid of colored cards (purple, orange, blue, light blue) with icons and text

---

### 7. STACKED BAR CHART + DATA TABLE BELOW
**Example:** Moelis Slides 9-10 (Revenue/Capex by Type) — THE most common Moelis pattern
```
┌──────────────────────────────────┐
│  Section Header Bar (navy)       │
├──────────────────────────────────┤
│  Stacked Bar Chart               │
│  w/ total labels on top          │
│  w/ segment colors               │
│  w/ legend below chart           │
├──────────────────────────────────┤
│  Data Table (underlying numbers) │
│  Matching column alignment       │
│  Color-coded row labels          │
└──────────────────────────────────┘
```
- Navy header bar with white text (e.g., "Revenue ($ mm)")
- Stacked bar chart with total value labels above each bar
- Data table directly below with the EXACT numbers from the chart
- Column alignment matches perfectly (same years as chart bars)
- This is the most data-dense standard pattern

---

### 8. MULTI-CHART DASHBOARD (4 zones)
**Example:** Moelis Slide 8 (Summary of Management Forecast)
```
┌───────────────────┬──────────────────┐
│  Text Overview    │  Stacked Bar 1   │
│  (bullets)        │  (CapEx by type) │
│                   │  + ratio labels  │
├───────────────────┼──────────────────┤
│  Stacked Bar 2   │  Stacked Bar 3   │
│  (EBITDA)         │  (Net Income)    │
│  + line overlay   │  + EPS labels    │
│  + CAGR labels    │  + line overlay  │
└───────────────────┴──────────────────┘
```
- 4-zone grid (2×2)
- Each chart has its own title, legend, data labels
- Line overlays showing consolidated totals
- CAGR callouts between chart segments

---

### 9. ANALYSIS AT VARIOUS PRICES (Dense Matrix)
**Example:** Moelis Slide 5, Evercore Slide 7
```
┌──────────────────────────────────────────┐
│  Multi-column table                       │
│  Color-coded header blocks per proposal  │
│  Section 1: Price, Premia, Market Cap    │
│  Section 2: TEV, Implied Multiples       │
│  Section 3: P/E Multiples               │
│  Highlighted "proposed" column           │
└──────────────────────────────────────────┘
```
- 8-15 columns with different proposals/prices
- Color-coded column headers (blue, green, yellow per bidder)
- Multiple sub-sections within one table
- Right-aligned financial numbers throughout
- Summary statistics (median, high, low, variance)

---

### 10. FOOTBALL FIELD (Valuation Summary)
**Example:** Evercore Slide 8 (Preliminary Valuation Summary), Moelis Slide 14
```
┌─────────┬───────────┬──────────────────┬──────────────┐
│Category │Methodology│  Horizontal Bars │ Implied      │
│Labels   │Description│  (range)         │ Multiples    │
│(colored │           │  ◄────────────►  │              │
│ pills)  │           │  $5.75    $9.06  │ 11.2x-14.4x │
│         │           │                  │              │
│         │           │ ▼ Offer line     │              │
│         │           │ ▼ Current line   │              │
└─────────┴───────────┴──────────────────┴──────────────┘
```
- Left sidebar: category pills (Core=navy, Precedent=orange, Reference=gray)
- Methodology column: text descriptions with assumptions
- Center: horizontal range bars (colored by category)
- Vertical reference lines (unaffected price, current price, proposed price)
- Right column: implied TEV/EBITDA multiples
- THE signature IB valuation slide

---

### 11. PILL-LABEL + BULLET CONTENT (Moelis Style)
**Example:** Moelis Slides 7, 12-13 (Financial Plan Overview)
```
┌──────────────────────────────────────┐
│ Full-width subtitle bar              │
├──────────┬───────────────────────────┤
│ Navy     │ • Bullet content          │
│ Pill     │ • Multiple lines          │
│ Label    │   ○ Sub-bullets           │
├──────────┼───────────────────────────┤
│ Navy     │ • Bullet content          │
│ Pill     │ • With specific data      │
│ Label    │                           │
├──────────┼───────────────────────────┤
│ Navy     │ • More bullets            │
│ Pill     │   ○ Sub-level detail      │
│ Label    │   ○ With footnote refs    │
└──────────┴───────────────────────────┘
```
- Built in engine v1 but needs refinement for multi-row content
- Variable row heights based on bullet count
- Some rows have sub-bullets with circle (○) markers
- Left-side category labels can also be rotated text (like "For reference only")

---

### 12. EVERCORE TOC / SECTION DIVIDER
**Example:** Evercore Slides 3, 4, 9
```
┌──────────────────────────────────┐
│                                  │
│  ██  (navy vertical bar)         │
│  ██                              │
│  ─────────────────────────────── │
│  ─────────────────────────────── │
│  Section Title (blue text)       │
│                                  │
│             [Table of Contents]  │
└──────────────────────────────────┘
```
- Small navy vertical rectangle (like a bookmark marker)
- Double horizontal rule (red/blue for Evercore)
- Section title in blue
- "Table of Contents" button/link bottom-right
- Very minimal, distinctive Evercore brand

---

### 13. EVERCORE BULLET HIERARCHY
**Example:** Evercore Slides 4-5 (Transaction Background, Review Status)
```
■  Main point (bold)
   ► Sub-point (regular)
      • Detail (regular, smaller)
      • Detail with bold keywords
   ► Sub-point
■  Main point 2
   ► Sub-point
```
- Three-level bullet hierarchy
- ■ (filled square) for main points
- ► (right arrow/triangle) for sub-points
- • (bullet) for detail level
- Bold dates at start of timelines (underlined)
- This is denser than GS bullet style

---

### 14. COLOR-CODED MULTI-COLUMN HEADER TABLE
**Example:** Moelis Slide 5 (Analysis at Various Prices)
```
┌─────────────┬────────┬────────┬────────┬────────┬────────┐
│             │Unaffct.│Indiana │Arizona │Indiana │Proposed│
│             │ Date   │Proposal│Proposal│Proposal│ Trans. │
│             │3/6/2024│3/7/2024│4/26/24 │5/1/24  │6/7/24  │
├─────────────┼────────┼────────┼────────┼────────┼────────┤
│Share Price  │ $32.08 │ $34.25 │ $38.25 │ $34.75 │ $35.75 │
│Mkt Cap      │  $12.5 │  $13.3 │  $14.8 │  $13.5 │  $13.9 │
├─────────────┼────────┼────────┼────────┼────────┼────────┤
│% Premium    │        │  (15%) │   (9%) │   2%   │   (5%) │
```
- Each column group has a distinct color header (Indiana=blue, Arizona=green, Proposed=yellow)
- Dense numerical data throughout
- Multiple logical sections within one table
- Parenthetical negatives right-aligned
- The final "Proposed Transaction" column is highlighted

---

### 15. MULTI-PANEL TEXT + IMAGES
**Example:** GS Slides 17-19 (Growth Strategy, AI, Cross-Sell)
```
┌───────────────────────────────────┐
│  Callout bar (full width, blue)   │
├──────────┬──────────┬─────────────┤
│  Panel 1 │  Panel 2 │  Panel 3    │
│  Image + │  Bullets │  Colored    │
│  Text    │  + Data  │  Cards      │
│  overlay │          │  (stacked)  │
├──────────┴──────────┴─────────────┤
│  Big Metric Cards (2-3 across)    │
│  "107%"  Net Retention             │
│  "33%"   EBITDA Margin            │
└───────────────────────────────────┘
```
- Top: callout bar
- Middle: 3-column panels (mix of images, bullets, cards)
- Bottom: big metric callout cards (large number + label)
- Logos embedded in text sections

---

## PRIORITY FOR ENGINE v2

### Must Build (used in every IB deck):
1. **#7 Stacked Bar + Data Table** — Moelis bread-and-butter
2. **#10 Football Field** — THE valuation summary slide
3. **#4 Dual Charts Side-by-Side** — GS trading analysis
4. **#3 Chart + Sidebar Stats** — GS price/VWAP analysis
5. **#9 Dense Multi-Column Table** — analysis at various prices

### Should Build:
6. **#5 Table Top + Dual Charts Bottom** — analyst views
7. **#8 Multi-Chart Dashboard (2×2)** — management forecast
8. **#6 List Left + Card Grid Right** — investment highlights

### Nice to Have:
9. **#2 Chart + Overlaid Mini-Table** — performance with stats
10. **#15 Multi-Panel Text + Images** — growth strategy

---

## KEY ENGINE CAPABILITIES NEEDED

1. **Zone-based composition** — define 2×1, 1×2, 2×2 grids with relative sizing
2. **Proportional bar rendering** — bar heights MUST match data ratios
3. **Stacked bar segments** — multiple colors per bar, proportional segments
4. **Data labels on charts** — above bars, at end-points of lines, CAGR annotations
5. **Overlaid mini-tables** — position a small table INSIDE a chart area
6. **Horizontal range bars** — for football field (left edge = low, right edge = high)
7. **Vertical reference lines** — for football field price markers
8. **Category pill labels** — colored pills in left sidebar (navy, orange, gray)
9. **Color-coded column headers** — different colors per column group
10. **Line chart rendering** — multi-series with end-point labels

### python-pptx limitations for charts:
- python-pptx CAN create native Excel-backed charts (bar, line, pie)
- But formatting them precisely (data labels, annotation callouts, overlaid shapes) requires XML manipulation
- For v2, start with table-based charts (rectangles as bars) for full control
- Graduate to native charts when layout is proven
