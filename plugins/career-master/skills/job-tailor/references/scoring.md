# Fit scoring (0–100)

| Dimension                               | Weight | How to score                                                                 |
|-----------------------------------------|--------|------------------------------------------------------------------------------|
| Must-have requirements                  | 40     | Share of must-haves covered: 🟢 = 1, 🟡 = 0.5, 🔴 = 0                          |
| Nice-to-have requirements               | 15     | Same method over nice-to-haves                                                |
| Seniority / scope                       | 15     | Years, level, team or budget scope vs the role (too junior and too senior both reduce) |
| Domain / sector                         | 10     | Same sector 10 · adjacent 5–7 · unrelated but transferable 2–4 · unrelated 0–1 |
| Location, modality, language            | 10     | Matches `constraints` and language level                                      |
| Salary                                  | 10     | Within or above band 10 · slightly below 5–7 · far below 0–3 · not posted 7 (unknown). Far above the band: 10, but check seniority fit |

Evidence per requirement
- 🟢 confirmed master claim, or matrix `direct` whose refs are all confirmed.
- 🟡 matrix `oversaw`, `partial`, `equivalent`, `learning`, a `direct` without confirmed refs, or
  a confirmed claim that covers the requirement only in part.
- 🔴 matrix `none` or nothing in the master.

Persona adjustments
- `junior`: treat "X years of experience" as soft when the offer is entry-level; count academic
  projects and internships as evidence for tools and methods.
- `returning`: score seniority on the whole career, not only the last years; mark outdated tools
  as 🟡 when the matrix has a modern `equivalent` or `learning` entry. A career break never
  lowers the score.
- `career-change`: domain weight uses transferable evidence; state it explicitly in the table.

Round the total to an integer. Gate: <55 red · 55–70 amber · >70 green.

## Level fit (overqualification check)

Reported in `score.md` and at the gate. It is **not** part of the 0–100 score (the Seniority /
scope dimension already lowers it when the role is too junior or too senior) and it never
rejects an offer by itself.

Count only the signals the offer actually states or implies:

1. **Years asked**: about a third or less of the user's years in that role family.
2. **Title or level**: at least one level below the user's recent titles and `target_roles`
   (assistant, junior, specialist, coordinator versus manager or lead).
3. **Scope**: team size, budget or accountability clearly smaller than the user has held.
4. **Pay**: a posted salary clearly below `constraints.salary_band`. Not posted = unknown, not a
   signal.
5. **Reporting and authority**: reports to a level the user has managed, or has no decision
   authority.

Verdict: 0–1 signals → **aligned** · 2 → **one level below** · 3 or more → **overqualified**.

Write the reasons in neutral, professional terms. Never mention age or total years of
experience. Suggested action: aligned → normal flow · one level below → apply, and offer
level-fit mode (see `cv-template.md`) · overqualified → show the main risks and let the user
choose: apply in level-fit mode, apply as is, or skip.

## score.md layout

```markdown
# <Company> — <Role>  ·  <total>/100  ·  🟢|🟡|🔴

| Requirement | Type (must/nice) | Fit | Evidence (ids) |
|-------------|------------------|-----|----------------|

| Dimension | Points |
|-----------|--------|

## Level fit
<aligned | one level below | overqualified> — <signals found, one line each> — <suggested action>

## Gaps
- <skill or requirement> — <honest framing>

## Values check
<one or two neutral lines, or "values check pending: reflection not done">
```

The values check compares the offer with the approved "What I am looking for" statements in
`reflection.md`; it is not part of the score and never quotes the reflection.
