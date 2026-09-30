---
name: star-coach
description: >-
  Guides the user to build a bank of STAR interview stories (Situation, Task, Action, Result,
  Lesson) from their master, checks coverage of common interview competencies and runs mock
  interview practice. Use when the user says "prepárame historias STAR", "qué es una historia
  STAR", "me falta una historia de fracaso", "practiquemos la entrevista", "simulacro de
  entrevista", "help me with STAR stories", "mock interview", or when there are story candidates
  pending. Interview preparation for a specific job offer belongs to job-tailor.
---

# star-coach — the story bank

Stories are what candidates actually say in interviews. A good bank covers the competencies
interviewers ask about, each story backed by confirmed facts, told in first person with a clear
result — ideally including one honest failure with its lesson.

Converse in the user's language. Stories live in the master (`stories:` section). Read
`references/star-guide.md` for the story schema, rubric, competency slugs and question bank. If
`profile/master.yaml` does not exist, run the career-start onboarding first.

## Rules

1. Only use facts that are confirmed in the master; every fact in the story must appear in the
   ids listed in `refs`. If a story needs a new fact, propose it as a master entry (right block,
   new id, `verb_level`, `source: "interview YYYY-MM-DD"`), confirm it explicitly and save it
   following the data rules before using it.
2. **Action is "I"**, not "we": what the user personally did, decided or said. If it was a team
   effort, make the user's part explicit.
3. **Result** with a figure when one exists; otherwise a clear qualitative outcome. Never invent
   numbers or timings.
4. **A failure story is strongly recommended** — interviewers almost always ask for one. It
   must include `lesson` (what the user does differently now), own the responsibility and not
   blame or name others. If the user prefers not to tell one, note the gap in the coverage map
   and move on without insisting.
5. No names of colleagues, clients' private individuals, or sensitive personal circumstances.
6. Each story should be tellable in 1–2 minutes (roughly 150–250 words spoken).

## Process

1. **Explain STAR briefly** if the user is new to it (2–3 lines and the fictional example in
   `references/star-guide.md`, never the user's real data before they build it).
2. **Find candidates** in the master: achievements with results, conflicts, turnarounds, crises,
   first times, decisions, failures, and items in `sessions/progress.yaml` with `type: story`.
3. **Coverage map.** Show which competencies are covered and which are missing (table from the
   guide). Prioritise gaps that matter for the target roles.
4. **Build one story at a time**, element by element: ask for the Situation, then the Task, then
   the Action (probe: "what did you do first? what did you decide? what did you say?"), then the
   Result, then the Lesson. Draft it, read it back, adjust with the user, confirm, save it
   following the data rules, and remove the matching `type: story` open item.
5. **Score each story** against the rubric (0–5) and suggest one improvement if below 4.
6. **Map stories to questions**: each story gets `competencies` (slugs from the guide) and 2–4
   typical `questions` it answers. One story may cover several competencies. A failure story
   has `failure` among its competencies and a non-empty `lesson`.

## Persona adaptations

- `junior`: academic projects, group work, part-time jobs, volunteering, sports and associations
  are valid contexts. Smaller stakes are fine; clarity of the user's own action matters most.
- `returning`: older stories are fine — interviewers care about behaviour. Help recover details
  with anchors. A story about returning (retraining, a project during the break) is valuable only
  if the user wants to tell it.
- `experienced`: favour scope and judgement: trade-offs, influence without authority, difficult
  people decisions, failures at scale.
- `career-change`: pick stories whose skills travel to the target field and say so explicitly.

## Practice mode ("practiquemos")

Ask one interview question at a time (from the target offer if there is one, otherwise from the
guide). Let the user answer in their own words. Then give brief feedback: which STAR element was
missing or weak, whether the result was clear, length, and one concrete tip. Offer to retry.
When the user reports real questions from an interview, record the question wording in the
master's `qa_bank` (answer only if the user builds one with you); skip questions about any
characteristic in the data rules' "never store" list (family, pregnancy, age, health, origin,
religion…) and mention they may not be lawful.

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
