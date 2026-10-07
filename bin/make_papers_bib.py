"""Build al-folio's papers.bib from the CV's Zotero export plus site-only fields.

Usage (from the repo root): python3 bin/make_papers_bib.py [zotero.bib] [papers.bib]
Defaults to ../cv/zotero.bib and _bibliography/papers.bib. Edit EXTRAS to add
badges, code links, awards, or "selected" papers for the homepage.
"""
import re, sys

EXTRAS = {
    "benderDontMeltYour2025": {"abbr": "SPAA", "selected": "true",
        "award_name": "Distinguished Paper", "award": "SPAA 2025 Distinguished Paper Award.",
        "slides": "slides/halg2026-heat-sink.pdf"},
    "demanFastCompactSketchBased2025": {"abbr": "arXiv",
        "arxiv": "2509.14433", "code": "https://github.com/etwest/DynamicQueriesCC"},
    "jonesBehavioralSegmentationClustering2025": {"abbr": "ITSC"},
    "tenchExploringLandscapeDistributed2025": {"abbr": "ALENEX", "arxiv": "2410.07518",
        "code": "https://github.com/GraphStreamingProject/Landscape"},
    "tenchGraphZeppelinHowFind2024": {"abbr": "TODS", "selected": "true",
        "code": "https://github.com/GraphStreamingProject/GraphZeppelin"},
    "benderIncrementFreezeEvery2023": {"abbr": "SPAA", "selected": "true",
        "code": "https://github.com/etwest/Increment-and-Freeze"},
    "delayoAutomaticHBMManagement2022": {"abbr": "SPAA",
        "slides": "https://docs.google.com/presentation/d/13cxfHbzg0HHaRo7hWR1G9VYn_elzn4y15NdDL3_pu1w/edit?usp=sharing"},
    "vorobyevaUsingAdvancedData2022": {"abbr": "Cluster"},
}
# Joint first authors: al-folio renders a trailing * on a last name as a superscript
EQUAL = {
    "delayoAutomaticHBMManagement2022": ["DeLayo, Daniel", "Zhang, Kenny"],
    "vorobyevaUsingAdvancedData2022": ["Vorobyeva, Janet", "DeLayo, Daniel"],
}
EQUAL_NOTE = "* Joint first authors."
DROP = ("file", "urldate", "copyright", "keywords")

src = sys.argv[1] if len(sys.argv) > 1 else "../cv/zotero.bib"
dst = sys.argv[2] if len(sys.argv) > 2 else "_bibliography/papers.bib"
text = open(src, encoding="utf-8").read()
# HTML tags that Crossref leaves in abstracts
text = text.replace("{$<$}p{$>$}", "").replace("{$<$}/p{$>$}", "")
# Zotero escapes math in abstracts as literal text; restore it for MathJax
text = text.replace("\\$", "$").replace("\\textbackslash ", "\\").replace("\\textasciicircum ", "^")
SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
# Better BibTeX exports Unicode symbols as LaTeX; turn the ones in abstracts back
text = text.replace("\\texttimes{}", "×").replace("\\texttimes", "×").replace("\\textohm ", "Ω")
text = re.sub(r"\{\$\^\{?(\d+)\}?\$\}", lambda d: d.group(1).translate(SUP), text)
def plain_math(m):
    # jekyll-scholar's latex filter eats $...$, so render abstract math as Unicode text
    s = m.group(1).replace("\\log", "log ").replace("  ", " ")
    s = re.sub(r"\^(\d+)", lambda d: d.group(1).translate(SUP), s)
    s = re.sub(r" +", " ", s).replace("log /", "log/").replace("( ", "(")
    return re.sub(r"log ([⁰¹²³⁴⁵⁶⁷⁸⁹]+)", r"log\1", s).strip()
def fix_abstract(m):
    return m.group(1) + re.sub(r"\$([^$]*)\$", plain_math, m.group(2)) + m.group(3)
text = re.sub(r"(abstract = \{)(.*?)(\},?\n)", fix_abstract, text, flags=re.S)
out = []
for entry in re.split(r"\n(?=@)", text.strip()):
    key = re.match(r"@\w+\{([^,]+),", entry).group(1)
    lines = [l for l in entry.rstrip().rstrip("}").rstrip().split("\n")
             if not re.match(r"\s*(%s)\s*=" % "|".join(DROP), l)]
    for name in EQUAL.get(key, []):
        last, first = name.split(", ")
        i = next(i for i, l in enumerate(lines) if re.match(r"\s*author\s*=", l))
        assert name in lines[i], f"{name} not in {key} authors"
        lines[i] = lines[i].replace(name, f"{last}*, {first}")
    if key in EQUAL:
        lines[-1] = lines[-1].rstrip(",") + ","
        lines.append(f"  annotation = {{{EQUAL_NOTE}}},")
    lines[-1] = lines[-1].rstrip(",") + ","
    for k, v in EXTRAS.get(key, {}).items():
        lines.append(f"  {k} = {{{v}}},")
    lines[-1] = lines[-1].rstrip(",")
    out.append("\n".join(lines) + "\n}")
    EXTRAS.pop(key, None)
if EXTRAS:
    sys.exit(f"keys not found in export: {sorted(EXTRAS)}")
open(dst, "w", encoding="utf-8").write("---\n---\n\n" + "\n\n".join(out) + "\n")
