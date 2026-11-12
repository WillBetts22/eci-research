# Data request: provenance of the ECI values in the Spring 2026 and Fall 2025 reports

Raised by nightly run `runs/2026-11-11_Q01-eci-library-repro/` (Section C).

## Problem
1. **The Spring 2026 report ECIs can't be reproduced from the data in the repo.** We extracted the "ECI increased/decreased from X in 2019 to Y in 2024" sentence from each of `reports/2026-spring/*.pdf` (Canada, Germany, Poland, Singapore, UAE, UK, Vietnam). None of those 14 values equals the same country's ECI (to 3 dp) in any of 30 variants built from `data/cleaned/2019–2023clean.csv`. The variants were the notebook as-is (an exact port, verified against the notebook's own functions), sign-oriented versions, and versions with and without the High-complexity aggregate.
2. **The reports say "2019 to 2024"**, but the repo has no 2024 data. CLAUDE.md also says the 2024 Comtrade pull hasn't been done yet.
3. **Fall 2025 Singapore report** (2019–2023): the printed % ECI changes have the right sign but not the right size (Singapore −240.31% printed vs −243.49% recomputed; China −184.44% vs −169.20%; Indonesia +181.39% vs +190.64%).
4. **Thailand has 0 in *Services and Utilities* in every cleaned CSV (2019–2023)**, so `df_to_matrix` drops it in every year. The Fall 2025 reports still quote Thailand's ECI (−617.72%), so they must have used different files.

## What's needed
- The exact cleaned CSVs (including any 2024 file) the Spring 2026 members used, with their Drive location and the date pulled. Equivalently, the notebook output files `<Country>_eci_19to24_dict.txt` / `.xlsx` for each Spring 2026 report.
- The same for the Fall 2025 Singapore and Thailand reports. In particular, which file gave Thailand a nonzero Services value.
- If a 2024 pull exists on Drive, it should go to `data/cleaned/2024clean.csv` via the `data-update` skill, so that rule 5 (numbers trace to notebook output) can be checked.

## Why it matters
QA can't verify any ECI number in the latest finished reports. Separately, the notebook's `compute_eci` sign flips in 2021–2023 on the repo data, so the printed "ECI change" figures may be sign artifacts. Without the source data we can't tell which numbers that affects.
