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

## score.md layout

```markdown
# <Company> — <Role>  ·  <total>/100  ·  🟢|🟡|🔴

| Requirement | Type (must/nice) | Fit | Evidence (ids) |
|-------------|------------------|-----|----------------|

| Dimension | Points |
|-----------|--------|

## Gaps
- <skill or requirement> — <honest framing>

## Values check
<one or two neutral lines, or "values check pending: reflection not done">
```

The values check compares the offer with the approved "What I am looking for" statements in
`reflection.md`; it is not part of the score and never quotes the reflection.
