# STAR guide

## Story schema (master → stories)

```yaml
- id: story-peak-season
  status: confirmed
  competencies: [pressure, problem-solving, initiative]   # slugs from the table below
  questions: ["Tell me about a time you worked under pressure", "A time you had to reorganise work quickly"]
  situation: "Context in 1–2 sentences: where, when, what was at stake."
  task: "What the user had to achieve or solve."
  action: "What the user did — decisions, steps, conversations. First person."
  result: "What changed. Figure if it exists; otherwise a clear qualitative outcome."
  lesson: "Required for failure stories; optional otherwise."
  refs: [ventisca-coord-04]   # confirmed master ids containing every fact in the story
  source: "interview 2026-10-02"
```

## Short fictional example (to explain STAR)

- **S**: In a four-person university project, two members stopped delivering three weeks before
  the deadline.
- **T**: Deliver on time without the rest of the group carrying all the work.
- **A**: I called a short meeting, we re-split the tasks by real availability, and I set up a
  shared board with intermediate dates.
- **R**: We delivered on time and got 8.5/10; the lecturer used our board as an example.
- **L** (optional): I now agree intermediate checkpoints at the start of any group project.

## Competency coverage map

| Slug                   | Competency                    | Typical question                                          | Target |
|------------------------|-------------------------------|-----------------------------------------------------------|--------|
| `achievement`          | Achievement / impact          | "What are you most proud of?"                             | 2      |
| `problem-solving`      | Problem solving               | "A complex problem you solved"                            | 1      |
| `teamwork`             | Teamwork                      | "A time you worked with a difficult team"                 | 1      |
| `conflict`             | Conflict                      | "A disagreement with a colleague and how you handled it"  | 1      |
| `failure`              | Failure / mistake             | "Tell me about a failure" · "A mistake you made"          | 1–2    |
| `pressure`             | Pressure / deadlines          | "A time you worked under pressure"                        | 1      |
| `initiative`           | Initiative                    | "Something you improved without being asked"              | 1      |
| `learning`             | Learning fast                 | "A time you had to learn something quickly"               | 1      |
| `influence`            | Influence without authority   | "How you convinced others"                                | 1      |
| `disagree-manager`     | Disagreement with a manager   | "A time you disagreed with your boss"                     | 1      |
| `decision`             | Difficult decision            | "A hard decision you had to make"                         | 1      |
| `stakeholder`          | Customer / stakeholder        | "A difficult customer or stakeholder"                     | 1      |
| `leadership`           | Leadership (if relevant)      | "How you developed someone" · "Handling underperformance" | 1–2    |
| `ethics`               | Ethics / integrity            | "A time you had to say no"                                | opt.   |
| `adaptability`         | Change / adaptability         | "A big change and how you adapted"                        | 1      |

A bank of 8–12 good stories usually covers everything; many stories cover several rows.

## Rubric (score 0–5, one point per criterion)

1. **Clear context**: an outsider understands the situation in two sentences.
2. **Own action**: the user's personal actions are explicit ("I decided…", "I proposed…").
3. **Result**: concrete, with a figure or an unambiguous outcome.
4. **Relevance**: maps to at least one competency the target roles value.
5. **Tellable**: 1–2 minutes, no jargon the interviewer would not know, no names.

Failure stories also need: responsibility owned, lesson stated, evidence of applying it later.

## Common fixes

- Too much situation → cut to two sentences; spend the time on Action.
- "We did…" everywhere → ask "and what was your part?"
- No result → ask what changed, who noticed, what happened next; accept qualitative outcomes.
- Heroic tone → add what was hard, what the user would do differently.
- Too long → keep one thread; move secondary details to follow-up answers.
