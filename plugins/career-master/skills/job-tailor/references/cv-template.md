# CV template

Single column, ATS-friendly (no tables for layout, no images, no icons, standard section names).
Write Markdown with these HTML hooks, then render with `scripts/render.py`. Text inside the HTML
hooks must be plain text (no `**bold**` or links inside them).

```markdown
# Full Name

<p class="headline">Headline for this offer</p>

<p class="contact">City, Country · Remote/Hybrid · phone · email<br>linkedin · portfolio/github</p>

## Profile
3–5 sentences, first person, tailored to the offer.

## Key achievements
- **Bold result first**, then context. (3–6 bullets)

## Skills
- **Group:** skill · skill · skill
- **Group:** skill · skill

## Professional experience
### Title — Organisation <span class="date">Mon YYYY – Mon YYYY</span>
<p class="context">One line about the organisation and scope.</p>
- Achievement bullets (first person, past tense).

## Education & certifications
## Languages
```

## Section order by persona

| persona        | order                                                                                           | length |
|----------------|--------------------------------------------------------------------------------------------------|--------|
| junior         | Profile · Education (with final project) · Projects · Experience (internships, part-time) · Skills · Training · Languages | 1 page |
| returning      | Profile · Key achievements · Skills (incl. recent training) · Experience · Earlier experience (compact) · Education · Languages | 1–2 pages |
| experienced    | Profile · Key achievements · Skills · Experience · Earlier experience (compact) · Education & certifications · Languages | 2 pages |
| career-change  | Profile (bridge to the new field) · Relevant skills and projects · Experience (transferable results first) · Training · Education | 1–2 pages |

Career breaks follow the timeline `disclose` field: `none` (default) → only the dates of the
surrounding entries; `neutral` → one line "Pausa profesional, 2014–2025" / "Career break,
2014–2025" (optionally followed by recent training); `as_written` → the user's note verbatim.
Never explain more than that.

Timeline `job` entries without an experience block appear as one line: title — organisation,
dates.

Age and personal data
- By default omit graduation years for education older than ~15 years and group roles older than
  ~15 years under "Earlier experience" with years only, unless the user or the offer asks. For
  `returning`, the last 2–3 roles before the break (or the most recent ones if no break is
  recorded) are always shown in full; older ones go under
  "Earlier experience".
- Never add photo, age, date of birth, nationality or marital status, even if an old CV had them.
- Never state total years of experience ("20+ years", "más de 20 años") in the headline,
  profile, cover letter or answers, unless the offer asks for it explicitly; describe scope and
  results instead. Durations of a single role or project are fine.
- Spanish documents use `meta.grammatical_gender` for titles and adjectives (Licenciada /
  Licenciado); if it is not set, ask.
- Dates: "Mon YYYY" in the document language ("ene. 2020" / "Jan 2020"); `end: null` →
  "Actualidad" / "Present".

## Level-fit mode

Only after the user chooses it for an offer whose level-fit verdict is "one level below" or
"overqualified". It changes selection and emphasis, never facts: nothing is invented and nothing
is deleted from the master.

- Headline: the confirmed headline closest to the offer's role family and level; never a title
  the user did not hold.
- Achievements: put hands-on delivery and result items first. Reduce scope metrics (team size,
  P&L, budget, organisation size) to one credibility line in the most relevant recent role.
- Keep every must-have of the offer evidenced, with its keywords, so ATS filters still match.
- Experience: real titles and dates; never hide an employer or create a gap.
- Profile: lead with what the role asks. A one-line reason for choosing this role is allowed
  only from "What I am looking for" statements the user has approved; otherwise ask.
- Offer, in one line, a 2–3 line motivation note for the recruiter message or a form field. Do
  not write a cover letter unless the user asks for one.
- Record in `trace.md` which scope items were reduced and why.

## Style checks
- Every bullet traceable to a confirmed master id.
- Figures exactly as in `metrics` and `usage_rule` (keep "approximately").
- Keep one voice throughout: first person by default ("I led…"); vary sentence openings so
  bullets do not all start with "I".
- Dates consistent across sections; no orphan headings at page breaks.
