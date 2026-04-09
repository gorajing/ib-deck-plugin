# Schemas

Formal JSON Schema (draft 2020-12) definitions for the canonical slide specs
and handshake files proposed in [`../v0.2-scope.md`](../v0.2-scope.md).

These schemas turn the v0.2 proposal into a machine-checkable artifact. A tool
that wants to speak the canonical format does not need to read any prose — it
needs to validate against these files. An LLM that wants to generate specs
can be grounded on them directly. A reviewer who wants to know "is this
proposal concrete enough to react to" gets a definitive answer by running a
validator against the examples.

## What is here

### Template schemas (5, canonical core)

| File | Canonical name | Status in v0.1 | Status in v0.2 |
|---|---|---|---|
| [`financial_summary.schema.json`](financial_summary.schema.json) | `financial_summary` | Implemented as `render_financial_summary` | Schema matches current shape, plus optional `source_refs` and `unit` |
| [`trading_comps.schema.json`](trading_comps.schema.json) | `trading_comps` | Implemented as `render_trading_comps` | Schema matches current shape, plus optional `source_refs` and `unit` |
| [`transaction_comps.schema.json`](transaction_comps.schema.json) | `transaction_comps` | **Not implemented** | **New template.** Schema documents the proposed shape; renderer implementation is a v0.2 deliverable. |
| [`sensitivity.schema.json`](sensitivity.schema.json) | `sensitivity` | Implemented as `render_sensitivity` | Schema matches current shape, plus optional 2D `source_refs` grid |
| [`operating_metrics.schema.json`](operating_metrics.schema.json) | `operating_metrics` | Implemented as `render_dual_chart` | Canonical rename. `template` field accepts both `operating_metrics` and `dual_chart` (the latter as a deprecation alias that prints a one-line warning). |

The remaining 7 templates in the repo (`cover`, `section_divider`, `toc`,
`exec_summary`, `investment_highlights`, `stacked_bar_table`, `football_field`,
`sources_uses`) are **reference extensions**. They are not part of the
canonical core and do not have formal schemas in this directory. They remain
available through the renderer and are documented in
[`../../ib-deck-engine/skills/ib-deck-engine/reference/`](../../ib-deck-engine/skills/ib-deck-engine/reference/).

### Handshake file schemas (4)

| File | Purpose |
|---|---|
| [`source_refs.schema.json`](source_refs.schema.json) | Shared schema fragment for the `source_refs` arrays used by every template schema. Defines the four accepted forms: `null` (derived), bare cell string, explicit cell object, range object with aggregator. Referenced via `$ref` from each template schema. |
| [`provenance.schema.json`](provenance.schema.json) | Workbook-to-canonical-metric map produced by `/ib-import-excel`. Lives alongside the workbook file. |
| [`import_config.schema.json`](import_config.schema.json) | Workspace-local variant of provenance. Functionally equivalent; chosen when the analyst lacks write permission to the workbook's directory. |
| [`deck_exceptions.schema.json`](deck_exceptions.schema.json) | Durable record of reviewed intentional discrepancies. Consumed by `/ib-audit` to downgrade matched findings from FAIL to INFO. |
| [`audit_report.schema.json`](audit_report.schema.json) | Machine-readable output of `/ib-audit`. Every audit run produces exactly one of these. |

## Versioning

These schemas are the **v0.2 proposal** and will remain at this version for
as long as they are actively being reviewed. Once the proposal is either
accepted or iterated on meaningfully, a versioned subdirectory (e.g.,
`docs/schemas/v0.3/`) will be introduced. Until then, this directory holds
exactly one version of each schema and the `$id` fields point at the `main`
branch.

**Breaking change policy:** a breaking change to any schema requires bumping
the version and moving the old files to a versioned subdirectory so existing
consumers are not silently broken. Additive changes (new optional properties,
new enum values) do not require a version bump.

## Using the schemas

### Validation with Python's jsonschema

```python
import json
from jsonschema import Draft202012Validator

with open("docs/schemas/financial_summary.schema.json") as f:
    schema = json.load(f)

with open("my_slide.spec.json") as f:
    spec = json.load(f)

validator = Draft202012Validator(schema)
errors = sorted(validator.iter_errors(spec), key=lambda e: e.path)

if errors:
    for e in errors:
        print(f"  {list(e.path)}: {e.message}")
else:
    print("OK")
```

### Resolving cross-schema `$ref`

The template schemas reference `source_refs.schema.json#/$defs/sourceRefArray`
via a relative `$ref`. Python's `jsonschema` library resolves this
automatically when both files are loaded from the same directory. For tools
that need an explicit resolver, the schemas are also self-describing via their
absolute `$id` URIs (pointing at raw GitHub URLs).

### What the schemas do *not* enforce

Some rules in [`../v0.2-scope.md`](../v0.2-scope.md) cannot be expressed in
JSON Schema alone. These need to be enforced by the validator or the audit
layer, not by schema validation:

- **Parallel array length invariants.** `source_refs[i]` must be parallel to
  `values[i]`. JSON Schema cannot express "array A has the same length as
  array B at the same nesting level." The validator must check this
  separately.
- **`headers` length vs `rows[i].values` length.** Every row's values array
  must have `len(headers) - 1` entries. Not expressible in JSON Schema.
- **Unique canonical metric names within a provenance file.** Not expressible
  without JSON Schema 2020-12's `unevaluatedProperties` + custom logic.
- **`base_row` / `base_col` within data dimensions.** Sensitivity's base-case
  indices must be within the row/column header arrays. Schema validates the
  types but not the bounds.
- **Audit check semantics.** The 10 checks in v0.2-scope.md §6 are documented
  by the `audit_report.schema.json` `check` enum but their behavior is a
  validator responsibility, not a schema responsibility.

The intention is: schemas catch shape errors at authoring time; the audit
layer and validator catch semantic errors at run time.

### Value type conventions

The canonical templates use two different conventions for storing values. This
is a current-state observation, not an aspiration.

- **Table templates** (`financial_summary`, `trading_comps`, `transaction_comps`,
  `sensitivity`) store values as **pre-formatted display strings**. The caller
  is responsible for formatting (`"1,058,651"`, `"32.5%"`, `"$3.83"`) before
  handing the spec to the renderer.
- **Chart templates** (`operating_metrics`) store values as **numbers** (because
  bar heights are derived from them). The `secondary_values` array in
  `operating_metrics` stores pre-formatted strings for the display row below
  the bars.

A future version could unify this by allowing numeric values everywhere and
having the renderer format them via a declared `unit`. That is a v0.3
question and is not part of this proposal.

### Audit integration

A spec author who wants the audit to run against their slide should include:

1. `source_workbook` and `source_sheet_default` at the top of the spec
2. A `source_refs` array parallel to each row's `values` array
3. A `unit` declaration on each row (for the unit_mismatch check)

Any of the three can be omitted. When they are, the audit emits WARN-level
findings rather than FAIL. Partial adoption is a design goal.

## What is deliberately not here

- **Schemas for the 7 reference-extension templates** (cover, section_divider,
  toc, exec_summary, investment_highlights, stacked_bar_table, football_field,
  sources_uses). These are not being pitched as canonical primitives and do not
  need formal schemas in v0.2. If the canonical core is accepted, the
  extensions can graduate to the schemas directory one at a time.
- **A schema for the analyst workspace layout.** The example layout in
  `../v0.2-scope.md` §2 is a suggestion, not a mandated structure. Any tool
  that speaks these schemas can organize files however it wants as long as the
  individual files validate.
- **A schema for the `format` callable in `operating_metrics` charts.** The
  current renderer's Python API accepts an optional `format` callable per
  chart for custom value formatting. Callables cannot appear in a JSON spec,
  so the schema omits the field entirely. Specs that need custom formatting
  should pre-format their values or rely on the renderer default.
- **Excel formula references in `source_refs`.** The `source_refs` schema
  intentionally forbids formula references. The audit compares evaluated values
  only, not formula trees. If a spec needs a computed value, it lives in the
  spec as a derived row (with `source_refs: null`), not in the audit engine.

## Sanity check against existing examples

The schemas in this directory have been designed to validate the example JSON
files in
[`../../ib-deck-engine/skills/ib-deck-engine/reference/examples/`](../../ib-deck-engine/skills/ib-deck-engine/reference/examples/)
with the caveat that those examples do not carry a `template` discriminator
field. To validate an existing example against its schema, add
`"template": "<name>"` at the top level and remove the `_comment` field.

| Example file | Validates against |
|---|---|
| `financial_summary.json` | `financial_summary.schema.json` |
| `trading_comps.json` | `trading_comps.schema.json` |
| `sensitivity.json` | `sensitivity.schema.json` |
| `dual_chart.json` | `operating_metrics.schema.json` (via the `dual_chart` alias) |

The `comparison/input/financial_summary_spec.json` used by the
[`comparison/`](../../comparison/) artifact also validates, with the same
caveat about the `template` field.

## Open questions

Reproduced from [`../v0.2-scope.md`](../v0.2-scope.md) §10 for convenience,
scoped to the schemas specifically:

1. **Parallel array vs inline objects for `source_refs`.** v0.2 picks parallel
   arrays for compactness; inline-per-value objects would be more robust to
   row reordering but much more verbose. Pushback welcome.
2. **Should the value type convention be unified?** Today table templates use
   strings and chart templates use numbers. Unifying on numbers + unit-driven
   formatting is a v0.3 question.
3. **Should the canonical core be 5 or 7?** Adding `football_field` and
   `sources_uses` would cover M&A sell-side pitches; today they remain as
   reference extensions. Easy to promote if the Claude team prefers coverage
   over focus.
