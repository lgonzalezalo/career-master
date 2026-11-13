#!/usr/bin/env python3
"""Mechanical checks for generated CVs, letters and answers (job-tailor, step 7).

Usage:
  python lint_cv.py FILE [FILE ...] [--master profile/master.yaml] [--max-pages N]

Generic checks (always on):
  - total years of experience stated (rule 9), photo/age/nationality/marital status (rule 9)
  - very old years in the text (warning; replaced by a personal rule whose id ends in "-year", if any)
  - figures (%, currency, K/M) that do not appear in the master (warning: check the source id);
    figures the master names to prohibit, e.g. "never 40%" (error if prohibited everywhere; a NOTE
    per file, not counted as a warning, if other ids allow it); team sizes not in the master (warning)
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

YEARS_IN_WORDS = (r"(?:ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|"
                  r"twenty-five|thirty|diez|once|doce|trece|catorce|quince|dieciséis|diecisiete|dieciocho|"
                  r"diecinueve|veinte|veinticinco|treinta)")
GENERIC = [
    ("years-total", "error", ("cv", "letter", "answers"),
     r"(?i)\b(?:[1-9]\d\+?\s*|" + YEARS_IN_WORDS + r"\s+)(?:years|yrs|años)\b",
     "Total years of experience stated; describe scope and results instead (unless the offer asks)"),
    ("decade", "warn", ("cv", "letter", "answers"),
     r"(?i)\b(?:a decade|two decades|una década|dos décadas)\b",
     "Decade wording is a total-years statement in disguise"),
    ("personal-data", "error", ("cv", "letter", "answers"),
     r"(?i)\b(?:date of birth|fecha de nacimiento|nationality|nacionalidad|marital status|estado civil|years old|años de edad)\b",
     "Personal data that must not appear (photo, age, nationality, marital status)"),
]
NUM = r"\d+(?:[.,]\d+)*"
# $250K, €60,000 | 30%, 250K, 1,5 M€, 60.000 €, 250 EUR
FIGURE = re.compile(rf"[$€]\s?{NUM}(?:\s?[KkMm]\b)?|{NUM}\s?(?:%|[KkMm]\b|€|\$|(?:EUR|USD)\b)")
# A figure the master only mentions as prohibited: "never 40%", "nunca 30%"
NEGATED = re.compile(r"(?i)\b(?:never|nunca|not|no|jamás)\b[^.;:]{0,25}$")
PEOPLE = (r"(?:people|persons?|engineers?|developers?|employees|staff|members|reports|FTEs?|strong|"
          r"personas|ingenier[oa]s|profesionales|técnicos|empleados|desarrolladores)")
HEADCOUNT = re.compile(rf"(?i)\b(\d{{2,4}})\+?[- ]{PEOPLE}\b")
# In the master the noun may come a couple of words later: "35 operations staff"
MASTER_HEADCOUNT = re.compile(rf"(?i)\b(\d{{2,4}})\+?(?:[- ][\w&]+){{0,2}}[- ]{PEOPLE}\b")


def kind_of(name):
    n = name.lower()
    if "letter" in n or "carta" in n:
        return "letter"
    if "answers" in n or "respuestas" in n:
        return "answers"
    return "cv"


def norm(tok):
    """Same value, same token: '27,5 %' == '27.5%'; '250.000 $' == '$250K' == '250000'; '1,5 M€' == '1.5M'."""
    t = tok.lower().replace(" ", "")
    mult = 1000 if re.search(r"\dk", t) else 1_000_000 if re.search(r"\dm", t) else 1
    t = re.sub(r"[.,](?=\d{3}(?!\d))", "", t).replace(",", ".")  # drop thousands separators; decimal comma -> point
    num = re.search(r"\d+(?:\.\d+)?", t)
    if not num:
        return t
    value = f"{float(num.group(0)) * mult:.4f}".rstrip("0").rstrip(".")
    return value + ("%" if "%" in t else "")


def master_figures(text):
    """Figures the master states (allowed), figures it prohibits somewhere ('never 40%') and team sizes."""
    flat = re.sub(r"\s+", " ", text)
    allowed, restricted = set(), set()
    for m in FIGURE.finditer(flat):
        negated = NEGATED.search(flat[max(0, m.start() - 40):m.start()])
        (restricted if negated else allowed).add(norm(m.group(0)))
    allowed |= {m.group(0) for m in re.finditer(r"\b\d{4,}\b", flat)}  # plain amounts, e.g. salary band
    heads = {m.group(1) for m in MASTER_HEADCOUNT.finditer(flat)}
    return allowed, restricted, heads


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
    allowed, restricted, master_heads = master_figures(master_text)
    oldest = datetime.date.today().year - 15
    # A personal rule whose id ends in "-year" (e.g. pre-2011-year) replaces the generic old-year warning
    generic_old_year = not any(rid.endswith("-year") for rid, *_ in personal)

    findings, errors = [], 0
    notes = {}  # (file, figure) -> lines; figures a usage_rule prohibits for some ids but allows for others

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
            if k == "cv" and generic_old_year:
                for m in re.finditer(r"\b(19[5-9]\d|20[01]\d)\b", line):
                    if int(m.group(1)) < oldest:
                        add("warn", f, i, "old-year", f"Year {m.group(1)} is more than 15 years old", line)
                        break
            if master_text:
                for m in FIGURE.finditer(line):
                    t = norm(m.group(0))
                    if t in restricted and t not in allowed:
                        add("error", f, i, "figure-forbidden", f"Figure '{m.group(0).strip()}' appears in the master only as prohibited (never/nunca): check the usage_rule", line)
                    elif t in restricted:
                        notes.setdefault((f, m.group(0).strip()), []).append(str(i))
                    elif t not in allowed:
                        add("warn", f, i, "figure", f"Figure '{m.group(0).strip()}' not found in the master: check the source id", line)
                for m in HEADCOUNT.finditer(line):
                    if m.group(1) not in master_heads:
                        add("warn", f, i, "headcount", f"Team size '{m.group(0).strip()}' not found in the master: check the source id", line)
    for x in findings:
        print(x)
    for (f, fig), where in notes.items():
        print(f"NOTE  {f}:{','.join(where)}  [figure-restricted]  '{fig}' is allowed for some ids and prohibited "
              f"for others by a usage_rule: the reviewer checks each use against trace.md")
    print(f"\n{errors} error(s), {len(findings) - errors} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
