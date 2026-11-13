# External data (downloaded 2026-11-12)

Used by the Q06 and Q12-Q16 runs and by the paper. Re-download with `bash download.sh`.
Large originals are gitignored; the small extracts that the scripts read are committed.

| File | Source | Committed? |
|---|---|---|
| `raw/atlas_hs92_country_year.csv` | Harvard Growth Lab, *International Trade Data (HS92)*, Dataverse doi:10.7910/DVN/T4CHWJ, file 13685109: published ECI, COI, diversity, exports by country-year 1995-2024 | yes (0.4 MB) |
| `raw/atlas_hs92_data_dictionary.csv`, `raw/atlas_hs92_product_year_4.csv` | same dataset (dictionary; HS4 PCI by year) | yes |
| `raw/atlas_hs92_country_product_year_4.csv` | same dataset, file 13685110: exports by country x HS4 x year | no (451 MB) |
| `raw/atlas_hs4_exports.pkl` | compacted from the file above by `scripts/compact_atlas.py` | no (98 MB) |
| `raw/wdi_panel.csv` | World Bank WDI bulk CSV (`WDI_CSV.zip`), extracted by `scripts/extract_wdi.py`: GDPpc (constant 2015 US$, PPP constant, current), population, resource rents, enrollment, R&D, trade, internet, electricity, private credit, merchandise exports; 1995-2024 | yes |
| `raw/wgi_panel.csv` | Worldwide Governance Indicators 2023 update (`wgidataset.xlsx`), extracted by `scripts/extract_wgi.py`: point estimates for government effectiveness, regulatory quality, rule of law, control of corruption; 1996-2022 | yes |
| `raw/pwt1001.dta` | Penn World Table 10.01 (dataverse.nl file 354098) | yes (3.5 MB) |
| `derived/score_panel.csv` | `scripts/build_score_panel.py`: 11 complexity variants per country-year 1995-2024 computed from the Growth Lab HS4 panel, merged with the files above | yes (1.8 MB) |

Notes
- The World Bank JSON API was hanging on 2026-11-12, so `scripts/fetch_wdi.py` (API version) is kept for reference but the bulk file is what was used.
- WGI uses a few non-ISO codes (ADO, ROM, ZAR, TMP, WBG, KSV); `extract_wgi.py` maps them to ISO3.
- PWT 10.01 ends in 2019.
