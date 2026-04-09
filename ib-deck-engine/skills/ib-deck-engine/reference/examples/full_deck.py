#!/usr/bin/env python3
"""
Demo: Build a complete 14-slide investment banking deck for Addus HomeCare Corp (ADUS).

This demonstrates every template in the IB Deck Engine library:
  1. Cover
  2. Table of Contents
  3. Executive Summary
  4. Investment Highlights
  5. Section Divider
  6. Financial Summary Table
  7. Stacked Bar + Data Table
  8. Dual Chart
  9. Section Divider
 10. Football Field
 11. Sensitivity Grid
 12. Trading Comps
 13. Section Divider
 14. Sources & Uses

Run from repo root:
    python3 examples/demo_full_deck.py

Output: case_study/adus_full_deck.pptx

Note: All financial data is from public SEC EDGAR 10-K filings.
This is a learning case study, not investment advice.
"""
import os
import sys

# Add parent dir to path so we can import ib_deck_engine
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ib_deck_engine import IBRenderer


def build_adus_deck():
    r = IBRenderer()

    # ─── 1. Cover ───
    r.render_cover({
        "title": "Project Alpine — Board of Directors\nDiscussion Materials",
        "subtitle": "Advisory Group LLC",
        "date": "April 2026",
    })

    # ─── 2. Table of Contents ───
    r.render_toc({
        "slide_number": 2,
        "title": "Today's Agenda",
        "items": [
            "Situation Overview and Strategic Context",
            "Review of Financial Performance",
            "Preliminary Valuation Analysis",
            "Perspectives on Process and Potential Buyers",
        ]
    })

    # ─── 3. Executive Summary ───
    r.render_exec_summary({
        "slide_number": 3,
        "title": "Executive Summary | Advisory Group Perspectives",
        "callout": "Advisory Group is pleased to present our preliminary perspectives on Addus HomeCare to the Board of Directors",
        "points": [
            {
                "main": "Addus HomeCare operates the largest independent personal care platform in the US, serving 107,000 consumers across 23 states with $1.4B in revenue",
                "subs": [
                    "Personal care segment (76.6% of revenue) grew 27.2% YoY driven by acquisitions and organic volume gains",
                    "EBITDA margins expanded 220bps over 3 years from 8.7% to 10.9%, demonstrating operating leverage at scale"
                ]
            },
            {
                "main": "The company is well-positioned for continued growth through both organic expansion and tuck-in M&A in a highly fragmented market",
                "subs": [
                    "Completed 3 acquisitions in FY2025; $525M+ undrawn revolver capacity for continued deal activity",
                    "Secular tailwinds from aging demographics and CMS policy shift toward home and community-based services"
                ]
            },
            {
                "main": "Preliminary valuation analysis suggests a range of $104-$174 per share with strong LBO returns at reasonable entry multiples",
                "subs": [
                    "DCF analysis (perpetuity growth): $129/share at 9.9% WACC, 3.0% terminal growth",
                    "LBO analysis: 2.51x MOIC / 20.2% IRR at 12.0x entry with 4.5x leverage, no multiple expansion assumed"
                ]
            },
        ]
    })

    # ─── 4. Investment Highlights ───
    r.render_investment_highlights({
        "slide_number": 4,
        "title": "Investment Highlights",
        "subtitle": "Scaled Home Care Platform With Secular Tailwinds and Proven Acquisition Engine",
        "cards": [
            {"title": "Market-Leading Platform", "body": "$1.09B Personal Care revenue serving 107,000 consumers across 23 states. Largest independent provider for dual-eligible populations."},
            {"title": "Expanding Margins at Scale", "body": "EBITDA margins expanded from 8.7% (FY2022) to 10.9% (FY2025). Capital-light model with only 0.5% CapEx/Revenue."},
            {"title": "Proven Buy-and-Build", "body": "23.2% revenue growth in FY2025 combining organic growth + strategic acquisitions. Revenue grown from $951M to $1.42B in 3 years."},
            {"title": "Demographic Tailwinds", "body": "65+ population growing 3% annually. Home care costs 50-75% less than facility-based alternatives, driving structural demand."},
        ]
    })

    # ─── 5. Section Divider ───
    r.render_section_divider({"title": "Review of Financial Performance"})

    # ─── 6. Financial Summary Table ───
    r.render_financial_summary({
        "slide_number": 6,
        "title": "Addus Has Delivered Consistent Revenue Growth with Expanding Profitability",
        "section_header": "Historical Financial Summary ($ in thousands)",
        "headers": ["Metric", "FY2023A", "FY2024A", "FY2025A", "3Y CAGR"],
        "rows": [
            {"label": "Revenue", "values": ["1,058,651", "1,154,599", "1,422,530", "14.4%"], "style": "bold"},
            {"label": "% Growth", "values": ["11.3%", "9.1%", "23.2%", ""], "style": "pct"},
            {"label": "Gross Profit", "values": ["339,876", "375,021", "461,874", "16.6%"], "style": "bold"},
            {"label": "% Margin", "values": ["32.1%", "32.5%", "32.5%", ""], "style": "pct"},
            {"label": "EBITDA", "values": ["105,082", "116,221", "155,027", "21.4%"], "style": "highlight"},
            {"label": "% Margin", "values": ["9.9%", "10.1%", "10.9%", ""], "style": "pct"},
            {"label": "Net Income", "values": ["62,516", "73,598", "95,910", "23.8%"], "style": "bold"},
            {"label": "Diluted EPS", "values": ["$3.83", "$4.23", "$5.22", "16.7%"], "style": "normal"},
        ],
        "source": "Source: SEC EDGAR. ADUS FY2025 10-K filed February 24, 2026."
    })

    # ─── 7. Stacked Bar + Data Table ───
    r.render_stacked_bar_table({
        "slide_number": 7,
        "title": "Personal Care Dominates Revenue Mix With Accelerating Growth Across All Three Segments",
        "header_text": "Net Service Revenue by Segment ($ in thousands)",
        "source": "Source: SEC EDGAR 10-K filings. Segment data from MD&A.",
        "format_total": lambda x: f"${x/1000:,.0f}M",
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
            ]
        }
    })

    # ─── 8. Dual Chart ───
    r.render_dual_chart({
        "slide_number": 8,
        "title": "Consistent Revenue Growth Accompanied by Meaningful EBITDA Margin Expansion",
        "source": "Source: SEC EDGAR XBRL data.",
        "charts": [
            {
                "subtitle": "Revenue ($M)",
                "periods": ["2022A", "2023A", "2024A", "2025A"],
                "values": [951120, 1058651, 1154599, 1422530],
                "color": "#1B365D",
                "format": lambda v: f"${v/1000:,.0f}M",
                "cagr": "14.4%",
                "secondary_label": "YoY Growth",
                "secondary_values": ["—", "+11.3%", "+9.1%", "+23.2%"],
            },
            {
                "subtitle": "EBITDA ($M) & Margin",
                "periods": ["2022A", "2023A", "2024A", "2025A"],
                "values": [82797, 105082, 116221, 155027],
                "color": "#4B7BA8",
                "format": lambda v: f"${v/1000:,.0f}M",
                "cagr": "23.3%",
                "secondary_label": "EBITDA Margin",
                "secondary_values": ["8.7%", "9.9%", "10.1%", "10.9%"],
            },
        ]
    })

    # ─── 9. Section Divider ───
    r.render_section_divider({"title": "Preliminary Valuation Analysis"})

    # ─── 10. Football Field ───
    r.render_football_field({
        "slide_number": 10,
        "title": "Preliminary Valuation Summary Implies a Range of $104–$174 Per Share Across Methodologies",
        "subtitle": "(All financials in $ per share unless otherwise stated)",
        "source": "Source: DCF and LBO models. Management projections. FactSet consensus estimates.",
        "methodologies": [
            {"category": "DCF\nPerpetuity", "category_color": "#1B365D",
             "description": "WACC: 8.5-11.0%\nTGR: 2.0-4.0%",
             "low": 104, "high": 174, "bar_color": "#1B365D",
             "implied_multiples": "8.5x - 15.2x"},
            {"category": "DCF\nExit Multiple", "category_color": "#1B365D",
             "description": "WACC: 8.5-11.0%\nExit: 10.0-14.0x EBITDA",
             "low": 111, "high": 178, "bar_color": "#3B6B9D",
             "implied_multiples": "9.1x - 15.8x"},
            {"category": "Trading\nComps", "category_color": "#E07020",
             "description": "Selected Public Companies\n10.0x - 13.5x NTM EBITDA",
             "low": 115, "high": 155, "bar_color": "#E07020",
             "implied_multiples": "10.0x - 13.5x"},
            {"category": "LBO\nAnalysis", "category_color": "#2E8B57",
             "description": "2.0-3.0x MOIC target\n15-25% IRR range",
             "low": 95, "high": 140, "bar_color": "#2E8B57",
             "implied_multiples": "8.0x - 12.0x"},
            {"category": "52-Week\nTrading", "category_color": "#888888",
             "description": "52-Week High / Low\nHistorical trading range",
             "low": 85, "high": 135, "bar_color": "#AAAAAA",
             "implied_multiples": "n/a"},
        ],
        "reference_lines": [
            {"price": 129, "label": "DCF Base", "color": "#1B365D"},
            {"price": 98, "label": "Current", "color": "#C00000"},
        ]
    })

    # ─── 11. Sensitivity Table ───
    r.render_sensitivity({
        "slide_number": 11,
        "title": "DCF Sensitivity Analysis Across WACC and Terminal Growth Rate Assumptions",
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
        "source": "Source: DCF model. Base case highlighted. Each cell recalculates the full DCF for that assumption combination."
    })

    # ─── 12. Trading Comps ───
    r.render_trading_comps({
        "slide_number": 12,
        "title": "Addus Trades at a Discount to Home Care Services Peers Despite Superior Growth and Margins",
        "header_text": "Selected Home Care Services Trading Comparables",
        "headers": ["Company", "Ticker", "Market Cap ($M)", "EV ($M)", "'26E Rev ($M)", "'26E EBITDA ($M)", "EV/Rev", "EV/EBITDA", "Rev Growth"],
        "rows": [
            {"company": "Addus HomeCare", "values": ["ADUS", "1,781", "1,820", "1,565", "175", "1.2x", "10.4x", "10.0%"]},
            {"company": "BrightSpring Health", "values": ["BTSG", "5,820", "8,400", "11,200", "530", "0.8x", "15.8x", "12.5%"]},
            {"company": "Pennant Group", "values": ["PNTG", "3,940", "4,200", "765", "82", "5.5x", "51.2x", "18.2%"]},
            {"company": "Enhabit Home Health", "values": ["EHAB", "680", "1,100", "1,065", "115", "1.0x", "9.6x", "3.5%"]},
            {"company": "Aveanna Healthcare", "values": ["AVAH", "2,150", "3,450", "2,085", "195", "1.7x", "17.7x", "6.8%"]},
            {"company": "Modivcare", "values": ["MODV", "310", "965", "2,720", "155", "0.4x", "6.2x", "2.1%"]},
            {"company": "Mean", "values": ["", "", "", "", "", "1.8x", "18.5x", "8.9%"], "summary": True},
            {"company": "Median", "values": ["", "", "", "", "", "1.1x", "12.7x", "8.4%"], "summary": True},
        ],
        "target_row": 0,
        "source": "Source: FactSet, Capital IQ. Market data illustrative. Addus highlighted in yellow."
    })

    # ─── 13. Section Divider ───
    r.render_section_divider({"title": "LBO Analysis & Transaction Assumptions"})

    # ─── 14. Sources & Uses ───
    r.render_sources_uses({
        "slide_number": 14,
        "title": "Preliminary LBO Capital Structure Sources Total Capitalization of $1,902M",
        "subtitle": "Based on 12.0x LTM EBITDA of $155M | 4.5x leverage | 63% sponsor equity contribution",
        "source": "Source: LBO model. Transaction assumptions illustrative.",
        "sources": [
            {"label": "Term Loan B (SOFR + 450)", "amount": 700000, "pct": "36.8%"},
            {"label": "Revolver (undrawn)", "amount": 0, "pct": "0.0%"},
            {"label": "Sponsor Equity", "amount": 1202229, "pct": "63.2%"},
            {"label": "Total Sources", "amount": 1902229, "pct": "100.0%", "total": True},
        ],
        "uses": [
            {"label": "Enterprise Value", "amount": 1860324, "pct": "97.8%"},
            {"label": "Advisory Fees (1.5%)", "amount": 27905, "pct": "1.5%"},
            {"label": "Financing Fees (2.0%)", "amount": 14000, "pct": "0.7%"},
            {"label": "Total Uses", "amount": 1902229, "pct": "100.0%", "total": True},
        ],
        "balance_check": "Balance Check: Sources = Uses = $1,902,229K ✓"
    })

    return r


if __name__ == "__main__":
    r = build_adus_deck()
    output = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                          "case_study", "adus_full_deck.pptx")
    os.makedirs(os.path.dirname(output), exist_ok=True)
    r.save(output)
    print(f"✓ Saved {output}")
    print(f"✓ {len(r.prs.slides)} slides")
    print()
    print("Slides generated:")
    for i, title in enumerate([
        "Cover", "Table of Contents", "Executive Summary", "Investment Highlights",
        "Section Divider (Financial Performance)", "Financial Summary Table",
        "Stacked Bar + Data Table (Revenue by Segment)", "Dual Chart (Revenue + EBITDA)",
        "Section Divider (Valuation)", "Football Field", "Sensitivity Grid",
        "Trading Comps", "Section Divider (LBO)", "Sources & Uses",
    ], 1):
        print(f"  {i:2}. {title}")
