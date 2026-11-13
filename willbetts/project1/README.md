# Project 1: Does ECI predict 10-year growth? (follow-up to Maitree's answer)

Will Betts, 2026-11-13. Question from `willbetts/ECI_growth_prediction.md`, Project 1.

Maitree's merged work (`maitreemody/eci_growth/`, PR #6) already answers the main question: yes. Across
five decades (1974-2024, 652 country-decades), 1 SD more ECI goes with 1.25 pp/yr faster growth, controlling for income and resources. This folder
closes the three things that answer left open, and builds on her panel instead of redoing it.

## Answer

**Yes. The classic Atlas result replicates almost exactly once we use the Atlas's own resource control.** The
effect is positive and significant in every decade from 1974 to 2024, including 2004-2014. It is not fading.

| | Atlas 2013 (published) | Maitree (resource rents) | This folder (Atlas control) |
|---|---|---|---|
| ECI coefficient, pp/yr per SD | 1.9 | 1.66 | **1.92** |
| Adjusted R², income + resources | 0.291 | 0.160 | 0.146 |
| Adjusted R², + ECI | 0.472 | 0.266 | 0.338 |
| **Gain from adding ECI** | **+0.181** | +0.106 | **+0.191** |
| Observations | 301 | 352 | 315 (125 countries) |

Decades 1978/88/98, Liberia 1988 and Zimbabwe 1998 excluded as in the Atlas. The last column uses an
Atlas-like set of 130 countries (population at least 1.2M and exports at least $1B in 2008).

## Findings

1. **The resource control was the missing piece.** The Atlas controls for the *increase* in natural-resource
   exports over the decade (constant $, as a share of initial GDP). We built it from Growth Lab SITC data:
   fuels, ores, crude minerals and non-ferrous metals (SITC 27, 28, 32-35, 68). With it, the ECI coefficient
   (1.92) and the R² gain (+0.19) match the published values. The result does not change if gold or agriculture is added to the definition (1.92, +0.19). Resource rents, the
   control Maitree used, is close to zero and absorbs none of the commodity shocks. The one gap left is the
   baseline R² (0.15 vs 0.29). Caveat: with *both* controls the baseline rises to 0.23 and the ECI gain
   falls back to +0.10 (coefficient 1.62, still p < 0.001). So the exact R² match depends on using the
   Atlas's control alone, as the Atlas did. The ECI coefficient stays between 1.6 and 1.9 in every version.
2. **The 2004-2014 dip was the commodity boom, and the Atlas control removes most of it.** By decade, with
   the Atlas control: 1.36, 1.63, 1.65, **0.95** (p = 0.001), 1.23. With rents, 2004-14 was 0.48 (p = 0.09).
   Pooled over 1974-2024 the R² gain doubles from +0.078 to +0.147 (coefficient 1.52). See
   `figures/coef_by_decade.png`.
3. **Why the nightly Q12 run said the effect "fades" (0.44 in 2013-23 vs Maitree's 1.07 in 2014-24).**
   Stepping from Maitree's specification to Q12's one change at a time: the start year makes no
   difference (1.07 to 1.04), HS ECI instead of SITC lowers it to 0.80, and the drop to 0.44 comes from Q12's
   **resource export share** control. Removing just that control from Q12 restores 0.92. A resource share
   measured at the start of the decade is strongly negatively correlated with ECI (-0.61 HS, -0.68 SITC, 2013).
   That makes it largely a second measure of low complexity, so it absorbs ECI's effect. The Atlas control
   measures the commodity *shock* during the decade instead, and swapping it in gives 0.86. Single-decade
   standard errors are about 0.35-0.45, so none of these step-by-step differences is significant on its own.
4. **The recent-decade number depends on the start year.** For windows starting 2010, 2011, 2012, 2013 and 2014, the
   coefficient is 0.55, 0.73, 0.88, 1.04 and 1.07 (SITC ECI). Windows starting at the 2010-12 commodity peak
   are weakest. Report the five-decade pooled estimate, not a single recent window.
5. **ECI does not matter more for poorer countries.** The ECI x income interaction is about zero over five
   decades (0.06, p = 0.50, with the Atlas control). On the Atlas decades it is *positive* (0.25, p = 0.03):
   the effect is larger for richer countries, the opposite of the Atlas's claim. This agrees with Maitree.
6. **The usual outliers matter.** In 2013 and 2014, the countries that move the ECI coefficient most are Sudan, Venezuela and Equatorial Guinea (low ECI, collapsing growth),
   pushing the coefficient up, and Turkmenistan and the Central African Republic pushing it down. That is why single-decade estimates are noisy.

## What this does not settle

ECI *predicts* growth. Whether *raising* ECI *causes* growth is Project 4. Maitree's country fixed-effects
estimate halves the coefficient (0.61, p = 0.09), so the case for the reports' "maximize ECI" advice still rests on
prediction, not causation.

## Corrections to the nightly paper

`willbetts/nightly/paper` (Q12) says the ECI-growth link "has weakened" (0.89, 0.59, 0.44 by window). That
pattern comes from the resource export share control, the HS ECI and the 1995-2023 windows. On the longer
panel with the Atlas's control, the link is stable. Q12's numbers are correct for its specification, but the
"fading" interpretation should be dropped.

## Files and how to run

- `build_panel.py`: merges Maitree's `country_year.csv` with nominal GDP and the US deflator from the bulk WDI file, and
  natural-resource exports from the Growth Lab SITC 2-digit file. Writes `data/derived/country_year_p1.csv`.
- `run.py`: parts A (Atlas replication), B (Q12 vs Maitree reconciliation) and C (by decade, interaction). Prints
  every table and writes `results.json`.
- `figures/coef_by_decade.png`.

```
bash download.sh            # SITC 2-digit file (50 MB, gitignored)
python3 build_panel.py && python3 run.py
```
Needs Maitree's `country_year.csv` (`maitreemody/eci_growth/scripts/panel.py`) and the nightly WDI bulk zip
(`willbetts/nightly/external-data/download.sh`).

Data: Growth Lab *International Trade Data (SITC)*, doi:10.7910/DVN/H8SFD2, `sitc_country_product_year_2.csv`
(file 13685146), downloaded 2026-11-13. World Bank WDI bulk CSV (`NY.GDP.MKTP.CD`, `NY.GDP.DEFL.ZS`).
