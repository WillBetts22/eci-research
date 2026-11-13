# Data request: which HS revision each reporter used in the raw Comtrade pulls

Raised by nightly run `runs/2026-11-13_P-2026-11-13-1-hs6-localization/` (section D and "Helpful to know").

## Problem (suspected, not verified)
- The number of distinct HS6 products in `data/raw/<year>_mega.csv` (same reporter sample rules) jumps from 5,465 in 2021 to 5,790 in 2022 and 5,812 in 2023. At HS4 the change is only 1,223 → 1,231.
- HS6 ECI's fit to log GDP per capita drops in 2022 (u ≥ 2: 0.480; u ≥ 3: 0.491), while HS4 stays at 0.583. In 2019–2021, HS6 matched or beat HS4.
- HS 2022 took effect in January 2022. Reporters on different HS editions produce different HS6 codes for the same goods. The raw files have **no classification column**, so the repo can't check this.

## What's needed
1. **For each reporter and year (2019–2023), the HS classification code** Comtrade reported (`classificationCode`, e.g. H5/H6) from the original pull. It could be added as a small CSV, `data/raw/<year>_classification.csv` (reporterCode, classificationCode). If the pull script is rerun, keeping that field is enough.
2. **Optional:** the official HS2017↔HS2022 correlation table (UN Statistics Division, https://unstats.un.org/unsd/classifications/Econ ; WCO correlation tables), so HS6 can be harmonized. Alternatively, Comtrade's `H?` converted series or CEPII BACI HS17, which is already harmonized.

## Why it matters
Any product-level ECI finer than HS4 (and to a lesser degree HS4 itself) is distorted when reporters use different HS editions. That matters if the lab ever moves past HS4. It also matters for the 2024 data update.
