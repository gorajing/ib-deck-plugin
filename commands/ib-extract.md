---
description: Extract a public company's 10-K financial data into a structured JSON master file
argument-hint: "[ticker]"
---

# IB Extract — 10-K to Master JSON

Pull a public company's most recent 10-K filing from SEC EDGAR and structure it as
a master JSON file that all downstream models and slides can reference.

## Why this exists

The single biggest architectural problem in IB workflows is **cross-model desync**:
the DCF, LBO, and pitch deck use different versions of the same numbers because each
was built independently. This command produces a single source of truth.

## Workflow

If a ticker is provided as $1, use it. Otherwise ask which company.

### Step 1: Pull the filing

Use `edgartools` to fetch the most recent original 10-K (not 10-K/A amendment):
```python
from edgar import Company, set_identity
set_identity("Your Name your@email.com")
c = Company("ADUS")
filing = c.get_filings(form="10-K", amendments=False).latest(1)
```

### Step 2: Extract structured data

Parse into this schema:
```json
{
  "metadata": {
    "company": "...", "ticker": "...", "cik": "...",
    "filing_date": "...", "fiscal_year_end": "...",
    "extraction_date": "...", "source": "SEC EDGAR via edgartools"
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
  "risk_factors": {...},
  "missing_data": [...]
}
```

### Step 3: Cross-checks

Verify before saving:
- Balance sheet balances: Assets = Liabilities + Equity (each year)
- Cash ties: Beginning + Net Change = Ending = BS Cash
- Net income flows: IS NI = CF starting NI
- Retained earnings rollforward: Prior RE + NI = Current RE

If any check fails, flag it in the JSON's `missing_data` field. Don't fabricate.

### Step 4: Save

Save as `{ticker}_master.json` in the current directory.

## Critical rules

- **Never fabricate data** — if a field is missing from the 10-K, mark it as null and note it in `missing_data`
- **Round to thousands** — all values in $000s for consistency
- **3 fiscal years minimum** — most recent + 2 prior
- **Source every assumption** — `effective_tax_rate_calc: "= 31,535 / 127,445"`

## Example

```
/ib-extract ADUS
```

Pulls Addus HomeCare's latest 10-K, extracts ~50 line items, runs 8 cross-checks,
saves as `ADUS_master.json`.
