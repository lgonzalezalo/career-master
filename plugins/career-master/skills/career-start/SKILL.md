---
name: career-start
description: >-
  Onboards a new user to career-master and sets up their career folder. Use when the user says
  "empecemos", "empezar con career master", "quiero preparar mi búsqueda de empleo",
  "configura career master", "busco mi primer trabajo", "quiero volver a trabajar", "let's
  start", "start career master", "set up my career folder", "help me get back into the job
  market", or when another career-master skill finds no profile/master.yaml in the folder.
---

# career-start — onboarding

Set up the user's career workspace and explain the journey. Keep it warm, short and practical.
Converse in the user's language (Spanish or English; follow whichever they write in).

## 1. Check the workspace

- **The folder.** In Cowork, the folder is the one connected to the task; if none is connected,
  ask the user to create a folder such as `career` and connect it. In Claude Code, the folder is
  the working directory; if it is the home directory, contains a `.git` folder or other
  unrelated files, create nothing and ask the user to create an empty folder and start Claude
  Code there. All data stays in that folder, on their computer.
- **Existing master.** If `profile/master.yaml` exists, do not re-run onboarding: summarise where
  they are (read `sessions/progress.yaml`) and offer the next pending step. If it is not at the
  root, look one level down (e.g. `career/profile/master.yaml`); if found, ask whether that is
  their career folder and ask them to connect or open that folder instead. Never create a new
  master when one may already exist without asking first.

## 2. Ask a few questions (two short turns)

**Turn 1** (AskUserQuestion when available):
1. **Situation** — the persona that sets the interviewer's mode:
   - `junior`: first job or less than ~2 years of experience (students, recent graduates, trainees).
   - `returning`: coming back after a long break (for any reason) or after many years in the
     same company.
   - `experienced`: active professional looking for the next step.
   - `career-change`: moving to a different field or role family.
2. **Languages** for documents (primary, plus optional second language).
3. For Spanish documents, **grammatical gender** to use (femenino / masculino / neutro). Never
   infer it from the name.

**Turn 2** (plain text, everything optional; "no lo sé todavía" is a fine answer):
- **Target**: role families or job titles they are aiming at — the reflection step helps decide.
- **Conditions**: city/region, remote/hybrid/on-site, relocation or travel, contract type,
  salary band, availability. Record the condition, never the reason behind it.

Never ask *why* there is a career break. If the user volunteers a reason, follow the data rules
(sensitive context only in their own words, only if they ask to keep it).

## 3. Create the folder structure

The folder from step 1 is the root: create everything directly inside it (never an extra
`career/` subfolder).

```
<career folder>/
├── profile/
│   ├── master.yaml          # single source of truth (see master-builder)
│   ├── skills_matrix.yaml   # built by skills-matrix
│   └── reflection.md        # private introspection output
├── sources/                 # old CVs, LinkedIn export, reviews… (inputs, read-only)
├── evidence/                # documents that back specific claims
├── sessions/progress.yaml   # interviewer state: open items, completeness, session log
├── offers/                  # one folder per job offer
└── tracker.csv              # application log
```

Write `profile/master.yaml` with only these sections, filled from the answers (omit fields the
user did not give):

```yaml
meta:
  version: "0.1"              # quoted string "MAJOR.MINOR"
  persona: junior             # junior | returning | experienced | career-change
  languages: [es, en]         # first = primary language of master text
  grammatical_gender: f       # f | m | neutral (as answered; omit if no Spanish documents)
  updated: "<today, YYYY-MM-DD>"
personal:
  name: ""
  location: ""                # city, region, country — never a street address
  contact: {email: "", phone: "", linkedin: "", portfolio: "", github: ""}
constraints:
  modality: remote            # remote | hybrid | on-site | flexible
  relocation: false
  travel: ok
  contract: permanent         # permanent | temporary | freelance | any
  salary_band: ""             # free text, soft criterion
  availability: ""
  target_roles: []
  avoid: []
```

Create `sessions/progress.yaml`:

```yaml
phase: ingest          # ingest | timeline | deep-dive | conflicts | verify | reflection | maintain
completeness: 0
open_items: []         # {id, type: claim|conflict|story|skill, ref, question, priority}
sessions: []           # {date, covered, confirmed, next}
```

Create `tracker.csv` as UTF-8 with BOM (`utf-8-sig`, so Excel shows accents) containing exactly
this header line:

```
id,created_at,company,role,role_family,source,agency,url,language,modality,salary_posted,salary_expected,score_total,decision,skip_reason,applied_at,first_response_at,status,status_updated_at,next_action,notes
```

## 4. Explain the journey (short)

Tell the user, in plain words:

1. **Your master** (2–5 sessions of 15–20 minutes): we review your professional life — studies,
   jobs, projects, achievements — and turn it into verified facts you can defend. This is the
   heart of the process and a real introspection exercise.
2. **Your skills matrix**: what you can honestly claim for each skill, and equivalents for what
   you have not used.
3. **Your stories**: STAR stories (Situation, Task, Action, Result) for interviews.
4. **Each offer**: fit score, tailored CV, cover letter, answers and a log of applications.

Set expectations: nothing goes into a CV unless the user has confirmed it; the process rewards
honesty, not inflation; sessions can be paused and resumed at any time.

## 5. Privacy note and sources

Tell the user, in two or three lines, what is stored and where: everything lives in their
folder; `profile/` holds their master, matrix and a private reflection; `offers/` holds one
folder per application; they can ask at any time to correct or delete something. If they keep
the folder in a cloud drive or git, it must stay private.

Then explain which sources help (old CVs, LinkedIn profile PDF, performance reviews,
certificates, transcripts, portfolio or repositories, reference letters, project documents) and
that from reviews and letters Claude only takes what they say about the user's work, never other
people's names or contacts. Ask them not to add ID documents, contracts, payslips or medical
information; if such a file appears in `sources/`, it is skipped.

Finish by inviting them to drop their sources into `sources/` and start the master
(master-builder skill).

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
