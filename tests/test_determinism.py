"""
Determinism tests for the IB Deck Engine template library.

For each template, we render the same JSON spec twice and verify that the
normalized content hash is identical across both runs. This is the core
promise of the renderer-first architecture: same input, same output.

If any of these tests fail, the architecture's main claim is broken and
needs to be investigated immediately.

Run with:
    pytest tests/ -v
or:
    python -m pytest tests/ -v
"""
from __future__ import annotations

import io
import os
import sys

# Make the bundled plugin library importable
PLUGIN_SCRIPTS = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        "ib-deck-engine",
        "skills",
        "ib-deck-engine",
        "scripts",
    )
)
sys.path.insert(0, PLUGIN_SCRIPTS)

import pytest

from ib_deck_engine import IBRenderer  # noqa: E402

from tests.normalize import pptx_content_hash  # noqa: E402


def _render_to_bytes(render_fn_name: str, spec: dict) -> bytes:
    """Render a single slide using the named template and return the PPTX bytes."""
    r = IBRenderer()
    getattr(r, render_fn_name)(spec)
    buf = io.BytesIO()
    r.prs.save(buf)
    return buf.getvalue()


def _assert_deterministic(render_fn_name: str, spec: dict):
    """
    Render the same spec twice and assert the normalized content hashes match.
    """
    bytes_a = _render_to_bytes(render_fn_name, spec)
    bytes_b = _render_to_bytes(render_fn_name, spec)

    hash_a = pptx_content_hash(bytes_a)
    hash_b = pptx_content_hash(bytes_b)

    assert hash_a == hash_b, (
        f"{render_fn_name} produced different normalized content across two "
        f"runs with identical input. The architecture's core determinism "
        f"promise is broken.\n"
        f"  run 1: {hash_a}\n"
        f"  run 2: {hash_b}"
    )


# ---------- Fixtures ----------

@pytest.fixture
def cover_spec():
    return {
        "title": "Project Test — Discussion Materials",
        "subtitle": "Advisory Group LLC",
        "date": "April 2026",
    }


@pytest.fixture
def section_divider_spec():
    return {"title": "Review of Financial Performance"}


@pytest.fixture
def toc_spec():
    return {
        "slide_number": 2,
        "title": "Today's Agenda",
        "items": [
            "Situation Overview",
            "Financial Performance",
            "Valuation Analysis",
            "Process and Next Steps",
        ],
    }


@pytest.fixture
def exec_summary_spec():
    return {
        "slide_number": 3,
        "title": "Executive Summary",
        "callout": "Advisory Group is pleased to share our preliminary perspectives",
        "points": [
            {
                "main": "Company operates a scaled platform in an attractive market",
                "subs": [
                    "Leading market position with differentiated capabilities",
                    "Consistent growth and margin expansion",
                ],
            },
            {
                "main": "Strong financial profile with predictable cash flow",
                "subs": [
                    "14.4% revenue CAGR over the historical period",
                    "EBITDA margin expansion from 8.7% to 10.9%",
                ],
            },
        ],
    }


@pytest.fixture
def investment_highlights_spec():
    return {
        "slide_number": 4,
        "title": "Investment Highlights",
        "subtitle": "A scaled platform with secular tailwinds",
        "cards": [
            {"title": "Market Leader", "body": "Largest independent player in a fragmented market."},
            {"title": "Expanding Margins", "body": "220bps of margin expansion over 3 years."},
            {"title": "Proven M&A", "body": "Track record of disciplined acquisitions integrating cleanly."},
            {"title": "Demographic Tailwinds", "body": "Structural demand growth from an aging population."},
        ],
    }


@pytest.fixture
def financial_summary_spec():
    return {
        "slide_number": 6,
        "title": "Consistent Revenue Growth with Expanding Profitability",
        "section_header": "Historical Financial Summary ($ in thousands)",
        "headers": ["Metric", "FY2023A", "FY2024A", "FY2025A", "3Y CAGR"],
        "rows": [
            {"label": "Revenue", "values": ["1,058,651", "1,154,599", "1,422,530", "14.4%"], "style": "bold"},
            {"label": "% Growth", "values": ["11.3%", "9.1%", "23.2%", ""], "style": "pct"},
            {"label": "Gross Profit", "values": ["339,876", "375,021", "461,874", "16.6%"], "style": "bold"},
            {"label": "% Margin", "values": ["32.1%", "32.5%", "32.5%", ""], "style": "pct"},
            {"label": "EBITDA", "values": ["105,082", "116,221", "155,027", "21.4%"], "style": "highlight"},
            {"label": "% Margin", "values": ["9.9%", "10.1%", "10.9%", ""], "style": "pct"},
        ],
        "source": "Source: SEC EDGAR. FY2025 10-K.",
    }


@pytest.fixture
def stacked_bar_table_spec():
    return {
        "slide_number": 7,
        "title": "Revenue by Segment",
        "header_text": "Net Service Revenue by Segment ($000s)",
        "source": "Source: SEC EDGAR 10-K filings.",
        "data": {
            "periods": ["FY2022A", "FY2023A", "FY2024A", "FY2025A"],
            "segments": [
                {"name": "Personal Care", "color": "#1B365D", "values": [706507, 794718, 856581, 1089215]},
                {"name": "Hospice", "color": "#4B7BA8", "values": [201772, 207155, 228191, 262542]},
                {"name": "Home Health", "color": "#8EB4D6", "values": [42841, 56778, 69827, 70773]},
            ],
            "totals": [951120, 1058651, 1154599, 1422530],
            "table_rows": [
                {"label": "Personal Care", "values": ["$706,507", "$794,718", "$856,581", "$1,089,215"], "color": "#1B365D"},
                {"label": "Hospice", "values": ["$201,772", "$207,155", "$228,191", "$262,542"], "color": "#4B7BA8"},
                {"label": "Home Health", "values": ["$42,841", "$56,778", "$69,827", "$70,773"], "color": "#8EB4D6"},
                {"label": "Total", "values": ["$951,120", "$1,058,651", "$1,154,599", "$1,422,530"], "bold": True},
            ],
        },
    }


@pytest.fixture
def dual_chart_spec():
    return {
        "slide_number": 8,
        "title": "Revenue Growth and EBITDA Margin Expansion",
        "source": "Source: SEC EDGAR XBRL data.",
        "charts": [
            {
                "subtitle": "Revenue ($M)",
                "periods": ["2022A", "2023A", "2024A", "2025A"],
                "values": [951120, 1058651, 1154599, 1422530],
                "color": "#1B365D",
                "cagr": "14.4%",
                "secondary_label": "YoY Growth",
                "secondary_values": ["—", "+11.3%", "+9.1%", "+23.2%"],
            },
            {
                "subtitle": "EBITDA ($M) & Margin",
                "periods": ["2022A", "2023A", "2024A", "2025A"],
                "values": [82797, 105082, 116221, 155027],
                "color": "#4B7BA8",
                "cagr": "23.3%",
                "secondary_label": "EBITDA Margin",
                "secondary_values": ["8.7%", "9.9%", "10.1%", "10.9%"],
            },
        ],
    }


@pytest.fixture
def football_field_spec():
    return {
        "slide_number": 10,
        "title": "Preliminary Valuation Summary Implies $104-$174 Per Share",
        "subtitle": "(All financials in $ per share)",
        "source": "Source: DCF and LBO models.",
        "methodologies": [
            {
                "category": "DCF\nPerpetuity",
                "category_color": "#1B365D",
                "description": "WACC: 8.5-11.0%\nTGR: 2.0-4.0%",
                "low": 104,
                "high": 174,
                "bar_color": "#1B365D",
                "implied_multiples": "8.5x - 15.2x",
            },
            {
                "category": "LBO\nAnalysis",
                "category_color": "#2E8B57",
                "description": "2.0-3.0x MOIC target\n15-25% IRR range",
                "low": 95,
                "high": 140,
                "bar_color": "#2E8B57",
                "implied_multiples": "8.0x - 12.0x",
            },
        ],
        "reference_lines": [
            {"price": 129, "label": "DCF Base", "color": "#1B365D"},
            {"price": 98, "label": "Current", "color": "#C00000"},
        ],
    }


@pytest.fixture
def sensitivity_spec():
    return {
        "slide_number": 11,
        "title": "DCF Sensitivity — WACC vs Terminal Growth",
        "table_label": "Implied Share Price ($)",
        "row_axis_label": "WACC →",
        "col_axis_label": "Terminal Growth Rate →",
        "data": {
            "row_headers": ["8.5%", "9.0%", "9.5%", "9.9%", "10.5%", "11.0%"],
            "col_headers": ["2.0%", "2.5%", "3.0%", "3.5%", "4.0%"],
            "values": [
                ["$147", "$159", "$174", "$194", "$220"],
                ["$136", "$146", "$158", "$174", "$194"],
                ["$126", "$135", "$145", "$157", "$173"],
                ["$119", "$127", "$129", "$145", "$158"],
                ["$111", "$118", "$125", "$134", "$145"],
                ["$104", "$110", "$117", "$125", "$134"],
            ],
            "base_row": 3,
            "base_col": 2,
        },
        "source": "Source: DCF model.",
    }


@pytest.fixture
def sources_uses_spec():
    return {
        "slide_number": 14,
        "title": "LBO Capital Structure",
        "subtitle": "12.0x LTM EBITDA | 4.5x leverage",
        "source": "Source: LBO model.",
        "sources": [
            {"label": "Term Loan B", "amount": 700000, "pct": "36.8%"},
            {"label": "Sponsor Equity", "amount": 1202229, "pct": "63.2%"},
            {"label": "Total Sources", "amount": 1902229, "pct": "100.0%", "total": True},
        ],
        "uses": [
            {"label": "Enterprise Value", "amount": 1860324, "pct": "97.8%"},
            {"label": "Advisory Fees", "amount": 27905, "pct": "1.5%"},
            {"label": "Financing Fees", "amount": 14000, "pct": "0.7%"},
            {"label": "Total Uses", "amount": 1902229, "pct": "100.0%", "total": True},
        ],
        "balance_check": "Balance Check: Sources = Uses ✓",
    }


@pytest.fixture
def trading_comps_spec():
    return {
        "slide_number": 12,
        "title": "Peer Trading Comparables",
        "header_text": "Selected Public Companies",
        "headers": ["Company", "Ticker", "EV/Rev", "EV/EBITDA", "Growth"],
        "rows": [
            {"company": "Company A", "values": ["ADUS", "1.2x", "10.4x", "10.0%"]},
            {"company": "Company B", "values": ["BTSG", "0.8x", "15.8x", "12.5%"]},
            {"company": "Company C", "values": ["PNTG", "5.5x", "51.2x", "18.2%"]},
            {"company": "Mean", "values": ["", "2.5x", "25.8x", "13.6%"], "summary": True},
            {"company": "Median", "values": ["", "1.2x", "15.8x", "12.5%"], "summary": True},
        ],
        "target_row": 0,
        "source": "Source: FactSet. Illustrative numbers.",
    }


# ---------- Per-template determinism tests ----------

def test_cover_deterministic(cover_spec):
    _assert_deterministic("render_cover", cover_spec)


def test_section_divider_deterministic(section_divider_spec):
    _assert_deterministic("render_section_divider", section_divider_spec)


def test_toc_deterministic(toc_spec):
    _assert_deterministic("render_toc", toc_spec)


def test_exec_summary_deterministic(exec_summary_spec):
    _assert_deterministic("render_exec_summary", exec_summary_spec)


def test_investment_highlights_deterministic(investment_highlights_spec):
    _assert_deterministic("render_investment_highlights", investment_highlights_spec)


def test_financial_summary_deterministic(financial_summary_spec):
    _assert_deterministic("render_financial_summary", financial_summary_spec)


def test_stacked_bar_table_deterministic(stacked_bar_table_spec):
    _assert_deterministic("render_stacked_bar_table", stacked_bar_table_spec)


def test_dual_chart_deterministic(dual_chart_spec):
    _assert_deterministic("render_dual_chart", dual_chart_spec)


def test_football_field_deterministic(football_field_spec):
    _assert_deterministic("render_football_field", football_field_spec)


def test_sensitivity_deterministic(sensitivity_spec):
    _assert_deterministic("render_sensitivity", sensitivity_spec)


def test_sources_uses_deterministic(sources_uses_spec):
    _assert_deterministic("render_sources_uses", sources_uses_spec)


def test_trading_comps_deterministic(trading_comps_spec):
    _assert_deterministic("render_trading_comps", trading_comps_spec)


# ---------- Cross-run stability test ----------

def test_ten_runs_of_financial_summary_produce_one_hash(financial_summary_spec):
    """
    The strongest determinism claim: render the same spec 10 times, verify all
    10 outputs hash to the same value. This is the fixture the architectural
    argument rests on — 'fixed input, repeated renders, identical output.'
    """
    hashes = set()
    for _ in range(10):
        hashes.add(pptx_content_hash(_render_to_bytes("render_financial_summary", financial_summary_spec)))

    assert len(hashes) == 1, (
        f"Expected 10 runs to produce 1 unique content hash, got {len(hashes)}: {hashes}"
    )
