#!/usr/bin/env python3
"""Mechanical checks for generated CVs, letters and answers (job-tailor, step 7).

Usage:
  python lint_cv.py FILE [FILE ...] [--master profile/master.yaml] [--max-pages N]

Generic checks (always on):
  - total years of experience stated (rule 9), photo/age/nationality/marital status (rule 9)
  - very old years in the text (warning)
  - figures (%, currency, K/M) that do not appear in the master (warning: check the source id)
  - PDF page count above --max-pages (default 2)
Personal checks: every item of `cv_rules.lint` in the master file:
  {id, pattern, severity: error|warn, applies: [cv, letter, answers], message}

File kind comes from the file name: cv* -> cv, letter*/carta* -> letter, answers*/respuestas* -> answers.
Exit code 1 if there is at least one ERROR; warnings never fail. Needs PyYAML for personal rules
and pypdf for PDF page counts (both optional: the check is skipped with a notice).
"""
import argparse
import datetime
import pathlib
import re
import sys

GENERIC = [
    ("years-total", "error", ("cv", "letter", "answers"),
     r"(?i)\b(?:[1-9]\d)\+?\s*(?:years|años)\b",
     "Total years of experience stated; describe scope and results instead (unless the offer asks)"),
    ("decade", "warn", ("cv", "letter", "answers"),
     r"(?i)\b(?:a decade|two decades|una década|dos décadas)\b",
     "Decade wording is a total-years statement in disguise"),
    ("personal-data", "error", ("cv", "letter", "answers"),
     r"(?i)\b(?:date of birth|fecha de nacimiento|nationality|nacionalidad|marital status|estado civil|years old|años de edad)\b",
     "Personal data that must not appear (photo, age, nationality, marital status)"),
]
FIGURE = re.compile(r"[$€]?\d+(?:[.,]\d+)*\s?(?:%|[KkMm]\b)|[$€]\d+(?:[.,]\d+)*")


def kind_of(name):
    n = name.lower()
    if "letter" in n or "carta" in n:
        return "letter"
    if "answers" in n or "respuestas" in n:
        return "answers"
    return "cv"


def norm(tok):
    return re.sub(r"[^0-9a-z.%]", "", tok.lower().replace(",", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--master")
    ap.add_argument("--max-pages", type=int, default=2)
    a = ap.parse_args()

    personal, master_text = [], ""
    if a.master:
        master_text = pathlib.Path(a.master).read_text(encoding="utf-8")
        try:
            import yaml
            rules = (yaml.safe_load(master_text) or {}).get("cv_rules", {}).get("lint", [])
            for r in rules:
                personal.append((r["id"], r.get("severity", "warn"), tuple(r.get("applies", ["cv", "letter", "answers"])),
                                 r["pattern"], r["message"]))
        except ImportError:
            print("NOTE  PyYAML not installed: personal rules skipped")
    master_figs = {norm(m.group(0)) for m in FIGURE.finditer(master_text)}
    master_flat = norm(master_text)
    oldest = datetime.date.today().year - 15

    findings, errors = [], 0

    def add(sev, f, line, rid, msg, snip=""):
        nonlocal errors
        errors += sev == "error"
        findings.append(f"{sev.upper():5} {f}:{line}  [{rid}]  {msg}" + (f"  ->  {snip.strip()[:90]}" if snip else ""))

    for f in a.files:
        p = pathlib.Path(f)
        k = kind_of(p.name)
        if p.suffix.lower() == ".pdf":
            try:
                from pypdf import PdfReader
                n = len(PdfReader(str(p)).pages)
                if n > a.max_pages:
                    add("error", f, 0, "pages", f"{n} pages, maximum {a.max_pages}")
            except ImportError:
                print("NOTE  pypdf not installed: page count skipped")
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if "@" in line or "linkedin.com" in line.lower() or "+34" in line:
                continue
            for rid, sev, applies, pat, msg in GENERIC + personal:
                if k not in applies:
                    continue
                for m in re.finditer(pat, line):
                    if rid == "years-total" and re.match(r"\s*(?:ago|atrás|atras)", line[m.end():]):
                        continue
                    add(sev, f, i, rid, msg, line[max(0, m.start() - 20):m.end() + 30])
                    break  # one finding per rule and line
            if k == "cv":
                for m in re.finditer(r"\b(19[5-9]\d|20[01]\d)\b", line):
                    if int(m.group(1)) < oldest:
                        add("warn", f, i, "old-year", f"Year {m.group(1)} is more than 15 years old", line)
                        break
            if master_text:
                for m in FIGURE.finditer(line):
                    t = norm(m.group(0))
                    if t not in master_figs and t not in master_flat:
                        add("warn", f, i, "figure", f"Figure '{m.group(0).strip()}' not found in the master: check the source id", line)
    for x in findings:
        print(x)
    print(f"\n{errors} error(s), {len(findings) - errors} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
