# Application tracker (tracker.csv)

Header (create exactly this line if the file is new):

```
id,created_at,company,role,role_family,source,agency,url,language,modality,salary_posted,salary_expected,score_total,decision,skip_reason,applied_at,first_response_at,status,status_updated_at,next_action,notes
```

## Values

- `id`: same as the offer folder name (`YYYY-MM-DD-company-role[-2]`).
- `role_family`: short label reused across rows (e.g. `data-analyst`, `operations`).
- `decision`: pending | apply | skip.
- `status`: draft → applied → screening → tech_interview → final_interview → offer | rejected |
  ghosted | withdrawn; `skipped` when the user decides not to apply.
- `score_total`: rounded integer. Salaries: free text. Dates: `YYYY-MM-DD`.

## Lifecycle

1. After scoring (job-tailor step 3): create the row with `decision: pending`, `status: draft`.
2. User skips: `decision: skip`, `status: skipped`, `skip_reason`.
3. Documents generated: `decision: apply` (status stays `draft`).
4. User says it was sent: `status: applied`, `applied_at` (ask the date if unclear).
5. News on a `draft` row: first ask whether and when they applied.
6. "Me han llamado" / "I got a call" → `screening` unless they say it was an interview; set
   `first_response_at` if empty. Rejection → `rejected` (also set `first_response_at` if empty).
7. If more than one open row could match, ask which company. Offer interview preparation after
   a positive response.
8. Suggest `ghosted` 21 days after `applied_at` with no news, and set it only if the user agrees.
9. Update `status_updated_at` on every status change.

## Format

- Write the file with Python's `csv` module: UTF-8 with BOM (`utf-8-sig`), comma separator,
  standard quoting (fields containing commas, semicolons, quotes or line breaks are quoted;
  internal quotes doubled). If the user opens it in Excel in Spanish and sees one column, explain
  Datos → Desde texto/CSV → delimitador: coma.
- Never store names, emails or phone numbers of recruiters, interviewers or other individuals in
  any column; write "recruiter", "hiring manager", or the agency name only.

## Analysis on request

- Response rate (rows with `first_response_at` that reached screening or further / rows
  applied) by score band (<55, 55–70, >70), source and role family.
- Most frequent 🔴 gaps across `score.md` files (section "Gaps") → suggest learning actions or
  target changes.
- Days from `applied_at` to `first_response_at`.
