# Skills matrix schema (profile/skills_matrix.yaml)

```yaml
meta:
  version: "1.0"               # quoted string
  updated: "2026-10-01"
  based_on_master: "1.2"        # master meta.version used for refs (string)
  target_roles: ["Junior Data Analyst"]

blocks:
  analytics:
    label: "Analytics and reporting"
    fit: high                   # high | medium | low
    skills:
      - skill: "Power BI"
        slug: power-bi              # same slug as in master achievements' skills lists
        aliases: [powerbi]
        level: direct
        how: "Automated the weekly sales report during my internship."
        refs: [quelbe-01]
      - skill: "Tableau"
        slug: tableau
        level: equivalent
        alternative: "Power BI (same dashboard concepts: data model, measures, visuals)."
      - skill: "Looker"
        slug: looker
        level: none                 # framing lives in the master's known_gaps
      - skill: "dbt"
        slug: dbt
        level: learning
        how: "Online course and personal project."
        evidence: "https://example.com/dbt-demo"

  ways_of_working:
    label: "Ways of working"
    fit: medium
    skills:
      - skill: "Agile / Scrum"
        slug: scrum
        aliases: [agile]
        level: partial
        how: "Used a shared task board with intermediate dates in a group project; no formal Scrum team experience."

learning_plan:
  - {skill: "dbt", action: "Finish course and publish a small project", by: "2026-11"}
```

Rules
- Gaps (`none`) are framed in the master's `known_gaps`, not duplicated here.
- `refs` point to master ids with `status: confirmed`. A ref to a non-confirmed id is invalid.
- `how` is one short sentence in first person, phrased according to the level.
- Keep skill names as recruiters write them (tool names in their original form).
- One skill per line; group aliases in the same entry ("PostgreSQL / Postgres").
