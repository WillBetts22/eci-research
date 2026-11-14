# Out-of-time growth forecasts: Will (Q16) vs Julia (Project 3)

William Betts, 2026-11-13. Reconciles the one result where Will's *Fourteen Tests* paper
(`willbetts/nightly/paper/eci_fourteen_tests.tex`, Q16) and Julia's Project 3
(`juliawang/eci_growth_3.ipynb`) disagree: whether adding ECI improves held-out 10-year growth forecasts.

## Answer

Both results are reproduced exactly (step 0 below = Will's published Q16; the `| J` columns of the reverse check = Julia's `horse_race.csv`).
The disagreement comes from **specification choices**. Neither person made a coding error.

| Change, starting from Will's Q16 (HS4 ECI, MSE gain vs baseline, %) | ECI (ours, HS4) | Harvard ECI |
|---|---|---|
| 0. Will Q16 as published (const 2015 US$, + resource export share, origins 2005–2014) | −1.8 | −7.0 |
| 1. Drop resource export share | +0.7 | −4.3 |
| 2. PPP outcome only | −0.9 | −7.6 |
| 3. Drop resource share + PPP (= Julia's baseline and outcome) | +2.0 | −4.4 |
| 4. + Julia's period effects and train-only scaling | +1.8 | −4.8 |
| 5. Same, Julia's three 10-yr origins only (2005, 2008, 2014) | **+4.8** | **+2.4** |

Reverse check: Julia's 8 designs with Will's resource-share control added. HS4 ECI's mean gain falls from +4.3% to +1.2%, and it beats the baseline in 5 of 8 designs instead of 7 of 8.

Three drivers, in order of size:
1. **Resource export share at the start year** (Will's baseline only). It correlates −0.32 to −0.66 with ECI, so it absorbs most of ECI's signal.
2. **Which forecast origins are scored.** ECI loses in origins 2009–2012 under either spec. Julia's three 10-yr origins skip those years.
3. **Outcome units** (constant US$ vs PPP). This makes a smaller difference, and it only helps ECI once resource share is dropped.

Period effects and scaling make no difference.

The consolidated report (spec comparison, per-origin chart, recommended wording) is in the published artifact linked from the PR/conversation.

## Files

- `step_will_to_julia.py`: Will's Q16 panel, changing one setting at a time toward Julia's spec. Writes `outputs/steps_will_to_julia.csv`.
- `julia_plus_resource_share.py`: Julia's scores, samples and designs, with and without Will's resource export share. Writes `outputs/julia_plus_resource_share.csv`.
- `outputs/*.txt`: printed output of each script.

Run from the repo root: `python3 willbetts/forecast-reconciliation/step_will_to_julia.py && python3 willbetts/forecast-reconciliation/julia_plus_resource_share.py`.
Needs `willbetts/nightly/external-data/derived/score_panel.csv`, the WDI panel, Julia's `outputs/project3/full/all_measures.csv`,
Maitree's `country_year.csv`, and `statsmodels`.
