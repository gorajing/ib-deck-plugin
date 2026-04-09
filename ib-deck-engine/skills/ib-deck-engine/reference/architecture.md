# Architecture

The IB Deck Engine uses a renderer-first architecture: the LLM fills structured
JSON specs, and a deterministic Python renderer handles all spatial execution.

## Two layers

```
Layer 1: CONTENT REASONING (LLM)
  - Pick the right template for the slide type
  - Write the action title
  - Select the data values
  - Cite the source
    │
    │  output: structured JSON spec
    ▼
Layer 2: DETERMINISTIC RENDERER (Python function)
  - Compute column widths from content
  - Apply right-alignment to numeric columns
  - Compute proportional bar heights from values
  - Apply row styles (bold, italic, highlight)
  - Position source text dynamically
  - Handle collision detection on reference labels
    │
    │  output: .pptx file
    ▼
Layer 3: python-pptx (emits OOXML)
```

The LLM operates entirely in Layer 1. It never touches `Inches()`, `Pt()`,
`RGBColor()`, EMU values, or any python-pptx shape-creation code. Those live
in the renderer functions and are enforced by code at render time.

## What this buys you

**Repeatability.** Same input → same output. If you call
`render_financial_summary(spec)` twice with the same spec, the slide XML
output is identical in the parts that matter (text, positions, styles). The
only non-deterministic parts are zip metadata (creation timestamps) which
shouldn't affect content.

**Evaluability.** "Did the LLM pick the right template and fill the right data?"
is a simpler test than "did the LLM write correct python-pptx code?" The
evaluation surface shrinks from "any possible code the LLM could emit" to
"a fixed JSON schema with a fixed set of valid values."

**Maintainability.** Adding a new template is writing a Python function.
Functions can be reviewed, versioned, tested, and changed without touching
prompts. Fixing a layout bug is a one-line code change, not a prompt-tuning
exercise.

**Lower failure surface.** Every pixel decision the LLM doesn't make is a
pixel decision that can't be wrong.

## Contrast with prompt-guided spatial code

An alternative architecture — used by `anthropics/financial-services-plugins`
at the time of writing — is to have the LLM write spatial code directly.
That architecture's skill files include instructions like:

- "Make sure to right-align numeric columns"
- "Bar heights should be proportional to data"
- "Tables must be real table objects, not text with tabs"
- "Use the 4-color font convention (blue/black/purple/green)"

These are guidance, not guarantees. The LLM may follow them correctly on one
generation and not on the next. Quality is achieved through prompt engineering
and post-hoc checking.

The renderer-first architecture moves these rules from guidance to construction.
The LLM doesn't need to remember to right-align because the function always
right-aligns. The LLM can't produce disproportional bars because bar heights
are computed by the function, not by the LLM.

Both architectures have merits. Prompt-guided is more flexible — the LLM can
generate any layout the prompt can describe. Renderer-first is more reliable
within the template library's scope but can't produce layouts outside it.

For investment banking, where slide patterns are highly standardized (~25-30
recurring layouts across a book), the reliability benefit of renderer-first
outweighs the flexibility benefit of prompt-guided. That's the bet this plugin
is making.

## Comparable patterns

The renderer-first architecture isn't novel. It's used by:

- **Beautiful.ai** — web-based design engine; AI picks a layout, engine renders
- **Gamma.app** — component-based slide generation with layout algorithms
- **Pitch** — component library with slot-based content filling
- **UpSlide** — native PowerPoint templates with data linking
- **Macabacus** — Excel-to-PowerPoint linking with pre-defined templates

What's different in the Claude plugin context: the "LLM fills a JSON spec"
pattern extends these tools' architecture to the conversational surface.
Instead of a designer clicking a layout in a UI, the LLM picks it by name and
fills a structured spec from the user's intent.

## Why not Office JS / in-PowerPoint rendering?

This version uses `python-pptx` and produces `.pptx` files from outside
PowerPoint. It does not run inside the Office add-in.

An Office JS port of the same template functions would enable in-PowerPoint
rendering (so `r.render_financial_summary(spec)` would draw directly onto an
active slide via the Office JS API instead of writing to a file). That port
is not part of v0.1.0 but is architecturally feasible — the renderer functions
would translate from `python-pptx` calls to Office JS `shape.addShape` /
`shape.addTextBox` calls, keeping the JSON spec API identical.

## Trade-offs and limitations

**Scope.** Renderer-first only works for patterns in the library. Novel slide
layouts require writing a new template function. If a user wants something
unique that doesn't fit any existing template, this architecture can't help.

**Flexibility.** Small visual tweaks (e.g., "make this specific row 2pt bigger")
require either a template parameter or a template fork. Prompt-guided
architectures can handle one-off tweaks more easily because the LLM is already
writing the code.

**Determinism vs. creativity.** The renderer is deterministic by design. If you
want the LLM to creatively reinterpret a slide differently each time, this
architecture is the wrong choice. For IB decks, that's a feature, not a bug.

## Future directions

- Chart rendering using `matplotlib` or native `python-pptx` charts (currently
  charts are rectangles computed directly)
- Pluggable style system (bank-specific presets)
- MCP server wrapper so the renderer works from any MCP client
- Normalized snapshot testing for every template
