---
name: kickoff
description: Plan a new semester for the ECI Lab. Covers the country list, member assignments, deadlines, GitHub issues, and the semester plan file. Use at the start of a semester or when the lead says "plan the semester".
argument-hint: "[semester, e.g. 2026-fall]"
---

You are the research PM planning semester `$ARGUMENTS` (if blank, infer it from today's date: Jan–Jun is spring, Jul–Dec is fall).

1. **Gather context** (don't ask for what you can read):
   - `admin/trackers/Country Reports Tracker.xlsx` (sheets "Sheet1" and "2024 Tracker") shows who did which country and when
   - `catalog/COUNTRIES.md` shows each country's last report semester. Countries not updated in 2+ years are candidates.
   - `CLAUDE.md` "Current semester context" gives the latest data year. If a new Comtrade year is likely out, propose a `/data-update` first.
2. **Ask the lead** only for: the country list agreed with Prof. Kachani (or approval of your proposed list), the member first names, and the key dates.
3. **Propose** a table: Country | Assignee | Previous report | Peers (from the previous report) | Category | Check-in date | Due date. Default timeline: assignments in week 1, check-in after 1 week, reports due after 3 weeks.
4. After approval:
   - Write `admin/todos/<semester>-plan.md` with the table, the timeline, and a weekly stand-up note
   - If `gh` is authenticated and the repo has a remote, **ask first**, then create one issue per country using `.github/ISSUE_TEMPLATE/country-report.md` (title `[<semester>] <Country> report`)
   - Create `reports/<semester>/` (with a `.gitkeep`)
5. Hand off to `archivist` to regenerate the catalog, then summarize the plan in under 15 lines.

Never write member contact details (emails, phones) into the repo. First names only.
