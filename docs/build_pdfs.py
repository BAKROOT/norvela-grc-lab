#!/usr/bin/env python3
"""Build the print editions of the Norvela GRC Lab from the Markdown sources.

Produces, next to this script:
  Norvela-GRC-Lab-Manual.pdf        the whole lab, minus the findings key
  Norvela-GRC-Lab-Findings-Key.pdf  the sealed findings key, separately

Usage:  pip install markdown weasyprint
        python3 docs/build_pdfs.py

The Markdown files are the source of truth. Edit them, then rebuild.
"""
from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
from weasyprint import HTML

DOCS = Path(__file__).resolve().parent
ROOT = DOCS.parent

TITLE = "The Norvela GRC Lab"
AUTHOR = "Bilal Ahmad Kamal"
VERIFIED = "September 2026"
REPO = "github.com/BAKROOT/norvela-grc-lab"

FICTION = (
    "Norvela Pay, its people, its vendors, its licence number, its incident "
    "and its supervisory correspondence are entirely fictional. Real tools "
    "and real regulations are named accurately; the company they are applied "
    "to is not real. Regulatory dates were current as of September 2026. "
    "Verify before citing."
)

# (number, title, subtitle, source)  source = path or "readme"
MANUAL = [
    ("01", "Overview", "What the lab is and why it is shaped this way", "readme"),
    ("02", "The Programme", "Eight phases, twelve weeks, with deliverables and proof gates",
     "CURRICULUM.md"),
    ("03", "Company Dossier: Norvela Pay",
     "Your assessment target: governance, estate, data, third parties",
     "01-scenario/00-COMPANY-DOSSIER.md"),
    ("04", "Incident Pack NOR-2026-0908", "A live incident with ten timed decision points",
     "01-scenario/10-INCIDENT.md"),
    ("05", "Lab Setup", "Building the environment in six parts, about three hours",
     "02-stack/SETUP.md"),
    ("06", "Scenario Evidence", "Artefacts the dossier and incident pack refer to",
     ["04-evidence/secret-scan-2025.md", "04-evidence/cto-slack-excerpt.md"]),
    ("07", "Interview Question Bank",
     "120 questions across six categories, with what a strong answer contains",
     "05-interview/QUESTION-BANK.md"),
    ("08", "Timed Case Studies", "Six cases in the formats real GRC interviews use",
     "05-interview/CASE-STUDIES.md"),
]

CSS = """
@page {
  size: A4; margin: 22mm 20mm 20mm 20mm;
  @bottom-left  { content: string(doctitle); font: 7.5pt Inter, sans-serif; color: #8A979E; }
  @bottom-right { content: counter(page) " / " counter(pages); font: 7.5pt Inter, sans-serif; color: #8A979E; }
}
@page cover { @bottom-left { content: none; } @bottom-right { content: none; } }
html { font: 9.6pt/1.5 "DejaVu Serif", Georgia, serif; color: #131B21; }
body { string-set: doctitle "The Norvela GRC Lab"; }
h1, h2, h3, h4 { font-family: Inter, "DejaVu Sans", sans-serif; color: #0E3B3A;
                 line-height: 1.2; page-break-after: avoid; }
h1 { font-size: 20pt; font-weight: 700; border-bottom: 2px solid #0E3B3A;
     padding-bottom: 5pt; margin: 0 0 12pt; string-set: doctitle content(); }
h2 { font-size: 12.5pt; margin: 18pt 0 6pt; padding-top: 8pt; border-top: 1px solid #D2DADE; }
h3 { font-size: 10.5pt; margin: 12pt 0 4pt; }
p, li { orphans: 3; widows: 3; }
a { color: #0E5A57; text-decoration: none; }
code { font: 8pt "DejaVu Sans Mono", monospace; background: #EDF2F2;
       padding: 0.5pt 2.5pt; border-radius: 2pt; }
pre { background: #F3F6F6; border-left: 3px solid #0E5A57; padding: 7pt 9pt;
      font-size: 7.6pt; line-height: 1.4; white-space: pre-wrap; page-break-inside: avoid; }
pre code { background: none; padding: 0; font-size: 7.6pt; }
table { border-collapse: collapse; width: 100%; margin: 8pt 0; font: 8pt/1.4 Inter, sans-serif;
        page-break-inside: auto; }
th { text-align: left; background: #0E3B3A; color: #fff; font-weight: 600; padding: 4pt 5pt; }
td { border-bottom: 1px solid #D2DADE; padding: 4pt 5pt; vertical-align: top; }
tr { page-break-inside: avoid; }
blockquote { margin: 8pt 0; padding: 6pt 10pt; background: #F4EFE8;
             border-left: 3px solid #A9571A; color: #3A3A3A; }
hr { display: none; }  /* h2 already carries a rule */
.section { page-break-before: always; }
.cover { page: cover; }
.cover .kicker { font: 600 8pt Inter, sans-serif; letter-spacing: 0.25em; color: #5C6B73;
                 margin-top: 70mm; }
.cover .t { font: 700 30pt Inter, sans-serif; color: #0E3B3A; margin: 6pt 0 8pt;
            border: 0; padding: 0; }
.cover .rule { width: 42mm; border-top: 3px solid #0E3B3A; margin-bottom: 14pt; }
.cover .lede { font-size: 12pt; max-width: 125mm; color: #2A363D; }
.cover table { width: auto; margin-top: 16pt; font-size: 8pt; }
.cover td { border: 0; padding: 2.5pt 18pt 2.5pt 0; }
.cover td:first-child { color: #8A979E; letter-spacing: 0.12em; font-size: 7pt; }
.cover .fine { margin-top: 55mm; font: 7.2pt/1.5 Inter, sans-serif;
               color: #5C6B73; border-top: 1px solid #D2DADE; padding-top: 6pt; max-width: 120mm; }
.cover .warn { margin-top: 18pt; padding: 8pt 10pt; border-left: 3px solid #A9571A;
               background: #F4EFE8; font-size: 9pt; max-width: 125mm; }
.toc h1 { border: 0; }
.toc .row { display: flex; padding: 6pt 0; border-bottom: 1px solid #D2DADE; }
.toc .n { width: 14mm; font: 700 9pt Inter, sans-serif; color: #A9571A; }
.toc .tt { font: 600 10pt Inter, sans-serif; color: #131B21; }
.toc .st { font: 8pt Inter, sans-serif; color: #5C6B73; }
.subsep { margin-top: 22pt; }
ol.num { list-style: none; padding-left: 0; }
ol.num > li { counter-increment: item; padding-left: 9mm; position: relative; }
ol.num > li::before { content: counter(item) "."; position: absolute; left: 0;
                      font: 600 8.6pt Inter, sans-serif; color: #A9571A; }
"""

MD_EXT = ["tables", "fenced_code", "sane_lists", "attr_list"]


def md_to_html(text: str) -> str:
    """Markdown -> HTML, keeping list numbering that runs across headings.

    The question bank numbers 1-120 and the findings key 1-46 across many
    separate lists. Python-Markdown records each list's first number in a
    start attribute, but WeasyPrint ignores start, so we number top-level
    ordered lists with a CSS counter seeded from it (see ol.num in CSS).
    """
    out = markdown.markdown(text, extensions=MD_EXT)

    def fix(m):
        if _depth(out, m.start()) > 0:
            return m.group(0)          # nested list: leave alone
        n = int(m.group(1) or 1)
        return f'<ol class="num" style="counter-reset: item {n - 1}">'

    return re.sub(r'<ol(?: start="(\d+)")?>', fix, out)


def _depth(s: str, pos: int) -> int:
    """How many <ol>/<ul> are open at pos (0 = top level)."""
    head = s[:pos]
    return (head.count("<ol") + head.count("<ul")
            - head.count("</ol>") - head.count("</ul>"))


def strip_h1(text: str) -> str:
    """Drop the file's own H1; the manual supplies section titles."""
    return re.sub(r"\A\s*# .*\n", "", text, count=1)


def readme_manual_blocks() -> str:
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    blocks = re.findall(r"<!-- manual:start -->(.*?)<!-- manual:end -->", readme, re.S)
    titles = ["", "## Why it's built this way", "## Regulatory currency"]
    parts = []
    for i, b in enumerate(blocks):
        heading = titles[i] if i < len(titles) else ""
        parts.append(f"{heading}\n\n{b.strip()}")
    start = (
        "## Start here\n\n"
        "1. `02-stack/SETUP.md`: build the lab. One evening.\n"
        "2. `01-scenario/00-COMPANY-DOSSIER.md`: read up on the company you are assessing.\n"
        "3. `CURRICULUM.md`: the phases. Work them in order.\n\n"
        "Do not open the Findings Key (a separate document) until Phase 3 is complete.\n\n"
        "## Fiction notice\n\n" + FICTION
    )
    return "\n\n".join(parts[:1] + [start] + parts[1:])


def section_html(num, title, source) -> str:
    if source == "readme":
        body = md_to_html(readme_manual_blocks())
    elif isinstance(source, list):
        chunks = []
        for i, s in enumerate(source):
            text = (ROOT / s).read_text(encoding="utf-8")
            sub = re.match(r"\s*# (.*)\n", text)
            head = f"<h2{' class=subsep' if i else ''}>{html.escape(sub.group(1))}</h2>" if sub else ""
            chunks.append(head + md_to_html(strip_h1(text)))
        body = "".join(chunks)
    else:
        body = md_to_html(strip_h1((ROOT / source).read_text(encoding="utf-8")))
    return f'<section class="section"><h1>{html.escape(title)}</h1>{body}</section>'


def cover(title, lede, rows, warn=None) -> str:
    trs = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in rows)
    w = f'<div class="warn">{warn}</div>' if warn else ""
    return (f'<div class="cover"><div class="kicker">GOVERNANCE · RISK · COMPLIANCE</div>'
            f'<div class="t">{title}</div><div class="rule"></div>'
            f'<div class="lede">{lede}</div><table>{trs}</table>{w}'
            f'<div class="fine">{FICTION}</div></div>')


def build_manual() -> Path:
    toc = "".join(
        f'<div class="row"><div class="n">{n}</div><div><div class="tt">{t}</div>'
        f'<div class="st">{st}</div></div></div>' for n, t, st, _ in MANUAL)
    toc += ('<div class="row"><div class="n">—</div><div><div class="tt">Findings Key</div>'
            '<div class="st">Supplied as a separate sealed document. Do not open until Phase 3.'
            '</div></div></div>')
    doc = (
        cover(TITLE,
              "A complete, self-hosted environment for learning governance, risk and "
              "compliance by assessing one fictional EU payment institution end to end.",
              [("PROGRAMME", "12 weeks · 8 phases (P0–P7) · ~8 h/week"),
               ("SUBJECT", "Norvela Pay, S.A. (Lisboa)"),
               ("SCOPE", "DORA · NIS2/RJC · GDPR · PCI DSS · ISO 27001 · SOC 2 · EU AI Act"),
               ("AUTHOR", AUTHOR),
               ("SOURCE", REPO),
               ("VERIFIED", VERIFIED)])
        + f'<section class="section toc"><h1>Contents</h1>{toc}</section>'
        + "".join(section_html(n, t, s) for n, t, _, s in MANUAL)
    )
    out = DOCS / "Norvela-GRC-Lab-Manual.pdf"
    HTML(string=f"<html><head><meta charset='utf-8'><title>{TITLE}: Manual</title>"
                f"<meta name='author' content='{AUTHOR}'><style>{CSS}</style></head>"
                f"<body>{doc}</body></html>", base_url=str(ROOT)).write_pdf(out)
    return out


def build_key() -> Path:
    text = (ROOT / "01-scenario/99-FINDINGS-KEY.md").read_text(encoding="utf-8")
    text = text.replace("<br>", "")
    doc = (
        cover("Findings Key",
              "The 46 planted findings in the Norvela Pay estate, with the framework "
              "and regulatory linkage for each.",
              [("COMPANION TO", "The Norvela GRC Lab Manual"),
               ("OPEN AFTER", "Phase 3 (control assessment)"),
               ("FINDINGS", "46, across seven domains"),
               ("AUTHOR", AUTHOR)],
              warn="<b>Sealed supplement.</b> The lab is only worth doing if you find "
                   "these yourself. Do not read this until you have completed your own "
                   "assessment through Phase 3.")
        + f'<section class="section"><h1>Findings Key</h1>{md_to_html(strip_h1(text))}</section>'
    )
    out = DOCS / "Norvela-GRC-Lab-Findings-Key.pdf"
    HTML(string=f"<html><head><meta charset='utf-8'><title>{TITLE}: Findings Key</title>"
                f"<meta name='author' content='{AUTHOR}'><style>{CSS}</style></head>"
                f"<body>{doc}</body></html>", base_url=str(ROOT)).write_pdf(out)
    return out


if __name__ == "__main__":
    for p in (build_manual(), build_key()):
        print(f"  {p.relative_to(ROOT)}  {p.stat().st_size:,} bytes")
