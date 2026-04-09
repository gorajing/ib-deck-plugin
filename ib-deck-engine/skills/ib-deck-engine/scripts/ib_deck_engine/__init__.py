"""
IB Deck Engine — A template library for investment banking presentations.

The core idea: separate content reasoning (what should the slide say) from
spatial execution (where to put the pixels). The LLM (or human) writes a JSON
spec; the renderer handles every pixel by construction.

Quick start:

    from ib_deck_engine import IBRenderer

    r = IBRenderer()
    r.render_cover({
        "title": "Project Alpine — Discussion Materials",
        "subtitle": "Advisory Group LLC",
        "date": "April 2026",
    })
    r.save("output.pptx")

See README.md for the full template catalog.
"""

from .templates import IBRenderer, BankStyle, GS

__version__ = "0.1.0"
__all__ = ["IBRenderer", "BankStyle", "GS"]
