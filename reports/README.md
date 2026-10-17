# Country Reports

One folder per semester (`YYYY-spring` / `YYYY-fall`). `archive-2013-2018/` holds the first generation of reports and working files.

- **Find a country's report history:** `catalog/COUNTRIES.md`
- **Read a report without opening Word:** `catalog/text/reports/...`
- **Latest finished reports:** `2026-spring/` (PDFs)
- **Full auto-report example (JSON + images):** `2025-fall/Thailand/(Correct Folder) ECI Auto Report Test/`

## Layout for new reports (from 2026-fall on)
```
reports/<semester>/<Country>/
  <Country>_<year>.docx / .pdf     final report
  <Country>_<year>_draft.md         agent draft (optional)
  analysis-notes.md                 every number with its source cell
  qa-report.md                      QA verdict
  slides.md                         3-slide outline
  auto-report/<Country>.json, img/  inputs to the Apps Script
  output/                           all other notebook outputs
  <Country>_executed.ipynb          the executed notebook (provenance)
```
Older semesters use a mix of flat files and per-country folders. They were kept as they were.
