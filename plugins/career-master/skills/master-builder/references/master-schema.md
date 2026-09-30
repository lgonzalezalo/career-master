# Master schema (profile/master.yaml)

YAML, UTF-8. Ids are stable, short, lowercase and unique across the file. Never reuse an id: to
retire an entry use `archive`; to erase its content use `deleted` (tombstone, see below).

| prefix                            | used for                                        | example              |
|-----------------------------------|-------------------------------------------------|----------------------|
| `<org>` or `<org>-<role>`         | experience block (add `-<role>` when the same organisation appears twice) | `acme`, `acme-admin` |
| `<block>-<nn>`                    | achievement inside that block                   | `acme-01`            |
| `t-<nn>`                          | timeline entry                                  | `t-03`               |
| `hl-` · `pv-`                     | headline · profile variant                      | `hl-01`, `pv-ops`    |
| `edu-` · `cert-` · `tr-` · `prj-` | education · certification · training · project | `edu-01`             |
| `story-<slug>`                    | STAR story                                      | `story-peak-season`  |
| `wm-` · `qa-` · `gap-<slug>`      | working method · Q&A answer · known gap         | `gap-sap`            |
| `lang-<code>`                     | language                                        | `lang-en`            |

## Statuses (every entry that has an `id`)

| status       | meaning                                                   | usable in documents |
|--------------|-----------------------------------------------------------|---------------------|
| `confirmed`  | user explicitly confirmed; defensible in interview        | yes                 |
| `draft`      | extracted or proposed, not yet reviewed                   | no                  |
| `verify`     | plausible but needs a figure, date or document            | no                  |
| `quarantine` | contradicts another source; resolution pending            | no                  |
| `archive`    | true but no longer wanted (outdated, irrelevant)          | no                  |
| `deleted`    | content erased at the user's request; only `{id, status}` remains | no          |

An entry that refers to other ids (`refs`, `timeline_ref`) is usable only if every referenced id
is `confirmed`; an achievement is usable only if its block is confirmed. A tombstone is exactly
`{id: x, status: deleted}` with no other keys; deleting a block leaves the block's tombstone in
`experience:` followed, in the same list, by one tombstone per achievement.

## Formats

- Dates are quoted strings: `"YYYY"` or `"YYYY-MM"` for periods; `"YYYY-MM-DD"` for `updated` and
  log entries. `end: null` means current (CV shows "Actualidad" / "Present").
- `meta.version` is a quoted string `"MAJOR.MINOR"`: minor +1 on every write (`"0.9"` → `"0.10"`);
  `"1.0"` once, when the first full pass reaches completeness ≥ 80; minor bumps after that.
- Figures keep the user's wording ("~12%", "unas 4 horas"); do not convert decimal separators.

## Top-level structure

```yaml
meta:
  version: "0.3"
  persona: returning            # junior | returning | experienced | career-change
  languages: [es, en]           # first = primary text language
  grammatical_gender: f         # f | m | neutral — for Spanish documents; asked, never inferred
  updated: "2026-10-01"

personal:                       # only these fields; never date of birth, ID, photo, nationality,
  name: ""                      # marital status or full street address
  location: ""                  # city, region, country
  contact: {email: "", phone: "", linkedin: "", portfolio: "", github: ""}

constraints:                    # job-search conditions, all optional
  modality: remote              # remote | hybrid | on-site | flexible
  relocation: false
  travel: ok
  contract: permanent           # permanent | temporary | freelance | any
  salary_band: "40-50K EUR gross"   # free text, soft criterion
  availability: "immediate"
  target_roles: ["Project Coordinator", "Operations Analyst"]
  avoid: ["pure sales roles"]

headlines:                      # 1-line titles for different targets
  - {id: hl-01, status: confirmed, text: "...", refs: [acme-01], source: "interview 2026-10-01"}

profile_variants:               # 3-5 sentence summaries per target
  - {id: pv-ops, status: confirmed, target: operations, text: "...", refs: [acme-01], source: "interview 2026-10-01"}

timeline:                       # skeleton confirmed in phase 2
  # type: job | education | training | project | volunteer | break
  - {id: t-01, status: confirmed, type: job, org: "Acme Logistics", title: "Operations Coordinator",
     start: "2012-03", end: "2018-06", context: "Regional distribution, 40 staff"}
  - id: t-02
    status: confirmed
    type: break
    start: "2018-07"
    end: "2026-01"
    note: ""                    # optional; only what the user wants recorded, in their words
    disclose: none              # none (CV shows dates only) | neutral ("Career break") | as_written
  - {id: t-03, status: confirmed, type: education, org: "...", title: "...", start: "2008", end: "2012"}

experience:                     # one block per role; org/title/dates must match its timeline entry
  - id: acme
    status: confirmed
    timeline_ref: t-01
    org: "Acme Logistics"
    title: "Operations Coordinator"
    start: "2012-03"
    end: "2018-06"
    context: "One-line description of the company and scope"
    team: {size: 6, reports: direct}     # only if stated
    achievements:
      - id: acme-01
        status: confirmed
        text: "First-person sentence, past tense, verb + action + result."
        metrics: ["-20% late deliveries in 12 months"]
        skills: [process-improvement, excel, supplier-management]   # slugs, shared with the matrix
        verb_level: coordinated    # did | contributed | coordinated | led | owned
        usage_rule: "Say 'coordinated', not 'led': the project was run by the regional manager."
        source: "sources/CV_2017.pdf p1 + interview 2026-10-01"

education:                      # timeline_ref links to the matching timeline entry
  - {id: edu-01, status: confirmed, timeline_ref: t-03, title: "...", org: "...", year: "2012", notes: "Final project: ...", source: "sources/CV_2017.pdf"}

certifications:
  - {id: cert-01, status: confirmed, name: "...", year: "2020", expires: null}

training:                       # courses, bootcamps, self-study with evidence
  - {id: tr-01, status: confirmed, name: "...", provider: "...", year: "2026", evidence: "evidence/...", source: "evidence/..."}

projects:                       # personal, academic, volunteer, open source
  - {id: prj-01, status: confirmed, name: "...", role: "...", text: "...", link: "...", skills: [...], source: "interview 2026-10-01"}

languages:                      # cited in trace.md by id
  - {id: lang-en, status: confirmed, language: English, level: B2, evidence: "Cambridge First 2019", source: "interview 2026-10-01"}

stories:                        # built with star-coach
  - id: story-peak-season
    status: confirmed
    competencies: [pressure, problem-solving]   # slugs: achievement, problem-solving, teamwork,
                                                # conflict, failure, pressure, initiative, learning,
                                                # influence, disagree-manager, decision,
                                                # stakeholder, leadership, ethics, adaptability
    questions: ["A time you worked under pressure"]
    situation: "..."
    task: "..."
    action: "... (first person)"
    result: "..."
    lesson: null                # required when competencies include failure
    refs: [acme-01]             # every fact in the story must be in these confirmed ids
    source: "interview 2026-10-02"

reflection_ref: profile/reflection.md   # private: never used in outgoing documents

working_method:                 # how the user likes to work, in their words
  - {id: wm-01, status: confirmed, text: "..."}

qa_bank:                        # reusable answers; real interview questions may have no answer
  - {id: qa-why-leave, status: confirmed, question: "...", answer: "...", refs: [], source: "interview 2026-10-01"}

known_gaps:                     # honest gaps and how to frame them; slug = matrix slug
  - {id: gap-sap, status: confirmed, skill: "SAP", slug: sap, framing: "Used another ERP (Navision); can ramp up quickly.", refs: [acme-01], source: "interview 2026-10-01"}

# tombstone example (content deleted at the user's request)
# - {id: acme-02, status: deleted}

verification_log:               # private: decisions on conflicts; never restate sensitive details
  - {date: "2026-10-01", item: acme-01, decision: "Team size is 6, not 10 (older CV was wrong)."}
```

## Related files

- `profile/reflection.md` — private: the user's reflection plus the approved "What I am looking
  for" statements (a list under that heading). Sensitive context only under the data rules'
  exception (explicit request, user's words, neutral wording offered).
- `profile/master.<lang>.yaml` — optional translation, wording only:

```yaml
meta: {lang: en, translation_of: "0.12"}   # master meta.version when last synced (informative)
texts:
  acme-01: {src: "3f2a9c1b", text: "I coordinated…", metrics: ["-20% late deliveries in 12 months"]}
  t-01: {src: "a71e04d2", title: "Operations Coordinator", context: "…"}
  hl-01: {src: "0c9d5e6f", text: "…"}
```

  `src` is the hash defined in the data rules (SKILL.md), computed over the translatable keys
  listed there; an id is stale when the hash no longer matches. Experience block titles are
  translated through their timeline id. A break `note` translation is used only after the user
  approves it. Status, `verb_level`, `usage_rule` and which ids are usable always come from the
  master.
- `sessions/progress.yaml` — interviewer state:

```yaml
phase: deep-dive
completeness: 45
open_items:
  - {id: oi-07, type: claim, ref: acme-02, question: "Any figure for the backlog reduction?", priority: 1}
  - {id: oi-08, type: conflict, ref: acme, question: "Team of 6 or 10?", priority: 1}
  - {id: oi-09, type: story, ref: acme-03, question: "Peak season 2016 as a pressure story", priority: 2}
sessions:
  - {date: "2026-10-01", covered: "Acme 2012-2018", confirmed: [acme-01, acme-03], next: "Education"}
```

## Writing rules for `text`

- First person, past tense for past roles ("I reorganised…"), present only for the current role.
- One idea per achievement: action + scope + result. Put figures in `metrics` as well.
- Plain words; no buzzwords the user would not say aloud.
- Team results: "my team…" or "we…"; own results: "I…". The `verb_level` must match.
- For juniors, academic, volunteer and part-time achievements are first-class entries.
