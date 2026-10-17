---
name: status
description: Report the current semester's progress across all country reports, covering what is done, in progress, blocked, and next. Use when someone asks for status, progress, or what's left.
---

Build a status report for the current semester (`CLAUDE.md`):

1. Read `admin/todos/<semester>-plan.md` if it exists (the assignments and due dates)
2. For each `reports/<semester>/<Country>/`, classify it by the files present:
   - `run_summary.json` only → analysis done
   - `*_draft.md` / `.docx` → drafted
   - `qa-report.md` with `VERDICT: PASS` → QA passed
   - `<Country>_<year>.pdf` → final
3. If `gh` is available, list the open issues labeled `country-report`
4. Check the hygiene: any `_work/` folders, uncommitted files (`git status --short`), and whether the catalog is stale (files newer than `catalog/CATALOG.csv`)

Output one table (Country | Owner | Stage | Due | Blocker) and then 3–5 bullets of next actions, each with an owner. Be brief.
