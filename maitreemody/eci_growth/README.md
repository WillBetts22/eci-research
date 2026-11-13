# ECI and growth: Projects 1 and 2 (Maitree Mody)

Answers Projects 1 and 2 of `willbetts/ECI_growth_prediction.md`:
1. **Replicate the classic result:** does ECI predict 10-year growth, controlling for income and resources?
2. **Did the Atlas predictions come true?** Scores every published edition of Harvard's growth projections.

Built independently of `willbetts/nightly/` (own downloads, own code), so it also checks the nightly Q12/Q16 results.

## Files
- `eci_growth_projects_1_2.ipynb`: the deliverable (question, data, method, results, robustness, findings).
- `build_notebook.py`: regenerates the notebook.
- `scripts/fetch_atlas.sh`, `scripts/fetch_worldbank.py`: download all data into `data/raw/`.
- `scripts/panel.py`: builds `data/derived/country_year.csv` and the decade panels.
- `scripts/vintages.py`: loads all 13 editions of the Growth Lab projections (2019-2026).
- `scripts/score_forecasts.py`: Project 2 scoring and benchmarks.
- `scripts/rolling_origin.py`: Project 2 step 5, rolling-origin refit of the Project 1 regression.
- `outputs/`: figures.

## Data (downloaded 2026-11-13)
- Harvard Growth Lab published ECI: SITC (1962-2024, doi:10.7910/DVN/H8SFD2) and HS92 (1995-2024, doi:10.7910/DVN/T4CHWJ).
- Growth Lab *Growth Projections and Complexity Rankings*, doi:10.7910/DVN/XTAQMC: all 13 Dataverse versions (2019-06-03 to 2026-02-08).
- World Bank WDI via API: GDP per capita (constant 2015 US$, PPP), resource rents, population, region and income group.
- Penn World Table 10.01.

## Headline results
- On the Atlas's own decades (1978/88/98), 1 SD of ECI goes with 1.65 pp/yr faster growth (published: 1.9). Adding ECI raises adjusted R² from 0.160 to 0.265 (+0.105), against the Atlas's 0.291 to 0.472 (+0.181): a similar proportional gain, smaller absolute gain.
- 1974-2024 (652 country-decades): R² +0.077 from ECI. The coefficient is positive in all five decades and significant in four; the weak one is 2004-14 (the commodity boom). The effect is similar at every income level.
- With country fixed effects the coefficient halves (p = 0.09), so the causal case is weak.
- Harvard's June 2019 forecasts for 2017-2027 correlate 0.49 with realized 2017-2024 growth (132 countries). Read as total GDP growth, their error is the smallest of all the forecasts tested, but only 2 of 15 paired tests are below 5%, and "repeat last decade" ranks countries at least as well. The edge was larger over 2017-2019.
- **The verdict depends on what `growth_proj` measures.** Its level suggests total GDP growth, but it barely moves with population growth, and the documentation doesn't say. Read as per-capita growth, the forecasts are the least accurate of all those tested.
- Most base years were never revised; 2019, 2022 and 2023 were revised later.
- Rolling-origin refit (forecast 1984, 1994, 2004, 2014 from data available then; 511 country-decades): adding ECI to income + rents gives out-of-sample R² +0.073, positive in 3 of 4 origins and in every robustness variant, but mostly not significant (main p = 0.065; 0.023 only in one variant, on squared error). It clearly beats repeating last decade's growth, and is indistinguishable from simple diversity. The gain comes mostly from a few big misses (8 country-decades give ~90% of it) and disappears in the nightly Q16 design (2005-2014 origins).

## Run
```
bash scripts/fetch_atlas.sh && python3 scripts/fetch_worldbank.py
python3 scripts/panel.py
python3 build_notebook.py && jupyter nbconvert --to notebook --execute --inplace eci_growth_projects_1_2.ipynb
```
Requires pandas, numpy, statsmodels, scipy, matplotlib, nbformat, pypdf (only to read the 2019 data dictionaries).
