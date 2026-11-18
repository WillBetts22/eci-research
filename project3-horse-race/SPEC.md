# Project 3 frozen specification

**Frozen 2026-11-18** by Will. Julia must sign off at the Wed 11/18 check-in. After sign-off, any change needs **both** Julia and Will and gets a dated line in the change log at the bottom of this file. **No changes after the Thu 11/19 numbers freeze.**

The question this spec answers: **Does ECI improve out-of-time 10-year growth forecasts beyond (a) income plus resources and (b) plain diversity?**

This is the plan's suggested default: Julia's pipeline and samples, Will's scored origins, and resource export share as a pre-specified second arm.

---

## 1. Outcome
- `growth = 100 × ln(GDPpc_{t+10} / GDPpc_t) / 10`, the annualized log growth of real GDP per capita, PPP, constant international $ (`gdppc_ppp_const` in `maitreemody/eci_growth/data/derived/country_year.csv`).
- Horizon: **10 years** (primary). 5 years is used only in the specification curve.

## 2. Sample
- Countries with population ≥ 1M **and** goods exports ≥ $1B in the start year (as in `juliawang/project3_horse_race.py`, line 54).
- Merge on **ISO3** only.
- Complete cases across **all** measures in §4, so every measure is scored on the same countries in each origin.
- Report N_train and N_test for every origin.

## 3. Baselines (two pre-specified arms; both are reported)
| Arm | Controls (all measured at start year *t*) | Role |
|---|---|---|
| **A (primary)** | log GDPpc_t, natural-resource rents (% GDP)_t | Headline |
| **B (pre-specified robustness)** | A + resource export share_t (HS 26/27/71, from `willbetts/nightly/external-data/derived/score_panel.csv`; merge as in `willbetts/forecast-reconciliation/julia_plus_resource_share.py`) | Reported alongside A in the same table |

**Banned from every out-of-time model:** the Atlas decade-*change* in resource exports used in Project 1. It uses future information. It may appear only in Maitree's in-sample table, labelled "in-sample only".

## 4. Measures (each added to the baseline one at a time)
`diversity, entropy, hhi, eci_hs4, eci_hs2, eci_groups18_goods, eci_groups17_goods, eci_hs4_matched17, eci_continuous, log_fitness200, log_fitness500, eci_harvard`, plus the `eci_hs4 + diversity` model. These are the scores already saved in `juliawang/outputs/project3/full/all_measures.csv`.

- **Converged Fitness** (`log_fitness_conv`) is added **only if** Aiden delivers it by Thu 11/19 at 12:00 in the same file format. Otherwise Fitness is reported as "unresolved: no annual network converged".
- **Sign check:** each ECI variant must correlate positively with diversity in every year. Flip and log any that don't.

## 5. Forecast design
- **Origins scored:** every start year **2005, 2006, …, 2014** (10 origins; 2014 + 10 = 2024 is the last available outcome year).
- **Training set for origin T:** all 10-year windows with start year s, where 1995 ≤ s and s + 10 ≤ T (an expanding window). Nothing that ends after T is used.
- **Estimation:** OLS; regressors standardized on training data only; centered training-period dummies (forecast effect = training average); SEs clustered by country.
- **Secondary designs** (reported, but they do not decide the answer): Julia's `primary_1998_2008` and her 3-origin set (2005/2008/2014).

## 6. Metrics and tests
For each measure × arm:
1. **Out-of-sample R² vs baseline (= MSE gain %):** `100 × (1 − MSE_model / MSE_baseline)`, pooled across all 10 origins, plus one value per origin.
2. **Origins won:** the number of the 10 origins with gain > 0.
3. **Clark–West test** (one-sided; the measure model nests the baseline), pooled across origins. Origins overlap, so the p-value comes from a **country-cluster bootstrap** (resample countries, keep all of each country's origins; 2,000 draws, seed 20261118).
4. **The same test vs diversity**: compare `eci_hs4 + diversity` with `diversity`, and `eci_hs4` with `diversity`, using a paired country-cluster bootstrap 95% CI of the MSE difference.
5. **Holm correction** across the 12 measures within each arm.
6. In-sample ΔR² and rank stability (from the existing `stability.csv`) are reported as extra columns.

## 7. Decision rule (fixed now, before new results)
- **"ECI earns its keep"** if, in **Arm A**, `eci_hs4` has a Holm-adjusted Clark–West p < 0.05 vs baseline, **and** its pooled gain over diversity has a 95% CI above zero, **and** its gain in **Arm B** is still positive.
- **"ECI ≈ diversity"** if ECI beats the baseline but the CI vs diversity includes zero.
- **"No forecast value"** if ECI does not beat the baseline in Arm A.
- If Arms A and B disagree, the headline is that the result depends on the resource control, and §6 (the specification curve) carries the paper.

## 8. Specification curve (Will, §6)
For `eci_hs4` and `diversity`, vary every combination of:
- resource control: none / rents / share / both;
- outcome units: const 2015 US$ / PPP;
- origins: all 2005–2014 / Julia's 3 / excluding 2009–2012;
- sample: all / excluding commodity exporters (resource share ≥ 25%);
- horizon: 5 / 10 years.

That is 4 × 2 × 3 × 2 × 2 = 96 specs per measure. Plot the pooled MSE gain sorted, with the Arm A and Arm B specs highlighted.

## 9. Out of scope (future work)
SITC extension back to 1962, ECI+, GENEPY, model confidence set, causal or fixed-effects designs (Project 4).

---

## Change log
- 2026-11-18: spec frozen (Will). Julia sign-off: ☐
