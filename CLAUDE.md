# CLAUDE.md — ECI Research Lab

Read this file first in every session in this repo.

## What this repo is
The Columbia Economic Complexity (ECI) Research Lab's full archive and working space. Each semester, student members each take 1–2 countries. For each country they run the analysis notebook on UN Comtrade export data and World Bank GDP, write a ~20-page **country report** from a fixed template, add 3 slides to the consolidated presentation, and publish the PDF on the lab website.

## Operating model: the PM is in charge
- The **`research-pm`** agent (`.claude/agents/research-pm.md`) is the default entry point for open-ended requests ("what should I do", "plan the semester", "help me with my report"). It breaks work down and delegates to the specialists:
  - `data-engineer`: Comtrade/GDP retrieval, cleaning, data integrity
  - `analyst`: runs/modifies the notebook, extracts every number and figure a report needs
  - `report-writer`: fills `templates/Auto Report Template.docx` sections, writes prose and slides
  - `qa-reviewer`: independently re-checks numbers, figure/table numbering, claims, and style
  - `lit-scout`: literature review in the lab's 3-question format
  - `archivist`: files new work in the right place, updates catalog and trackers
  - `onboarding-guide`: teaches new members, answers "where is X" questions
- **Workflows** in `.claude/workflows/` run multi-country or multi-source jobs. Use them when a task fans out across more than ~3 items.
- **Skills** in `.claude/skills/` are the step-by-step playbooks the agents follow. Treat them as the source of truth for procedures.

## Where things are (current = use it; archive = history only)
| Need | Path |
|---|---|
| Notebook to run | `code/current/Spring2026.ipynb` (sections: Comprehensive → Greedy → Plot Budget → Sensitivity) |
| Cleaned data | `data/cleaned/<year>clean.csv` (2019–2023), also `data/archive/2024-fall/2019-2023 cleaned/` |
| GDP | `data/archive/2024-fall/GDP_2023.csv` (World Bank, current US$, 1990–2023) |
| Report template | `templates/Auto Report Template.docx` (placeholders like `[Country]`, `{instructions}`) |
| Auto-fill script | `code/report-automation/Code.gs` (fills the Google Doc template from `<Country>.json` + `img/`) |
| Example auto-report outputs | `reports/2025-fall/Thailand/(Correct Folder) ECI Auto Report Test/` |
| Latest finished reports | `reports/2026-spring/*.pdf` |
| A country's report history | `catalog/COUNTRIES.md` |
| Text of any .docx | `catalog/text/<same path>.md` (read these instead of the .docx) |
| Methodology | `docs/methodology.md` |
| Known bugs | `docs/KNOWN-ISSUES.md` |

## Hard rules
1. **No PII in git.** Never add rosters, phone numbers, applicant forms, resumes, or grades. If a user asks, explain why and suggest the private Drive.
2. **No secrets.** The Comtrade key comes from the `COMTRADE_API_KEY` env var (`.env`, gitignored). If you see a 32-hex key in a file, redact it.
3. **Never edit files under any `archive/` folder.** Copy the file into a current location first.
4. **Don't overwrite another member's report.** New work goes in `reports/<current-semester>/<Country>/`.
5. **Numbers in reports must trace to notebook output.** Never invent or "estimate" an ECI, GDP growth rate, R², SOI, or allocation. If a value is missing, leave the placeholder and flag it.
6. After adding or moving files, run `python3 scripts/docx_to_md.py && python3 scripts/build_catalog.py`.
7. The greedy optimizer takes **15–30 minutes per budget level** (5/10/15/20%). Warn the user before starting it, and run it in the background.

## Conventions
- Semester folders: `YYYY-spring` / `YYYY-fall`. Report files: `<Country>_<data end year>.docx` and `.pdf`.
- Comparable (peer) countries: if a country had a previous report, **reuse the same 3 peers** for continuity.
- `category` is `"developed"` or `"emerging"`. It sets the GDP-growth thresholds and the wording.
- Industry groups: 18 fixed categories (see `docs/methodology.md#industry-groups`). Note the header `"Precious Stones\t"` has a trailing tab in the cleaned CSVs.
- Country names must match the cleaned CSV exactly (e.g. `"Viet Nam"` in some files, `"Vietnam"` in others; check before running).
- Commits: small and descriptive, e.g. `Add Poland 2026-spring report + figures`.

## Current semester context
- Semester: **Fall 2026** (repo created 2026-10-17). Latest data year in the cleaned set: **2023**. The 2024 Comtrade pull has not been done yet (see `docs/onboarding/07-annual-data-update.md`).
- Spring 2026 finished reports: Canada, Germany, Poland, Singapore, UAE, United Kingdom, Vietnam.
