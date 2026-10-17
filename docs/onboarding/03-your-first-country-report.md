# 03 · Your First Country Report: End to End

This is the whole job, in order. Each step links to a detailed guide. Expect **about 4–6 hours of hands-on time** spread over 2–3 weeks, plus about 1–2 hours of unattended greedy-optimizer runtime.

> **Agent shortcut:** `/country-report <Country>` runs steps 1–6 with the analyst, report-writer, and QA agents. You stay in the loop and approve each stage. See [08](08-using-the-agent-team.md).

## 0 · Before you start
- [ ] You have a country assignment (GitHub issue + `admin/trackers/Country Reports Tracker.xlsx`)
- [ ] You can run the notebook ([02-setup.md](02-setup.md))
- [ ] Create your folder: `reports/<current-semester>/<Country>/` (e.g. `reports/2026-fall/Poland/`)

## 1 · Read the country's previous report (20 min)
Find it in [`catalog/COUNTRIES.md`](../../catalog/COUNTRIES.md). Readable text copies are in `catalog/text/reports/...`. Note down:
- the **3 comparable (peer) countries** → **reuse them** for continuity
- the **category** (developed / emerging)
- the leading and emerging economies used in the RID/SDV comparison tables
- what the previous report concluded, because your report should say what changed

No previous report? Pick 3 peers of similar size/region/income, and confirm them with the research lead.

## 2 · Run the notebook (about 1 hour active, plus about 1–2 hours of greedy runtime)
Full cell-by-cell guide: [04-running-the-code.md](04-running-the-code.md). In short:
1. **Comprehensive**: ECI/PCI, GDP & ECI graphs, RID, SDV, SOI → writes `<Country>.json` + `img/`
2. **Greedy budget allocation**: 5%, 10%, 15%, 20% → 4 pickle files (**slow**: about 15–30 minutes each)
3. **Plot budget allocation**: pie charts, ECI-increment chart, portfolio table
4. **Sensitivity**: positive/negative shock charts, SDV-sensitivity and contingency tables

Save outputs to `reports/<semester>/<Country>/auto-report/` (JSON + `img/`) and `reports/<semester>/<Country>/output/` (everything else).

## 3 · Generate the draft report (15 min)
**Automated path (preferred since 2025):** upload the `<Country>/` folder (JSON + `img/`) to the Drive batch folder and run `batchProcessDocuments()` in the Apps Script ([`code/report-automation/`](../../code/report-automation/)). You get a Google Doc copy of the Auto Report Template with every `[placeholder]` and tagged image filled in.

**Manual path:** copy `templates/Auto Report Template.docx` and fill the placeholders by hand from the JSON and the notebook output.

## 4 · Write the prose (1–2 hours)
The template has `{curly-brace instructions}` where you must write country-specific context. Guide: [05-writing-the-report.md](05-writing-the-report.md).

## 5 · Self-check, then request QA (30 min)
Run the checklist in [05-writing-the-report.md#qa-checklist](05-writing-the-report.md#qa-checklist). Then open a **pull request** with your `.docx` + `.pdf` + outputs. The PR template includes the checklist. A reviewer (or the `qa-reviewer` agent: `/qa reports/<semester>/<Country>`) signs off.

## 6 · Presentation slides (30 min)
Add **3 slides** for your country to `presentations/Updated Consolidated ECI Presentation.pptx`, following the existing country examples (e.g. the India slides, about slide 116). See [06](06-presentation-and-website.md).

## 7 · Publish (15 min)
- Export the final PDF as `<Country>_<end year>.pdf`
- Upload it to the lab website ([06](06-presentation-and-website.md))
- Update the tracker row, and close your GitHub issue
- Run `python3 scripts/docx_to_md.py && python3 scripts/build_catalog.py` and commit

## Definition of done
- [ ] `reports/<semester>/<Country>/<Country>_<year>.docx` **and** `.pdf` are committed
- [ ] Auto-report JSON and `img/` are committed under `auto-report/`
- [ ] Every number in the text matches the JSON/notebook output
- [ ] Figures and tables are numbered consecutively, and captions name the right country and years
- [ ] 3 slides are added to the consolidated deck
- [ ] The website links to the new PDF
- [ ] The tracker is updated and the catalog is regenerated
