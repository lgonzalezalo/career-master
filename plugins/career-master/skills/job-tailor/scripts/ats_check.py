#!/usr/bin/env python3
"""ats_check.py - objective checks on the FINAL PDF (an approximation of an ATS, not a real one).

Usage:
  python3 ats_check.py <cv.pdf> [--keywords <keywords.txt>] [--pages N]

keywords.txt: one term per line; synonyms separated by |  (e.g. follow-up|seguimiento);
a leading ! marks a known gap that must NOT be added (WARN if it appears); lines with # are comments.
Terms match as whole words (plural -s/-es allowed) and across line breaks.
Needs the poppler tools: pdftotext, pdfinfo, pdffonts, pdfimages.
Exit code 1 only if an ERROR is found."""
import argparse
import os
import re
import subprocess
import sys


def run(cmd):
    try:
        return subprocess.run(cmd, capture_output=True, text=True).stdout
    except FileNotFoundError:
        sys.exit(f"Missing tool: {cmd[0]} (install poppler-utils)")


ap = argparse.ArgumentParser()
ap.add_argument("pdf")
ap.add_argument("--keywords")
ap.add_argument("--pages", type=int)
a = ap.parse_args()
if not os.path.isfile(a.pdf):
    sys.exit(f"PDF not found: {a.pdf}")
res = []


def add(level, msg):
    res.append((level, msg))


text = run(["pdftotext", a.pdf, "-"])  # simple reading order, like a basic parser
lines = [l.strip() for l in text.splitlines() if l.strip()]
flat = re.sub(r"\s+", " ", text.lower())  # one line, so multi-word terms survive line breaks

# 1. Extraction and pages
m = re.search(r"Pages:\s+(\d+)", run(["pdfinfo", a.pdf]))
n = int(m.group(1)) if m else -1
if a.pages:
    add("OK" if n == a.pages else "WARN", f"Pages: {n} (target {a.pages})")
else:
    add("INFO", f"Pages: {n}")
add("OK" if len(text) > 800 else "ERROR", f"Extractable text: {len(text)} characters")

# 2. Fonts and images (text drawn as an image is unreadable for an ATS)
fonts = [l.split() for l in run(["pdffonts", a.pdf]).splitlines()[2:] if l.strip()]
noemb = [f[0] for f in fonts if len(f) > 4 and f[-5] == "no"]
add("OK" if not noemb else "WARN", "Fonts embedded" if not noemb else f"Fonts not embedded: {noemb}")
imgs = len([l for l in run(["pdfimages", "-list", a.pdf]).splitlines()[2:] if l.strip()])
add("OK" if imgs == 0 else "WARN", f"Embedded images: {imgs} (cannot verify whether they hold text)")

# 3. Contact data
add("OK" if re.search(r"\S+@\S+\.\S+", text) else "ERROR", "Contact: email")
# a phone has 9+ digits; a date range such as "2015 - 2020" is not one
MONTH = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sept?|oct|nov|dec|ene|abr|ago|dic)[a-zé]*\.?"
POINT = rf"(?:\d{{2}}/\d{{4}}|{MONTH}\s+(?:de\s+)?\d{{4}}|(?:19|20)\d{{2}})"
date_rx = rf"\b{POINT}\s*[–—-]\s*(?:{POINT}|present|current|actual|actualidad|presente|hoy)\b"
phones = re.findall(r"\+?\d[\d ()\-.]{7,}\d", re.sub(date_rx, " ", text, flags=re.I))
add("OK" if any(sum(c.isdigit() for c in ph) >= 9 for ph in phones) else "WARN", "Contact: phone")

# 4. Expected sections (English or Spanish headings)
heads = "\n".join(l.lower() for l in lines)
for name, rx in [("profile/summary", r"^(profile|summary|perfil|resumen)"),
                 ("experience", r"^(experience|work experience|experiencia)"),
                 ("education", r"^(education|formaci[oó]n|educaci[oó]n)")]:
    add("OK" if re.search(rx, heads, re.M) else "WARN", f"Section: {name}")

# 5. Dates: consistent format and next to their role line
# (date_rx is defined above: 03/2021 – 10/2026, Feb 2022 – Sep 2026, febrero de 2022 – actualidad, 2011 – 2020)
for i, l in enumerate(lines):
    if re.fullmatch(date_rx, l, re.I):
        prev = lines[i - 1] if i else ""
        ok = bool(re.search(r"\s[—–|-]\s", prev))
        add("OK" if ok else "WARN",
            f"Date '{l}' follows a role line" if ok else f"Date '{l}' does not follow a role line (association risk)")
kinds = {"mm/yyyy" if "/" in d else "month yyyy" if d[0].isalpha() else "yyyy" for d in re.findall(date_rx, text, re.I)}
if len(kinds) <= 1:
    add("OK", "Date format consistent")
elif len(kinds - {"yyyy"}) == 1:
    add("INFO", f"Dates as '{(kinds - {'yyyy'}).pop()}' and also year-only (check it is intended)")
else:
    add("WARN", f"Mixed date formats: {sorted(kinds)}")

# 6. Keywords approved by the user (never suggest stuffing)
if a.keywords:
    for raw in open(a.keywords, encoding="utf-8"):
        raw = raw.strip()
        if not raw or raw.startswith("#"):
            continue
        gap = raw.startswith("!")
        terms = [t.strip() for t in raw.lstrip("!").split("|") if t.strip()]
        if not terms:
            continue
        cnt = sum(len(re.findall(r"(?<!\w)" + r"\s+".join(map(re.escape, t.lower().split())) + r"(?:e?s)?(?!\w)", flat))
                  for t in terms)
        if gap and cnt:
            add("WARN", f"Known gap present {cnt}x: {terms[0]} -> check it is not claimed as own experience")
        elif gap:
            add("INFO", f"Known gap, do not add: {terms[0]} (absent, correct)")
        elif cnt == 0:
            add("MISSING", f"No coverage: {terms[0]} -> add only if already evidenced in the master (pending confirmation)")
        elif cnt > 15:
            add("WARN", f"Term repeated {cnt}x: {terms[0]} (possible excess)")
        else:
            add("OK", f"Term covered ({cnt}x): {terms[0]}")

for level, msg in res:
    print(f"[{level:7}] {msg}")
print("\nLimitation: approximation with pdftotext; not the result of any real ATS and no guarantee of passing a filter.")
sys.exit(1 if any(l == "ERROR" for l, _ in res) else 0)
