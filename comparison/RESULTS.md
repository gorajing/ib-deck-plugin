# Results: Renderer-first vs prompt-guided spatial code

## What was compared

One slide type (`financial_summary`), one fixed input (ADUS 3-year historical),
two code paths:

- **Track A** — `IBRenderer().render_financial_summary(spec)` against a 18-line JSON spec.
- **Track B** — a hand-written `python-pptx` build script representing what an
  LLM plausibly writes on a first pass given the prompt and no reference to an
  existing renderer. Not engineered to fail.

Both tracks were run three times. Screenshots of `run1.pptx` from each track
are in `screenshots/`.

## Visual comparison (run 1)

| | Track A (renderer) | Track B (prompt-guided) |
|---|---|---|
| Screenshot | `screenshots/track_a_run1.png` | `screenshots/track_b_run1.png` |
| Action title | Rendered in navy bold; wraps to two lines at the library's default title font size | Rendered in navy bold; fits on one line (LLM chose a slightly smaller title area) |
| Section header bar | Navy rectangle, white bold text | Navy rectangle, white bold text |
| Table | Real PPTX table object | Real PPTX table object |
| Right-aligned numerics | Yes | Yes |
| Bold subtotal rows | Yes (Revenue, GP, EBITDA, NI, Diluted EPS) | Yes (Revenue, GP, EBITDA, NI — Diluted EPS is *not* bolded in Track B because the prompt listed it under subtotals but the build.py mapped it to `"normal"` style) |
| Italic gray `%` rows | Yes | Yes |
| EBITDA row highlight | Light blue background | Light blue background |
| Source citation | Present, bottom-left | Present, bottom-left |
| Slide number | Present (in a navy footer bar with "Investment Banking" label — library default) | Present (bare "6" in the bottom-right corner; no footer bar) |
| "Confidential" marker | Present, top-right, red italic | Present, top-right, red italic |
| Library branding | "Advisory Group" header, "Investment Banking" footer (library defaults; not in the prompt) | Absent (the prompt didn't mention them, so the LLM didn't add them) |
| Overflow / clipping | None observed | None observed |

**Honest read of the pictures:** on this single simple slide, both tracks
produce something a reviewer would accept. The prompt-guided version is not
broken. The differences that show up visually are cosmetic (title line-wrap,
presence/absence of library footer branding, one subtotal row that Track B's
build.py mis-classified).

## Code-size comparison

| | Track A | Track B |
|---|---|---|
| Lines of spatial code the LLM had to write | **0** | **166** non-blank code lines |
| `Inches(...)` calls | 0 | 32 |
| `Pt(...)` calls | 0 | 12 |
| `RGBColor(...)` calls | 0 | 10 |
| `PP_ALIGN.*` references | 0 | 6 |
| `MSO_SHAPE.*` references | 0 | 1 |
| Total artifact the LLM produces | `financial_summary_spec.json` — 18 lines, 1,262 chars | `build.py` — 213 lines including docstring |

Track A's `build.py` (45 lines) only loads the JSON and calls the renderer. The
45 lines are infrastructure, not LLM output. The actual LLM-produced artifact
is the JSON spec.

## Determinism (3 runs each)

Both tracks were run three times. PPTX files were hashed after stripping
volatile ZIP metadata (`dcterms:created`, `dcterms:modified`,
`cp:lastModifiedBy`, `cp:revision`) so that only the stable slide content
contributes to the hash. See `../tests/normalize.py`.

| | Track A | Track B |
|---|---|---|
| Unique hashes across 3 runs | 1 | 1 |
| Hash | `b36cff98f93cf143746bfb3726240a0fe83a10bf83cb6b2735b1303dcd6dd35e` | `410ae4ba5387034d4e3da8b68a17ca765041f5b4517984360e68359fa082234e` |

### What this determinism test does and does not prove

**What it proves:** running the same Python code twice produces the same PPTX
bytes, on both tracks. Track A's renderer is deterministic. Track B's
hand-written build script is also deterministic. Good, but unsurprising —
both are just Python files.

**What it does not prove:** whether an LLM, asked to build this slide *from
scratch* three separate times, would produce the same output three times. For
Track A, the LLM only needs to produce the same 18-line JSON spec, which is
much easier to keep stable across generations. For Track B, the LLM needs to
re-derive 32 `Inches()` positions, 12 `Pt()` sizes, and 10 `RGBColor()` values
from scratch each time. The variance that matters lives in the code the LLM
writes, not in running that code multiple times.

This test case does not attempt to measure LLM generation variance. It isolates
only the *architectural* variable: how much spatial code the LLM is asked to
produce in the first place.

## Where the difference actually lives

On a single slide in isolation, the two approaches are close. The renderer
approach starts to pull away when:

1. **The same layout appears on multiple slides.** A 20-slide deck with five
   financial_summary slides in Track A shares one renderer. In Track B, every
   slide is its own 150–200 line file, and drift between them is a natural
   outcome.
2. **Formatting conventions change.** Changing the navy color, the title font
   size, or the source-line position is a one-line edit in the renderer. In
   Track B it requires editing every build script.
3. **The data changes.** Track A: edit the JSON, rerun. Track B: re-run the
   same build script (fine) — or, if the LLM is regenerating each slide, write
   a fresh 150–200 line file each time.

None of the above is tested by this one-slide comparison. This comparison only
establishes that the *code-size difference* and the *single-pass determinism*
are real. The scaling properties are a separate claim.

## Criteria summary

| Criterion | Track A | Track B |
|---|---|---|
| Renders without errors | Pass | Pass |
| Honors IB formatting conventions listed in the prompt | Pass | Pass (with one subtotal misclassification) |
| No overflow / clipping | Pass | Pass |
| Uses a real PPTX table object | Pass | Pass |
| Lines of spatial code the LLM wrote | 0 | 166 |
| Normalized content hash stable across 3 runs of the same code | Yes (1/3) | Yes (1/3) |
| Measures LLM-generation variance | No | No |

## Conclusion (narrow)

On this single test case, renderer-first architecture produces the same slide
using zero lines of spatial code from the LLM, versus 166 lines for a
good-faith prompt-guided implementation. Both implementations render
deterministically on re-execution. Neither implementation's determinism result
speaks to LLM generation variance, which is the scaling question this
comparison does not attempt to answer.
