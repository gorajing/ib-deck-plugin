---
description: Guided workflow for structuring a company's financials into the master JSON schema
argument-hint: "[ticker]"
---

# IB Extract — Master JSON Workflow Guide

Walks Claude through assembling a company's financial data into the master JSON
schema that every downstream template reads from.

## What this command IS (in v0.1.0)

A workflow guide that tells Claude:
- What fields the master JSON should contain
- What cross-checks to run (balance sheet balances, cash ties, etc.)
- How to format the output so downstream templates can read it

## What this command is NOT (in v0.1.0)

- **Not an autonomous SEC EDGAR pipeline.** This version does not ship with an
  automated extractor bundled into the plugin. If you want automated extraction,
  either install `edgartools[ai]` separately and write a short one-off script,
  or see the worked extraction example in the companion repo at
  github.com/gorajing/ib-deck-engine.
- **Not a parser.** Claude structures data the user provides (pasted financials,
  uploaded JSON, manual entry) into the schema.

A fully automated `/ib-extract` that directly calls `edgartools` is on the
[v0.2.0 roadmap](../../../README.md#roadmap).

## Why a structured master JSON matters

The "single source of truth" pattern prevents cross-model desync. If the DCF, LBO,
and pitch deck all read from the same JSON, they cannot diverge on revenue, EBITDA,
share count, or tax rate. Every downstream template call reads from the same source.

## The target schema

```json
{
  "metadata": {
    "company": "...", "ticker": "...", "cik": "...",
    "filing_date": "...", "fiscal_year_end": "...",
    "extraction_date": "...", "source": "..."
  },
  "income_statement": {
    "FYxxxxA": {
      "total_revenue": ..., "cost_of_revenue": ...,
      "gross_profit": ..., "general_and_administrative": ...,
      "depreciation_and_amortization": ..., "operating_income": ...,
      "interest_expense": ..., "pretax_income": ...,
      "income_tax_expense": ..., "net_income": ...,
      "ebitda": ..., "eps_diluted": ...,
      "basic_shares": ..., "diluted_shares": ...,
      "margins": {...}, "revenue_growth": ...
    }
  },
  "balance_sheet": {...},
  "cash_flow": {...},
  "share_count": {...},
  "key_assumptions": {...},
  "debt_detail": {...},
  "business_description": {...},
  "missing_data": [...]
}
```

A complete example is in the companion repo:
https://github.com/gorajing/ib-deck-engine/blob/main/case_study/adus_10k_master.json

## Workflow

If a ticker is provided as $1, use it. Otherwise ask:
"What company are we working on, and how is the data arriving — pasted financials,
CSV, existing JSON, or should we walk through the 10-K together?"

### Step 1: Get the source data

Options in priority order:
1. User provides existing structured data (JSON / CSV / pasted financials)
2. User has the 10-K filing and wants to walk through the key line items together
3. User runs a one-off `edgartools` script separately

### Step 2: Structure into the schema

Fill each field. For anything missing from the source, add it to the `missing_data`
array with a note on what's needed. **Never fabricate numbers to fill gaps.**

### Step 3: Run cross-checks

Before saving:
- Balance sheet balances: Assets = Liabilities + Equity (each year)
- Cash ties: Beginning + Net Change = Ending = BS Cash
- Net income flows: IS NI = CF starting NI
- Retained earnings rollforward: Prior RE + NI = Current RE

If any check fails, flag it in `missing_data`.

### Step 4: Save

Save as `{ticker}_master.json` in the current working directory.

## Critical rules

- **Never fabricate data** — null values with notes in `missing_data` are always
  better than guessed numbers
- **Round consistently** — all values in $000s for consistency across templates
- **3 fiscal years minimum** — most recent + 2 prior
- **Source every assumption** — e.g., `"effective_tax_rate_calc": "= 31,535 / 127,445"`

## Example

```
/ib-extract ADUS
```

Walks through structuring Addus HomeCare's financials. A complete reference output
lives at `case_study/adus_10k_master.json` in the companion repo.
