#!/usr/bin/env python3
"""Automated checks for the career-master repository.

Run from the repository root:  python tools/check.py
Exit code 0 = all checks passed; 1 = at least one failure (listed at the end).

Checks
  1. Manifests: plugin.json / marketplace.json valid, names and versions consistent with CHANGELOG.
  2. Skills: frontmatter name matches folder, description present, referenced local files exist,
     no references into other skills' folders, shared data-rules block identical in every skill.
  3. Shared contracts: tracker header identical everywhere it is defined.
  4. Example masters: schema enums, quoted dates/versions, unique ids, refs confirmed,
     timeline_ref coherence, break disclosure, failure stories with lesson, known_gaps ids.
  5. Example matrix in matrix-schema.md: levels, slugs, refs resolve against the junior example.
  6. Markdown: balanced code fences.
  7. Privacy: no real-looking emails/links in plugin files; .gitignore blocks personal data and
     keeps plugin files tracked (uses a throw-away git repository).
  8. render.py: PDF for a file with spaces/accents, "~" kept literally, non-PDF output refused,
     missing input refused (PDF rendering is skipped if Playwright/Chromium are unavailable).
"""
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "career-master"
SKILLS = PLUGIN / "skills"
FAIL: list[str] = []
WARN: list[str] = []


def fail(msg: str) -> None:
    FAIL.append(msg)


def ok(cond: bool, msg: str) -> None:
    if not cond:
        fail(msg)


# Canonical enums (must match master-schema.md, matrix-schema.md, star-guide.md)
STATUSES = {"confirmed", "draft", "verify", "quarantine", "archive", "deleted"}
PERSONAS = {"junior", "returning", "experienced", "career-change"}
TIMELINE_TYPES = {"job", "education", "training", "project", "volunteer", "break"}
VERB_LEVELS = {"did", "contributed", "coordinated", "led", "owned"}
DISCLOSE = {"none", "neutral", "as_written"}
MODALITY = {"remote", "hybrid", "on-site", "flexible"}
CONTRACT = {"permanent", "temporary", "freelance", "any"}
GENDER = {"f", "m", "neutral"}
MATRIX_LEVELS = {"direct", "oversaw", "partial", "equivalent", "learning", "none"}
FIT = {"high", "medium", "low"}
COMPETENCIES = {"achievement", "problem-solving", "teamwork", "conflict", "failure", "pressure",
                "initiative", "learning", "influence", "disagree-manager", "decision",
                "stakeholder", "leadership", "ethics", "adaptability"}
PERIOD_KEYS = {"start", "end", "year", "by", "expires"}
FULLDATE_KEYS = {"updated", "date"}
PERIOD_RE = re.compile(r"^\d{4}(-(0[1-9]|1[0-2]))?$")
FULLDATE_RE = re.compile(r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])$")
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SOURCE_RE = re.compile(r"(interview|entrevista) \d{4}-\d{2}-\d{2}|^(sources|evidence)/")
PREFIX = {"timeline": r"^t-\d{2}$", "headlines": r"^hl-", "profile_variants": r"^pv-",
          "education": r"^edu-", "certifications": r"^cert-", "training": r"^tr-",
          "projects": r"^prj-", "stories": r"^story-", "working_method": r"^wm-",
          "qa_bank": r"^qa-", "known_gaps": r"^gap-", "languages": r"^lang-[a-z]{2}$"}
VERSION_RE = re.compile(r"^\d+\.\d+$")


# 1. Manifests ---------------------------------------------------------------------------------
def check_manifests() -> None:
    pj = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
    mj = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    ok(re.fullmatch(r"[a-z0-9-]+", pj.get("name", "")) is not None, "plugin.json: name not kebab-case")
    entry = next((p for p in mj.get("plugins", []) if p.get("name") == pj["name"]), None)
    ok(entry is not None, "marketplace.json: plugin entry missing")
    if entry:
        ok(entry.get("version") == pj.get("version"), "marketplace.json version != plugin.json version")
        ok((ROOT / entry["source"]).resolve() == PLUGIN.resolve(), "marketplace.json source path wrong")
    ch = (ROOT / "CHANGELOG.md").read_text()
    m = re.search(r"^## (\d+\.\d+\.\d+)", ch, re.M)
    ok(bool(m) and m.group(1) == pj.get("version"), "CHANGELOG top version != plugin.json version")


# 2. Skills ------------------------------------------------------------------------------------
def check_skills() -> None:
    shared_blocks = {}
    for sk in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        md = sk / "SKILL.md"
        if not md.exists():
            fail(f"{sk.name}: SKILL.md missing")
            continue
        text = md.read_text()
        fmm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        fm = yaml.safe_load(fmm.group(1)) if fmm else {}
        ok(fm.get("name") == sk.name, f"{sk.name}: frontmatter name mismatch")
        ok(bool(fm.get("description")), f"{sk.name}: description missing")
        ok(not re.search(r"[<>]", fm.get("description", "")), f"{sk.name}: description must not contain '<' or '>' (rejected by the plugin validator)")
        ok(len(fm.get("description", "")) <= 1024, f"{sk.name}: description longer than 1024 characters")
        for ref in set(re.findall(r"`((?:references|scripts|examples)/[\w./-]+)`", text)):
            ok((sk / ref).exists(), f"{sk.name}: referenced file missing: {ref}")
        for other in SKILLS.iterdir():
            if other.is_dir() and other.name != sk.name:
                ok(f"{other.name}/references" not in text and f"{other.name}/examples" not in text,
                   f"{sk.name}: references another skill's files ({other.name})")
        idx = text.find("## Data rules (shared by all career-master skills)")
        ok(idx >= 0, f"{sk.name}: shared data rules block missing")
        if idx >= 0:
            shared_blocks[sk.name] = text[idx:].strip()
    if len(set(shared_blocks.values())) > 1:
        fail("shared data rules block differs between skills: " + ", ".join(shared_blocks))


# 3. Shared contracts --------------------------------------------------------------------------
def between(text: str, start: str, end: str) -> str | None:
    i, j = text.find(start), text.find(end)
    return text[i:j] if i >= 0 and j > i else None


def check_contracts() -> None:
    comp = {n: between((SKILLS / n / "SKILL.md").read_text(), "<!-- completeness:start -->", "<!-- completeness:end -->")
            for n in ("master-builder", "job-tailor")}
    ok(all(comp.values()), "completeness block missing in master-builder or job-tailor")
    ok(len(set(comp.values())) == 1, "completeness block differs between master-builder and job-tailor")
    for f in [SKILLS / "job-tailor/SKILL.md", SKILLS / "job-tailor/references/scoring.md"]:
        ok("<55" in f.read_text() and ">70" in f.read_text(), f"{f.name}: gate thresholds <55 / >70 missing")
    # every yaml snippet in docs must parse
    for f in PLUGIN.rglob("*.md"):
        for i, block in enumerate(re.findall(r"```yaml\n(.*?)```", f.read_text(), re.S)):
            try:
                yaml.safe_load(block.replace("<today, YYYY-MM-DD>", "2026-01-01"))
            except yaml.YAMLError as e:
                fail(f"{f.relative_to(ROOT)}: yaml block {i} does not parse: {str(e)[:80]}")
    # enums stated in career-start must match canonical ones
    cs = (SKILLS / "career-start/SKILL.md").read_text()
    for label, enum in (("persona", PERSONAS), ("modality", MODALITY), ("contract", CONTRACT)):
        m = re.search(rf"{label}:.*#\s*([\w|\- ]+)", cs)
        ok(bool(m) and {x.strip() for x in m.group(1).split("|")} == enum, f"career-start: {label} enum differs")
    # README versions
    ver = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())["version"]
    for f in [ROOT / "README.md", PLUGIN / "README.md"]:
        ok(f"v{ver}" in f.read_text(), f"{f.relative_to(ROOT)}: version v{ver} not mentioned")
    header_re = re.compile(r"^id,created_at,company[^\n]*$", re.M)
    headers = {}
    for f in [SKILLS / "career-start/SKILL.md", SKILLS / "job-tailor/references/tracker.md"]:
        found = header_re.findall(f.read_text())
        ok(len(found) == 1, f"{f.relative_to(ROOT)}: tracker header not found exactly once")
        if found:
            headers[str(f)] = found[0]
    ok(len(set(headers.values())) == 1, "tracker header differs between files")


# 4. Example masters ---------------------------------------------------------------------------
def walk(obj, path, ids, errs):
    if isinstance(obj, dict):
        if "id" in obj:
            if obj["id"] in ids:
                errs.append(f"duplicate id {obj['id']}")
            ids[obj["id"]] = obj
            if obj.get("status") not in STATUSES:
                errs.append(f"{obj['id']}: missing or bad status {obj.get('status')!r}")
            if obj.get("status") == "deleted" and set(obj) != {"id", "status"}:
                errs.append(f"{obj['id']}: tombstone must contain only id and status")
        for k, v in obj.items():
            if v is None or path.endswith("meta") and k == "version":
                pass
            elif k in PERIOD_KEYS and (not isinstance(v, str) or not PERIOD_RE.match(v)):
                errs.append(f"{path}/{k}: must be a quoted \"YYYY\" or \"YYYY-MM\" string, got {v!r}")
            elif k in FULLDATE_KEYS and (not isinstance(v, str) or not FULLDATE_RE.match(v)):
                errs.append(f"{path}/{k}: must be a quoted \"YYYY-MM-DD\" string, got {v!r}")
            walk(v, f"{path}/{k}", ids, errs)
    elif isinstance(obj, list):
        for i, x in enumerate(obj):
            walk(x, f"{path}[{i}]", ids, errs)


def check_master(path: pathlib.Path) -> dict:
    d = yaml.safe_load(path.read_text())
    errs: list[str] = []
    ids: dict = {}
    walk(d, "", ids, errs)
    live = lambda e: isinstance(e, dict) and e.get("status") != "deleted"
    meta = d.get("meta", {})
    if "es" in meta.get("languages", []) and "grammatical_gender" not in meta:
        errs.append("meta.grammatical_gender required when es is a document language")
    for section, rx in PREFIX.items():
        for e in d.get(section, []) or []:
            if isinstance(e, dict) and "id" in e and not re.match(rx, str(e["id"])):
                errs.append(f"{section}: id {e['id']} does not match {rx}")
    for section in ("headlines", "profile_variants", "qa_bank", "known_gaps", "education", "training", "projects", "languages"):
        for e in d.get(section, []) or []:
            if live(e) and e.get("status") == "confirmed" and not e.get("source"):
                errs.append(f"{e.get('id')}: confirmed entry without source")
            if live(e) and e.get("source") and not SOURCE_RE.search(str(e["source"])):
                errs.append(f"{e.get('id')}: source format not recognised: {e['source']}")
            for r in (e.get("refs") or []) if live(e) else []:
                if r not in ids:
                    errs.append(f"{e.get('id')}: ref {r} does not exist")
                elif e.get("status") == "confirmed" and ids[r].get("status") != "confirmed":
                    errs.append(f"{e.get('id')}: ref {r} not confirmed")
            if live(e) and e.get("timeline_ref") and e["timeline_ref"] not in ids:
                errs.append(f"{e.get('id')}: timeline_ref {e['timeline_ref']} does not exist")
    for g in d.get("known_gaps", []) or []:
        if live(g) and not (g.get("slug") and SLUG_RE.match(g["slug"]) and g["id"] == f"gap-{g['slug']}"):
            errs.append(f"{g.get('id')}: known gap needs slug and id gap-<slug>")
    for v in d.get("verification_log", []) or []:
        if v.get("item") not in ids:
            errs.append(f"verification_log item {v.get('item')} does not exist")
    if not (isinstance(meta.get("version"), str) and VERSION_RE.match(meta["version"])):
        errs.append("meta.version must be a quoted MAJOR.MINOR string")
    if meta.get("persona") not in PERSONAS:
        errs.append("meta.persona invalid")
    if meta.get("grammatical_gender") not in GENDER | {None}:
        errs.append("meta.grammatical_gender invalid")
    c = d.get("constraints", {})
    if c.get("modality") not in MODALITY | {None}:
        errs.append("constraints.modality invalid")
    if c.get("contract") not in CONTRACT | {None}:
        errs.append("constraints.contract invalid")
    for t in [x for x in d.get("timeline", []) if live(x)]:
        if t.get("type") not in TIMELINE_TYPES:
            errs.append(f"{t.get('id')}: bad timeline type")
        if t.get("type") == "break" and t.get("disclose") not in DISCLOSE:
            errs.append(f"{t.get('id')}: break needs disclose in {sorted(DISCLOSE)}")
    for b in [x for x in d.get("experience", []) if live(x)]:
        t = ids.get(b.get("timeline_ref"))
        if not t:
            errs.append(f"{b['id']}: timeline_ref missing or unknown")
            continue
        if t.get("type") != "job":
            errs.append(f"{b['id']}: timeline_ref must point to a job entry")
        for k in ("org", "title", "start", "end"):
            if t.get(k) != b.get(k):
                errs.append(f"{b['id']}: {k} differs from {b['timeline_ref']}")
        for a in [x for x in b.get("achievements", []) if live(x)]:
            if not re.match(rf"^{re.escape(b['id'])}-\d{{2}}$", a["id"]):
                errs.append(f"{a['id']}: achievement id must be {b['id']}-NN")
            for sl in a.get("skills", []):
                if not SLUG_RE.match(sl):
                    errs.append(f"{a['id']}: skill slug {sl!r} invalid")
            if a.get("verb_level") not in VERB_LEVELS:
                errs.append(f"{a['id']}: bad verb_level")
            if a.get("status") == "confirmed" and not a.get("source"):
                errs.append(f"{a['id']}: confirmed claim without source")
    for s in [x for x in d.get("stories", []) if live(x)]:
        for r in s.get("refs", []):
            if r not in ids:
                errs.append(f"{s['id']}: ref {r} does not exist")
            elif s.get("status") == "confirmed" and ids[r].get("status") != "confirmed":
                errs.append(f"{s['id']}: ref {r} not confirmed")
        if not s.get("refs"):
            errs.append(f"{s['id']}: story without refs")
        bad = set(s.get("competencies", [])) - COMPETENCIES
        if bad:
            errs.append(f"{s['id']}: unknown competencies {bad}")
        if "failure" in s.get("competencies", []) and not s.get("lesson"):
            errs.append(f"{s['id']}: failure story without lesson")
    years_re = re.compile(r"\b\d+\s*\+\s*(años|years)\b|\b\d+\s*(años|years)\s+(de experiencia|of experience|en|in)\b"
                          r"|(más de|over|more than)\s+\d+\s+(años|years)", re.I)
    for section in ("headlines", "profile_variants"):
        for e in d.get(section, []) or []:
            if live(e) and years_re.search(str(e.get("text", ""))):
                errs.append(f"{e.get('id')}: states total years of experience (age-neutral rule)")
    for e in errs:
        fail(f"{path.name}: {e}")
    return {"ids": ids, "doc": d}


# 5. Matrix example ----------------------------------------------------------------------------
def check_matrix(junior: dict) -> None:
    junior_ids, junior_doc = junior["ids"], junior["doc"]
    text = (SKILLS / "skills-matrix/references/matrix-schema.md").read_text()
    block = re.search(r"```yaml\n(.*?)```", text, re.S)
    ok(block is not None, "matrix-schema.md: yaml example missing")
    if not block:
        return
    m = yaml.safe_load(block.group(1))
    ok(isinstance(m["meta"].get("version"), str), "matrix example: version not a string")
    ok(isinstance(m["meta"].get("based_on_master"), str), "matrix example: based_on_master not a string")
    ok(m["meta"].get("based_on_master") == junior_doc["meta"]["version"],
       "matrix example: based_on_master != junior example meta.version")
    gap_slugs = {g.get("slug") for g in junior_doc.get("known_gaps", [])}
    slugs = set()
    for name, b in m["blocks"].items():
        ok(b.get("fit") in FIT, f"matrix {name}: bad fit")
        for s in b["skills"]:
            ok(s.get("level") in MATRIX_LEVELS, f"matrix {s.get('skill')}: bad level")
            ok(bool(s.get("slug")) and SLUG_RE.match(s.get("slug", "")) is not None, f"matrix {s.get('skill')}: slug missing or invalid")
            if s.get("level") == "none":
                ok(s.get("slug") in gap_slugs, f"matrix {s.get('skill')}: none without gap-{s.get('slug')} in master")
            if s.get("level") == "oversaw":
                ok(re.search(r"in my team|en mi equipo", s.get("how", ""), re.I) is not None, f"matrix {s.get('skill')}: oversaw without 'in my team' phrasing")
            if s.get("level") == "direct":
                ok(bool(s.get("refs")), f"matrix {s.get('skill')}: direct without refs")
                for r in s.get("refs", []):
                    ok(s.get("slug") in junior_ids.get(r, {}).get("skills", []), f"matrix {s.get('skill')}: ref {r} does not list slug {s.get('slug')}")
            ok(s.get("slug") not in slugs, f"matrix duplicate slug {s.get('slug')}")
            slugs.add(s.get("slug"))
            for r in s.get("refs", []):
                ok(junior_ids.get(r, {}).get("status") == "confirmed",
                   f"matrix {s.get('skill')}: ref {r} not a confirmed id in junior example")
            if s.get("level") == "equivalent":
                ok(bool(s.get("alternative")), f"matrix {s.get('skill')}: equivalent without alternative")
            if s.get("level") == "learning":
                ok(bool(s.get("evidence")), f"matrix {s.get('skill')}: learning without evidence")
    all_skills = {s.get("skill") for b in m["blocks"].values() for s in b["skills"]}
    for lp in m.get("learning_plan", []):
        ok(lp.get("skill") in all_skills, f"matrix learning_plan skill {lp.get('skill')} not in matrix")


# 6. Markdown ----------------------------------------------------------------------------------
def check_markdown() -> None:
    for f in ROOT.rglob("*.md"):
        if ".git" in f.parts:
            continue
        n = sum(1 for line in f.read_text().splitlines() if line.lstrip().startswith("```"))
        ok(n % 2 == 0, f"{f.relative_to(ROOT)}: unbalanced code fences")


# 7. Privacy -----------------------------------------------------------------------------------
def check_privacy() -> None:
    email_re = re.compile(r"[\w.+-]+@([\w-]+\.)+[a-z]{2,}", re.I)
    url_re = re.compile(r"https?://[^\s)\"'>]+|(?:github|linkedin)\.com/[^\s)\"'>]+", re.I)
    allowed_url = re.compile(r"example\.com|lgonzalezalo|claude\.com|anthropic\.com", re.I)
    for f in PLUGIN.rglob("*"):
        if not f.is_file() or f.suffix not in {".md", ".yaml", ".json", ".py", ".css"}:
            continue
        t = f.read_text()
        for m in email_re.finditer(t):
            ok(m.group(0).lower().endswith("@example.com"), f"{f.relative_to(ROOT)}: real-looking email {m.group(0)}")
        for m in url_re.finditer(t):
            ok(bool(allowed_url.search(m.group(0))), f"{f.relative_to(ROOT)}: unexpected link {m.group(0)}")
    if not shutil.which("git"):
        WARN.append("git not available: .gitignore check skipped")
        return
    with tempfile.TemporaryDirectory() as tmp:
        repo = pathlib.Path(tmp) / "r"
        shutil.copytree(ROOT, repo, ignore=shutil.ignore_patterns(".git"))
        personal = ["profile/master.yaml", "profile/master.en.yaml", "mi-carrera/profile/master.yaml",
                    "mi-carrera/tracker.csv", "data/offers/x/cv.pdf", "offers/x/trace.md",
                    "sources/CV_2017.pdf", "evidence/cert.pdf", "sessions/progress.yaml",
                    "reflection.md", "tracker.csv", "cv.docx", "Connections.csv", "export.zip",
                    "offers/x/cv.print.html", "career-master.plugin"]
        for p in personal:
            fp = repo / p
            fp.parent.mkdir(parents=True, exist_ok=True)
            fp.write_text("x")
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True)
        subprocess.run(["git", "add", "-A"], cwd=repo, check=True)
        tracked = set(subprocess.run(["git", "ls-files"], cwd=repo, capture_output=True, text=True).stdout.split())
        for p in personal:
            ok(p not in tracked, f".gitignore: personal file would be committed: {p}")
        for f in PLUGIN.rglob("*"):
            if f.is_file() and "__pycache__" not in f.parts:
                rel = str(f.relative_to(ROOT))
                ok(rel in tracked, f".gitignore: plugin file would be ignored: {rel}")


# 8. render.py ---------------------------------------------------------------------------------
def check_render() -> None:
    script = SKILLS / "job-tailor/scripts/render.py"
    with tempfile.TemporaryDirectory() as tmp:
        d = pathlib.Path(tmp) / "Oferta Café"
        d.mkdir()
        src = d / "CV Lucía.md"
        src.write_text("# Lucía\n\n<p class=\"headline\">Analista</p>\n\n- de ~12% a ~5% @x ^y^\n", encoding="utf-8")
        r = subprocess.run([sys.executable, str(script), str(src), str(d / "x.html")], capture_output=True, text=True)
        ok(r.returncode == 1, "render.py: non-PDF output not refused")
        r = subprocess.run([sys.executable, str(script), str(d / "nope.md"), str(d / "x.pdf")], capture_output=True, text=True)
        ok(r.returncode == 1, "render.py: missing input not refused")
        if not shutil.which("pandoc"):
            WARN.append("pandoc not available: '~' literal check skipped")
        else:
            html = subprocess.run(["pandoc", str(src), "-f", "markdown-subscript-superscript-citations", "-t", "html"],
                                  capture_output=True, text=True).stdout
            ok("<sub>" not in html and "~12%" in html, "render: '~' approximations not kept literally")
            ok(re.search(r"PANDOC_FORMAT\s*=\s*\"markdown-subscript-superscript-citations\"", script.read_text()) is not None,
               "render.py: pandoc format changed")
        env = dict(os.environ, RENDER_FORCE_BUILTIN="1", PLAYWRIGHT_BROWSERS_PATH="/nonexistent")
        r = subprocess.run([sys.executable, str(script), str(src), str(d / "fb" / "cv.pdf")], capture_output=True, text=True, env=env)
        ok(r.returncode == 2, f"render.py: builtin/no-browser fallback exit {r.returncode}, expected 2")
        fb = d / "fb" / "cv.print.html"
        ok(fb.exists() and "<h1>" in fb.read_text() and 'class="headline"' in fb.read_text(),
           "render.py: builtin converter fallback HTML missing or wrong")
        if fb.exists():
            fb.unlink()
        out = d / "out dir" / "CV Lucía.pdf"
        r = subprocess.run([sys.executable, str(script), str(src), str(out)], capture_output=True, text=True)
        if r.returncode == 0:
            ok(out.exists() and out.stat().st_size > 1000, "render.py: PDF missing or empty")
            ok("page" in r.stdout, "render.py: page count not printed")
            ok(not list(d.rglob("*.html")), "render.py: left HTML files behind")
        elif r.returncode == 2:
            if os.environ.get("CI"):
                fail("render.py: no PDF produced in CI (exit 2)")
            WARN.append("render.py: no PDF engine here (exit 2); fallback path exercised")
            ok(any(d.rglob("*.print.html")), "render.py: fallback HTML not written")
        else:
            fail(f"render.py: unexpected exit {r.returncode}: {r.stderr[-300:]}")


def main() -> int:
    check_manifests()
    check_skills()
    check_contracts()
    junior = check_master(SKILLS / "master-builder/examples/junior-master.yaml")
    check_master(SKILLS / "master-builder/examples/returning-master.yaml")
    check_matrix(junior)
    check_markdown()
    check_privacy()
    check_render()
    for w in WARN:
        print(f"WARN  {w}")
    for f in FAIL:
        print(f"FAIL  {f}")
    print(f"\n{len(FAIL)} failure(s), {len(WARN)} warning(s)")
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main())
