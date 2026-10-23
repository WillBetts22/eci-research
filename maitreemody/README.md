# Maitree Mody — ECI versus GDP per capita

Research question: **Do countries with higher ECI have higher GDP per capita?**

This is the core empirical claim behind ECI (Hidalgo & Hausmann 2009; *Atlas of Economic Complexity*), so the exploration is a validation check: does ECI computed from the lab's data reproduce the known income pattern?

## Files

- `exploration.ipynb`: explanation, figure and tables. Open it from this folder and run the cells in order.
- `analyze.py`: reproducible calculation. Writes everything in `outputs/`.
- `build_notebook.py`: regenerates `exploration.ipynb`.
- `outputs/findings.md`: results, interpretation and limitations.
- `outputs/`: correlations by year, 2019 regressions, residuals, country-year metrics, the 2019 figure, and the World Bank extract.

## Data

- Exports: `data/raw/<year>_mega.csv` (HS6, used for product-level HS4 ECI) and `data/cleaned/<year>clean.csv` (the lab's industry groups), 2019–2023. 2019 is the primary year. 2023 is shown for completeness only (KNOWN-ISSUES D1).
- GDP per capita: World Bank `NY.GDP.PCAP.PP.KD` (PPP, constant 2021 intl $) and `NY.GDP.PCAP.CD`, downloaded 2026-10-23 and saved in `outputs/worldbank_gdp_per_capita_2019_2023.csv`, so no download is needed. The repo's own GDP file has total GDP only, with no population.
- Results concern ECI recomputed from the lab's data, not Harvard's published rankings.

## Summary of results

- Product-level (HS4) ECI correlates 0.77–0.81 (Spearman) with log GDP per capita in every year, R² = 0.56 in 2019 (n = 126).
- The lab's 17-group ECI correlates only about 0.36–0.51, R² = 0.08, no better than counting products with RCA ≥ 1.
- The lab notebook's ECI as-is correlates negatively with income in 2021 and 2023, because `compute_eci` sets the sign from whichever country is in the first row.
- Resource exporters are richer than their ECI predicts, the known Atlas pattern.

See `outputs/findings.md` for details and limitations. Descriptive only: this doesn't test causality or growth.

## Run

From the repo root: `python3 maitreemody/analyze.py`. Requires numpy, pandas, scipy, statsmodels, matplotlib, plus `pip install pycountry tabulate`.
