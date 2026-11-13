# Changelog

## 0.1.4 — 2026-11-13 (pilot)
- `lint_cv.py`: figures are compared by value ("27,5%" = "27.5%", "250.000 $" = "$250K"), and
  currency written after the number is detected. A figure the master only names to prohibit
  ("never 40%") is an error; if other ids allow it, it is a NOTE for the reviewer to check
  against `trace.md`. Team sizes not in the master are warned. Total years of experience are
  also caught in words ("twenty years", "quince años") and as "yrs". The generic old-year
  warning is replaced by a personal rule whose id ends in `-year`, if the master defines one.
- `ats_check.py`: keywords match whole words (plural allowed) and across line breaks; a known
  gap (`!`) that appears in the PDF is now a WARN; dates with month names and "Present" are
  recognised; a date range is no longer read as a phone number; clear message if the PDF or
  poppler is missing.

## 0.1.3 — 2026-10-28 (pilot)
- Step 7 now has two layers: `scripts/lint_cv.py` (mechanical checks: total years, personal data,
  figures not in the master, PDF pages, plus personal rules from `cv_rules.lint` in the master)
  and an independent read-only reviewer (`references/reviewer.md`).
- Form questions: for Easy Apply and similar forms, job-tailor asks for the questions before
  analysing and flags knockout ones at the gate, before any document is generated.
- Step 7c: `scripts/ats_check.py` checks the final PDF (extractable text, pages, fonts, images,
  contact, sections, dates next to roles) and the coverage of the user-approved `keywords.txt`.
  It is an approximation, not a real ATS, and never recommends keyword stuffing.

## 0.1.2 — 2026-10-21 (pilot)
- Level fit: `score.md` reports whether the role is aligned, one level below or overqualified
  (five neutral signals, never changes the score, never auto-rejects).
- Level-fit mode in `cv-template.md`: selection and emphasis only, nothing invented or deleted.

## 0.1.1 — 2026-10-02 (pilot)
- Age-neutral wording: headlines, profiles, cover letters and answers never state total years of
  experience ("20+ years", "más de 20 años") unless the offer explicitly asks; scope and results
  instead (cv-template, job-tailor rule 9, master-builder verify phase).
- Returning example headline no longer states years in the sector.
- `tools/check.py` flags total years of experience in example headlines and profile variants.

## 0.1.0 — 2026-09-30 (pilot)
- First public version.
- Skills: career-start, master-builder, skills-matrix, star-coach, job-tailor.
- Personas: junior, returning, experienced, career-change.
- Fictional example masters (junior and returning).
- Pre-release review: self-contained onboarding (tracker header, progress file), STAR example
  inside star-coach, junior completeness rule, temporary `unknown` skill state, trace file
  wording, schema for progress/reflection/translation files, render script creates output folder.
- Second review: render.py keeps "~" approximations literally, refuses non-PDF outputs, uses a
  temp file, falls back cleanly when Chromium is missing (exit 2 + printable HTML) and prints
  the page count; quoted-string versions; timeline statuses; competency slugs with `failure`;
  inline write rules in every skill; missing-master handoff; offer folder naming; `skipped`
  status; fully fictional examples; anchored .gitignore.
- Privacy and data-consistency review: delete/correct flow with tombstones and cascade;
  ingest filter (no date of birth, ID, photo, nationality, family status, address, health,
  third parties; LinkedIn archive limited to profile files); reflection.md private; career-break
  `disclose` field; translation file with `translation_of`; referential integrity for refs and
  `timeline_ref`; experience blocks linked to the timeline; `known_gaps` with ids and sources;
  quoted dates; skill slugs shared by master and matrix; recruiter data scrubbed from offers and
  tracker; UTF-8-BOM CSV; age-neutral CV defaults and grammatical gender asked, never inferred;
  shared data rules in every skill; public-issue warnings; broader .gitignore.
- Multi-lens final review (flows, data contracts, privacy, UX/packaging): single completeness
  formula (pro rata, recent roles defined for returning/junior) shared verbatim by two skills;
  headlines/profile variants drafted with refs; integrity cascade extended to every dependent
  entry and tombstones for nested ids; delete flow with confirmation, disclose alternative and
  full offer/tracker cleanup; break-note and sensitive-context exception made explicit;
  protected form questions left to the user; tracker lifecycle with `role_family` and
  `first_response_at`; fixed `score.md` layout; translation fingerprints; language ids;
  onboarding in two turns with Claude Code folder handling; READMEs with requirements, Claude
  Code steps and PDF fallback; CI permissions; `tools/check.py` extended (tombstones, per-key
  dates, id prefixes, sources, refs, slugs, gaps, shared blocks, YAML snippets, enums, versions).
