# Comparison: renderer-first vs prompt-guided spatial code

This folder contains a tightly controlled before/after comparison of two
approaches to building a single financial-summary slide:

- **Track A — renderer-first.** The LLM writes only a JSON spec and calls
  `IBRenderer().render_financial_summary(spec)`. No `Inches()`, no `Pt()`, no
  `RGBColor()`, no shape manipulation. The renderer owns every pixel.
- **Track B — prompt-guided spatial code.** The LLM writes `python-pptx` code
  directly, making every position, size, alignment, and color decision in the
  same file.

The goal is to isolate the architectural variable — how much spatial code the
LLM is responsible for — and observe the consequences on a single concrete task.

## Why this comparison and not an apples-to-apples comparison with another plugin

The obvious comparison would be against Anthropic's `financial-services-plugins`.
That comparison is not what this folder contains, because that plugin does not
expose a "build one financial_summary slide from this fixed data" primitive.
Forcing an apples-to-apples run against a plugin that is solving a slightly
different task would either (a) require a lot of adapter code that would itself
become the variable under test, or (b) produce a misleading result.

What this comparison does instead: hold the task and the input fixed, vary
only the architecture. The Track B build script is what someone would plausibly
write starting from `input/prompt.txt`, `python-pptx` documentation, and no
reference to an existing renderer. That is the condition any LLM operates under
when it is asked to produce a slide without a slide library.

## Methodology

1. **Fixed task.** Build one PPTX slide containing Addus HomeCare's 3-year
   historical financials, formatted to standard IB conventions.
2. **Fixed input.** `input/financial_summary_spec.json` (and the natural-language
   version, `input/prompt.txt`) are the two inputs. Both contain identical data
   — one is structured JSON for the renderer path, one is natural language for
   the prompt-guided path.
3. **Fixed output target.** Single `.pptx` file with one slide, 13.33 × 7.5
   inches.
4. **Three runs.** Each track is run three times. The three output files per
   track are hashed after normalizing away volatile PPTX metadata (see
   `../tests/normalize.py`).
5. **Honest accounting of what the determinism test shows.** Running the same
   `.py` file three times is expected to be deterministic for both tracks.
   That test does not measure "would an LLM write the same code three times?"
   and `RESULTS.md` says so plainly.

## Layout

```
comparison/
├── README.md                              # this file
├── RESULTS.md                             # criteria table and findings
├── input/
│   ├── financial_summary_spec.json        # fixed input: JSON spec
│   └── prompt.txt                         # fixed input: natural-language prompt
├── track_a_renderer/
│   ├── build.py                           # loads spec, calls IBRenderer
│   ├── run1.pptx, run2.pptx, run3.pptx    # outputs
│   └── hashes.txt                         # normalized content hashes
├── track_b_prompt_guided/
│   ├── build.py                           # hand-written python-pptx
│   ├── run1.pptx, run2.pptx, run3.pptx    # outputs
│   └── hashes.txt                         # normalized content hashes
└── screenshots/
    ├── track_a_run1.png                   # Quick Look render of track_a run1
    └── track_b_run1.png                   # Quick Look render of track_b run1
```

## How to reproduce

```bash
# Track A
cd track_a_renderer
python3 build.py

# Track B
cd ../track_b_prompt_guided
python3 build.py
```

Each script writes `run1.pptx`, `run2.pptx`, `run3.pptx` into its own directory
and prints a summary to stdout.

To regenerate the screenshots (macOS only):

```bash
qlmanage -t -s 1600 -o /tmp/ql_a track_a_renderer/run1.pptx
qlmanage -t -s 1600 -o /tmp/ql_b track_b_prompt_guided/run1.pptx
cp /tmp/ql_a/run1.pptx.png screenshots/track_a_run1.png
cp /tmp/ql_b/run1.pptx.png screenshots/track_b_run1.png
```

## Headline finding

On this single slide, both tracks produce visually acceptable output. The
difference lives in the *code size* the LLM is responsible for:

- Track A: **0 lines** of spatial code. The LLM writes an 18-line JSON spec.
- Track B: **166 non-blank code lines**, including 32 `Inches()` calls, 12 `Pt()`
  calls, and 10 `RGBColor()` calls.

Both tracks produce deterministic output across 3 runs of the same file. That
test does not capture LLM generation variance, and the conclusion in
`RESULTS.md` is careful to say so.

See `RESULTS.md` for the full criteria table and the honest framing of what
this comparison does and does not establish.
