# Data issue: `EU-28` row in the cleaned CSVs, and Italy's Comtrade code in the nightly library

Raised by nightly run `runs/2026-11-12_Q02-high-complexity-aggregate/` (Sections G and load cell). No external data is needed; these are code/cleaning fixes for Will or the data team to decide on.

## 1. `EU-28` is treated as a country by the notebook
- Every `data/cleaned/<year>clean.csv` (2019–2023) has an `EU-28` row (Comtrade M49 code 97, a regional aggregate).
- It passes `df_to_matrix`'s zero filter in all five years, so `compute_eci` includes it. With the sign oriented, it ranks 10th, 10th, 12th, 18th and 12th (2019–2023).
- Removing it gives Spearman 0.982–0.990 against the original ranking, but moves individual countries' ECI by up to 0.82–1.20 SD. Its exports are also added on top of its members' rows in the world totals that RCA uses.
- **Suggested fix:** drop rows whose Comtrade code is a regional aggregate (the list in `maitreemody/analyze.py` / `eci.M49_AGGREGATES`) during cleaning or before `df_to_matrix`. Suggest logging it in `docs/KNOWN-ISSUES.md` as D7.

## 2. HS chapter 84 is only in the High-complexity aggregate (D4, quantified)
- In `data/raw/2019_mega.csv`, chapter 84 is 37.3% of the aggregate's chapters and 11.9% of all exports, and it is in no regular group. Dropping the aggregate (as research-agenda §4 suggests) would delete machinery from the data. Decide on D4 (Q05) before dropping the aggregate.

## 3. Library gap: Italy
- `willbetts/nightly/lib/eci.py::m49_to_iso3(381)` returns `None` (Comtrade uses 381 for Italy; ISO numeric is 380). ISO3-keyed analyses silently lose Italy. One-line fix: add `381: 'ITA'` to `M49_SPECIAL_ISO3`. Not changed tonight because the protocol only allows editing `lib/` when the question is about it.
