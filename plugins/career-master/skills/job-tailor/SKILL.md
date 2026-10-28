---
name: job-tailor
description: >-
  Evaluates the user's fit with a job offer and produces tailored, honest application material
  from their master: fit score with gaps, CV (PDF/Markdown), cover letter, answers to application
  or agency questions, interview preparation for that offer, and an application tracker. Use when
  the user pastes a job offer (text, link or screenshot) or says "evalúa esta oferta", "hazme el
  CV para esta oferta", "hazme un CV", "mejora mi currículum", "carta de presentación",
  "responde a estas preguntas", "prepárame la entrevista con una empresa", "actualiza mis
  candidaturas", "me han llamado de…", "me han rechazado", "evaluate this job", "tailor my CV",
  "update my resume", "cover letter", "prepare my interview with a company", "I got a call from…".
  General STAR stories and mock-interview practice belong to star-coach.
---

# job-tailor — from master to application

Converse in the user's language; write documents in the offer's language. Read
`references/scoring.md`, `references/cv-template.md` and `references/tracker.md` when you reach
those steps.

## Preconditions

- If `profile/master.yaml` does not exist, run the career-start onboarding first; you may still
  give a rough, clearly labelled fit reading of the offer.
- Compute completeness with the formula below. If it is below ~40, say so, offer a quick score
  anyway, and suggest continuing the master first — documents built on a thin master are weak.
- Read `profile/skills_matrix.yaml` if present; if its `based_on_master` differs from the master
  `meta.version`, treat any `direct` whose refs are not all confirmed as 🟡.
- Read `profile/reflection.md` only for the values check. If it does not exist yet, write
  "values check pending: reflection not done".
- **Language.** Status, `verb_level`, `usage_rule` and the set of usable ids always come from
  `profile/master.yaml`. Take wording from `profile/master.<lang>.yaml` only for ids whose `src`
  fingerprint still matches the master text. For missing or stale ids, translate faithfully
  (same facts, figures and verbs) and offer to save them there with `translation_of` set to the
  current master version; when creating the file, add `<lang>` to `meta.languages`.
- **No offer.** If the user asks for a CV without an offer, ask for one; if they want a general
  CV, build it for `constraints.target_roles` without scoring (same rules, trace included).

<!-- completeness:start -->
Completeness (0–100; each component pro rata; total rounded to an integer). Read
`profile/master.yaml`, `sessions/progress.yaml` and `profile/reflection.md`.
- 20 · timeline: share of timeline entries (excluding `archive` and `deleted`) that are
  `confirmed` and have dates.
- 30 · recent roles: share of recent roles with ≥3 confirmed achievements. Recent roles = roles
  in the last ~10 years of work; for `returning`, the last 2–3 roles before the break (or the
  2–3 most recent roles if no break is recorded). For
  `junior`, count confirmed achievements, education, projects and training against a target of 6.
- 15 · results: share of confirmed achievements with a metric or a clear qualitative outcome.
- 10 · conflicts: 10 if there are no open items of `type: conflict` and no `quarantine` entries.
- 15 · reflection: 15 if `profile/reflection.md` has ≥3 approved "What I am looking for" statements.
- 10 · constraints and working method: 5 each when filled.
<!-- completeness:end -->

## Non-negotiable rules

1. Use only master entries with `status: confirmed`; never `draft`, `verify`, `quarantine`,
   `archive` or `deleted`. An entry that has `refs` or `timeline_ref` is usable only if every
   referenced id is confirmed; an achievement only if its block is confirmed.
2. Respect every `usage_rule` and `verb_level` exactly (team size, "coordinated" vs "led",
   approximate figures stay approximate).
3. Never invent figures, dates, employers, tools, clients, results or facts about the company.
   Missing data → qualitative wording or ask the user.
4. First-person CV and letters, natural register (not forced-native in a second language).
5. Matrix levels govern the Skills list and phrasing: `direct` (all refs confirmed) → listed;
   `oversaw` → "in my team"; `partial` → only with its qualifier ("basic", year of use) or
   omitted; `equivalent` → list the equivalent tool, never the target tool;
   `learning` → only in training or marked "(learning / en formación)"; `none` → never claimed.
6. No colleagues' names or third parties' personal circumstances.
7. `profile/reflection.md` is private: use it only for the values check in `score.md`, in
   neutral terms. Never quote or paraphrase it in CVs, letters or answers; approved "What I am
   looking for" statements may inspire wording only after the user approves the sentence.
8. Career breaks follow the timeline `disclose` field: `none` → dates only; `neutral` →
   "Pausa profesional, YYYY–YYYY" / "Career break, YYYY–YYYY"; `as_written` → the note verbatim
   (in another language, only a translation the user approved, saved in the translation file).
   Never add a reason the user did not mark for disclosure, in any document or answer. A career
   break never lowers the fit score.
9. Never include photo, age, date of birth, nationality or marital status, even if an old CV had
   them. Never state total years of experience ("20+ years", "más de 20 años") in headlines,
   profile, letters or answers unless the offer explicitly asks; describe scope and results instead.
10. Form questions about right to work, nationality, age, health or disability, pregnancy,
    gender or gender identity, sexual orientation, ethnicity, religion, political or union
    affiliation, criminal record, family or salary history: do not answer or store them. Write
    "[Respóndela tú directamente en el formulario / Answer this yourself in the form]" in
    `answers.md` and tell the user that voluntary diversity questions can be skipped or answered
    "Prefer not to say". Questions about a career break follow rule 8.

## Flow for a new offer

1. **Ingest** the offer (paste, screenshot or link; LinkedIn usually needs the text pasted). Save
   `offers/<YYYY-MM-DD>-<company>-<role>/raw.md` (folder name in lowercase ASCII, words joined
   with hyphens, no accents or spaces, e.g. `2026-10-01-acme-logistica-coordinadora`; add `-2`,
   `-3` if it already exists). When saving `raw.md`, remove individuals' names, emails, phone
   numbers and profile links; keep company, role, requirements, conditions and the public
   application URL.
2. **Analyse**: company, role, role family, seniority, must-haves, nice-to-haves, tools, domain,
   language, modality, salary, location, form questions, and the level-fit signals
   (`references/scoring.md`, "Level fit").
3. **Score 0–100** with `references/scoring.md` and save `score.md` in the layout defined there.
   Add the tracker row now (`decision: pending`, `status: draft`), following
   `references/tracker.md`.
4. **Gate**: <55 red (recommend skipping), 55–70 amber (user decides), >70 green. Conditions in
   `constraints` are soft: mismatches lower the score and are flagged, never auto-reject. Show
   the level-fit verdict beside the colour; it never changes the score or rejects. If it is not
   "aligned", ask once whether to apply in level-fit mode. Ask
   whether to continue; if the user skips, set `decision: skip`, `status: skipped`,
   `skip_reason`.
5. **Select**: headline, profile variant and 3–8 achievements per recent role (as defined in
   the completeness formula; for `junior`, choose from all confirmed achievements, projects and
   education to fill one page), prioritising must-haves. If no confirmed headline or profile
   variant fits, draft one from confirmed ids only, show it for approval and, on an explicit yes,
   save it in the master (`headlines` / `profile_variants`, with `refs` and `source`, text in
   `meta.languages[0]`) and, if the offer is in another language, its wording in
   `profile/master.<lang>.yaml`. Show the selection for validation before writing.
6. **Generate** (only what the user asks for):
   - CV: section order and page count per persona in `references/cv-template.md`, unless the
     user prefers otherwise; single column, ATS-friendly. In level-fit mode, also follow the
     "Level-fit mode" section of that file.
   - Cover letter: 250–300 words; a hook about the company using only facts from the offer or
     pages actually read (otherwise keep it generic), 1–2 stories that match must-haves, close.
   - Answers: based on `stories`, `qa_bank` and `working_method`; respect character limits;
     rule 10 for protected questions.
   - Agency answers: honest; never claim to meet every requirement if there are gaps.
7. **Validate** before delivering: every sentence traceable to a confirmed id (save the
   sentence → id mapping in `trace.md` in the offer folder; ids may also be `lang-<code>`,
   `personal.<field>`, `constraints.<field>` or `matrix:<slug>`; `trace.md` is never sent); no
   new figures; usage rules respected; no private data (rules 7–10) and no protected traits the
   user has not approved (data rules); page count; language.
   - **7a. Mechanical checks.** Run `python3 "<this skill's folder>/scripts/lint_cv.py" --master
     profile/master.yaml offers/<folder>/cv.md` (add `letter.md` and `answers.md` if they exist).
     Fix every ERROR; fix each warning or justify it in `trace.md`.
   - **7b. Independent review.** Launch a subagent with read-only tools and a fresh context, give
     it only the file paths and the brief in `references/reviewer.md`. If subagents are not
     available, run the same checklist yourself in a separate pass. Fix every BLOCKER once, re-run
     7a and tell the user which advisories remain. Do not loop more than once.
8. **Render and save** in the offer folder (`cv.md`, `cv.pdf`, `letter.md`, `answers.md`):
   `python3 "<this skill's folder>/scripts/render.py" "offers/<folder>/cv.md"
   "offers/<folder>/cv.pdf" --title "<Name> - CV"`. The script prints the page count; adjust
   content until it matches the target, and look at the PDF as an image when possible.
   Exit code 2: no PDF engine — tell the user to open the `.print.html` it left, press Ctrl+P
   (Cmd+P on Mac), choose "Save as PDF", A4, default margins. Exit code 1: read the message
   (missing input, wrong output name, pandoc error), fix it and retry. Then set
   `decision: apply` in the tracker (status stays `draft` until the user says it was sent).

## Interview preparation

For an offer in progress: 10–15 likely questions (from the offer, the role type and the gaps),
each mapped to a STAR story or `qa_bank` answer; how to frame each gap honestly; 3–5 questions
for the user to ask the company; a short company brief if web research is available. Save it as
`offers/<folder>/interview.md` (private preparation, never sent). Offer practice mode through
star-coach.

## Tracker

Maintain `tracker.csv` following `references/tracker.md` (lifecycle, columns, format). Never
record names or contacts of recruiters or interviewers. On request, analyse response rate by
score band, source and role family, and the most frequent gaps — then suggest whether to adjust
targets, the master or the skills matrix.

## Data rules (shared by all career-master skills)

- **Before writing** `profile/master.yaml`, re-read it; if `meta.version` changed since you read
  it, merge instead of overwriting. Then bump `meta.version` (quoted `"MAJOR.MINOR"`, minor +1)
  and check the YAML still parses (Python `yaml` if available, otherwise re-read it).
- **Translation:** `profile/master.<lang>.yaml` keeps a `src` hash per id, computed from the
  master entry `e` as
  `hashlib.sha1("\x1f".join(json.dumps(e[k], ensure_ascii=False) for k in KEYS if e.get(k) is not None).encode()).hexdigest()[:8]`
  with `KEYS = [text, metrics, title, context, notes, note, name, role, language, level,
  evidence, provider, skill, target, questions, situation, task, action, result, lesson,
  question, answer, framing]`. After changing any of those fields, do not update the `src` until
  the id is re-translated, so it shows as stale.
- **Dates** are quoted strings: `"YYYY"` or `"YYYY-MM"`; `end: null` = current; logs `"YYYY-MM-DD"`.
- **Never store** — in any file of the career folder (master, translations, matrix,
  `sessions/progress.yaml`, `profile/reflection.md`, offers, tracker, `qa_bank`) or anything
  extracted from documents — date of birth or age, ID/passport/social-security numbers, photos,
  nationality or immigration status, ethnic origin, marital or family status, pregnancy, full
  street address, health or disability, religion, political opinions, union membership, sexual
  orientation or gender identity, criminal record, salary figures from payslips or reviews, or
  names and contact details of other people (use roles: "my manager", "the recruiter"). In
  `constraints` record the condition, never the reason ("part-time", not why). Only exception:
  the user may explicitly ask to keep sensitive personal context in `profile/reflection.md` or a
  break `note`, in their own words; before saving, say it is sensitive and offer neutral wording
  ("Pausa personal", "Cuidado familiar"). Open items and session logs never contain it.
- **Private working data** — `profile/reflection.md`, `score.md`, `interview.md`, `trace.md`,
  `verification_log`, `usage_rule` text and career-break notes — never goes into anything the
  user sends out. Only exception: the note of a break with `disclose: as_written`; before setting
  it, and before using it in another language, show the exact line that will appear and get an
  explicit yes.
- **Protected traits in achievements:** if a confirmed entry would reveal a protected
  characteristic (religion, politics, union, health or disability, orientation, family status —
  e.g. an association's name), tell the user and offer a neutral description ("asociación sin
  ánimo de lucro"); the user decides.
- **Public reports:** if the user asks for help reporting a problem (e.g. a GitHub issue),
  describe steps and messages only; never include master content, file contents or file paths
  that contain their username.
