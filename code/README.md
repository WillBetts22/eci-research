# Code

| Folder | What | Status |
|---|---|---|
| `current/Spring2026.ipynb` | The analysis notebook in 4 sections: Comprehensive (ECI, GDP, RID, SDV, SOI; writes the auto-report JSON and images), Greedy budget allocation, Plot budget allocation, Sensitivity. Guide: `docs/onboarding/04-running-the-code.md` | current |
| `data-retrieval/` | `Data_Retrieval_2025.ipynb` (Comtrade API pull) and `datacleaning2025.ipynb` (HS → 18 groups). Guide: `docs/onboarding/07-annual-data-update.md` | current |
| `report-automation/` | Google Apps Script (`Code.gs`, `appsscript.json`, plus the original export `ECI Report Gen.json`). `batchProcessDocuments()` copies the Google Doc template once per country subfolder, replaces images by alt-text title from `img/`, and replaces `[placeholders]` from the `.json`. | current |
| `archive/<semester>/` | Every earlier version. `2024-fall/DO NOT USE_ Code_v06.ipynb` is known-broken. | archive |

To run the notebook locally for one country without Colab: `python3 scripts/run_notebook.py --help`.

## Report automation setup (Apps Script)
1. Create an Apps Script project, paste `Code.gs`, and enable the **Drive** and **Docs** advanced services (see `appsscript.json`).
2. Set `templateId` (the Google Doc version of the Auto Report Template), `destinationFolderId`, and `mainBatchFolderId`.
3. In the batch folder, create one subfolder per country containing `<Country>.json` and `img/` (from `reports/<semester>/<Country>/auto-report/`). The images must be shared publicly.
4. Run `batchProcessDocuments()`.

## Version history
2020-spring and 2021: separate notebooks (Comprehensive, Greedy new/plot, Sensitivity, SOI) → 2022-fall: updated set → 2023-fall: merged "All Code v03" → 2024-spring: v04/v05 → 2024-fall: v06 → 2025-fall: CurrentFall2025 → 2026-spring: Spring2026 (auto-report JSON).
