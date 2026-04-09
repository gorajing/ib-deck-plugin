#!/usr/bin/env python3
"""
Track A: Renderer-first architecture.

Input: the fixed JSON spec in ../input/financial_summary_spec.json
Output: one-slide PPTX produced by calling IBRenderer.render_financial_summary(spec).

The entire "code the LLM writes" is the JSON spec. No Inches(), no Pt(),
no RGBColor(), no python-pptx shape creation. The renderer handles every pixel.

Run:
    python3 build.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "ib-deck-engine", "skills", "ib-deck-engine", "scripts"))

from ib_deck_engine import IBRenderer

# Load the fixed input
with open(os.path.join(HERE, "..", "input", "financial_summary_spec.json")) as f:
    spec = json.load(f)

# Strip the _comment field (not part of the actual spec)
spec.pop("_comment", None)

# Render
r = IBRenderer()
r.render_financial_summary(spec)

# Save three runs to demonstrate determinism
for run_num in range(1, 4):
    output = os.path.join(HERE, f"run{run_num}.pptx")
    r2 = IBRenderer()
    r2.render_financial_summary(spec)
    r2.save(output)
    print(f"✓ Wrote {output}")

print("\nTrack A complete. 3 runs produced.")
print(f"Lines of 'spatial code' the LLM had to write: 0")
print(f"Lines in the JSON spec: {sum(1 for _ in json.dumps(spec, indent=2).split(chr(10)))}")
