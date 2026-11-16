# Data request: small cell-level extract of the Growth Lab HS4 panel (2019–2022)

**Raised by:** nightly run 2026-11-16 (P-2026-11-16-1, `runs/2026-11-16_P-2026-11-16-1-noise-models/`)

## What
A committed, compact extract of the Harvard Growth Lab country × HS4 × year export panel, which is already referenced in `external-data/README.md`:

- Source: Harvard Growth Lab, *International Trade Data (HS92)*, Dataverse doi:10.7910/DVN/T4CHWJ, file 13685110 (`atlas_hs92_country_product_year_4.csv`). `external-data/download.sh` + `scripts/compact_atlas.py` already build `raw/atlas_hs4_exports.pkl` (98 MB, gitignored).
- Rows: years **2019–2022** only; countries = the 112-country fixed HS4 panel (or simply all countries with ≥ $1B exports); variables `iso3, hs4, year, export_value`; drop zero cells.
- Suggested file: `external-data/derived/atlas_hs4_2019_2022.csv.gz` (should be a few MB compressed). Alternatively, just put the `.pkl` back in `external-data/raw/` on the machine the nightly agent uses.

## Why
Tonight's trade-noise model needs the size of cell-level reporting noise (σ). With only country and product totals in the repo, σ can only be bracketed between 0.031 (robust, from totals) and 0.196 (plain SD), and the "essentially unchanged" threshold τ* moves from 0.025 to 0.110 SD across that range (0.255 at σ = 0.50). A cell-level comparison of our `data/raw` HS4 values against the Growth Lab's cleaned values pins σ down, which is what the report template's band hinges on.

## Not needed
No new download source. This is a subset of a file the lab has already downloaded once (2026-11-12).
