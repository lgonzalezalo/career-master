---
name: skills-matrix
description: >-
  Builds and maintains the user's skills matrix: for each skill in their target market, an honest
  level (direct, oversaw, partial, equivalent, learning, none) backed by references to confirmed
  master claims, plus defensible equivalents and gaps. Use when the user says "haz mi matriz de
  skills", "qué skills puedo defender", "mis habilidades", "qué competencias tengo", "actualiza
  la matriz", "no sé si puedo decir que sé X", "build my skills matrix", "which skills can I
  claim".
---

# skills-matrix — what the user can honestly claim

The matrix (`profile/skills_matrix.yaml`) answers, for each skill a recruiter may ask about:
*can I claim it, how, and with what evidence?* It feeds offer scoring, the CV Skills list and
honest gap framing. It is **not** a source of achievement sentences: those only come from
confirmed master claims.

Converse in the user's language. Read `references/matrix-schema.md` before writing. If
`profile/master.yaml` does not exist, run the career-start onboarding first; if the master has few
confirmed claims, say the matrix will be thin and suggest continuing the master.

## Levels

| level        | icon | meaning                                                               | how to phrase it                           |
|--------------|------|-----------------------------------------------------------------------|--------------------------------------------|
| `direct`     | 🟢   | hands-on, own use, can explain details; refs to confirmed claims      | "I used / built / ran…"                    |
| `oversaw`    | 🟡   | in my team or area as the person responsible, without own hands-on use | "in my team / on my platform…", never "I used" |
| `partial`    | 🟡   | basic, old or indirect use                                            | "basic experience with…", "used in 2015…"  |
| `equivalent` | 🟡   | not used, but a defensible equivalent (e.g. SSIS → Azure Data Factory) | "I haven't used X; I have used Y, which…"  |
| `learning`   | 🟡   | actively learning with evidence (course, project, repo)               | "I'm learning X — see project…"            |
| `none`       | 🔴   | no experience and no real equivalent                                  | framed in the master's `known_gaps`        |

A `direct` whose refs are missing or not all confirmed counts as 🟡 until fixed.

## Process

1. **Scope the market.** From `constraints.target_roles`, recent offers in `offers/` and the
   user's input, build 4–8 blocks of skills recruiters in that market ask for (e.g. for data
   roles: architecture, cloud, engineering, analytics, governance, AI, ways of working, domain;
   for operations roles: planning, ERP, reporting, people, customer, compliance). Include soft and
   domain skills, not only tools.
2. **Pre-fill from the master.** For each skill, look for confirmed claims whose `skills` list
   contains its slug and propose a level with `refs` to those ids. Mark the rest as `unknown` —
   a temporary working state kept in `sessions/progress.yaml` (`type: skill`), never saved in the
   matrix. Remove those open items once answered.
3. **Interview the unknowns** in small batches (5–8 skills per message, grouped by block):
   "Have you used it yourself, had it in your team, used it long ago, used something
   equivalent, or not at all?" Ask for the concrete example behind every `direct`.
4. **New facts.** If an example the user gives is not in the master yet, propose it as a master
   entry (right experience or project block, new id, `verb_level`, `source: "interview
   YYYY-MM-DD"`), confirm it explicitly, save it following the data rules and put its id in
   `refs`. If the user does not confirm, save the skill as `partial` without refs (never
   `direct`).
5. **Equivalents.** For `none` or `partial` skills, look for a defensible equivalent in the
   user's history and propose it. This is especially valuable for `returning` users (old tools
   → modern tools) and `career-change` users (skills that travel across fields).
6. **Gaps.** For each skill that stays `none`, agree a framing with the user and add it to the
   master's `known_gaps` as `{id: gap-<slug>, status: confirmed, skill: "<name>", slug: <slug>,
   framing: "...", refs: [<ids the framing relies on>], source: "interview YYYY-MM-DD"}`
   following the data rules; optionally add a
   `learning_plan` entry to the matrix.
7. **Validate and save.**
   - Every skill has a `slug` (lowercase, hyphens) matching the slugs used in master `skills:`
     lists, plus `aliases` for other spellings.
   - Every `direct` has `refs` to confirmed master claims whose `skills` include the slug.
   - Every `oversaw` carries the "in my team" / "en mi equipo" phrasing in `how`.
   - `equivalent` names the `alternative`; `learning` requires `evidence`.
   - Every `none` has a matching `gap-<slug>` in the master.
   - Bump the matrix `meta.version` (quoted string) and set `based_on_master` to the master
     `meta.version` used (string).
8. **Summarise** per block: fit (`high` / `medium` / `low`), strongest skills, main gaps, and 2–3
   suggested learning actions tied to the target roles.

## Keeping it current

- When a new offer mentions a skill not in the matrix, ask the user and add it.
- When `based_on_master` differs from the master version, re-check that all `refs` are still
  confirmed; drop refs that are not and re-evaluate those levels with the user.
- Never upgrade a level without the user's explicit statement.

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
