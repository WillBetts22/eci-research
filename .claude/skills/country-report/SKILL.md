---
name: country-report
description: Produce one ECI country report end to end (analysis → draft → independent QA → filing) with user checkpoints. Use when someone asks to do, update, or redo a country report.
argument-hint: "<Country> [semester] [--with-greedy]"
---

Country report pipeline for: **$ARGUMENTS**

Read `docs/onboarding/03-your-first-country-report.md` for the human version of this process. As PM, run these stages in order and **stop at each checkpoint**.

### Stage 0 · Brief (you)
- Semester: from the arguments or `CLAUDE.md`
- The previous report: `catalog/COUNTRIES.md` → read its text mirror and extract the **peers**, the **category**, and the leading/emerging comparison economies
- The country's name in notebook form (e.g. `Vietnam`, `USA`). `scripts/run_notebook.py` validates it.
- Show the user: country, peers, category, semester, and whether greedy is included. **Checkpoint 1: confirm.**

### Stage 1 · Analysis (`analyst`)
Brief the analyst with everything from Stage 0. It runs `scripts/run_notebook.py` (Section 1; greedy/plot/sensitivity only if `--with-greedy`, and in the background) and writes `analysis-notes.md`.
**Checkpoint 2:** show the 5–8 headline numbers and any errors. Flag a SOI `[nobs]` under 50 as suspect (`docs/KNOWN-ISSUES.md` N3). Ask the user to confirm before drafting.

### Stage 2 · Draft (`report-writer`)
Inputs: the report folder and the previous report's path. Outputs: `<Country>_<year>_draft.md`, `<Country>_<year>.docx`, and `slides.md`.

### Stage 3 · QA (`qa-reviewer`, which must be a separate agent from the writer)
On FAIL, send the exact fix list to `report-writer`, then re-run QA. Allow at most 2 rounds, then escalate to the user with the outstanding items.

### Stage 4 · File (`archivist`)
Filing, catalog regeneration, the PII/secret scan, and a proposed commit message.

### Report back
Paths to the draft, QA report, and slides; the headline numbers; open items; and what the human still has to do (review the prose, export the PDF, add the 3 slides to the deck, update the website, update the tracker).
