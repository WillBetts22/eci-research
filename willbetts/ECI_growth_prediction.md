# ECI and Growth: Four Two-Week Projects

Will Betts, 2026-10-23. Breaks down Question 1 of `research-agenda.md`: **How well does ECI predict growth, and is the relationship causal?**

This is the question to tackle first. The lab's reports recommend budgets that **maximize a country's ECI**. That advice only makes sense if (a) ECI predicts growth and (b) raising ECI causes growth. Each project below tests a piece of that.

| # | Project | Core question | Type |
|---|---|---|---|
| 1 | Replicate the classic result | Does ECI predict 10-year growth, controlling for income? | Replication |
| 2 | Did the Atlas predictions come true? | How accurate were complexity-based forecasts made in the past, out of sample? | Out-of-sample test |
| 3 | Horse race of complexity measures | Does ECI beat simpler or alternative measures, including the lab's own 18-group ECI? | Model comparison |
| 4 | Causation: timing, fixed effects and mediators | Does ECI cause growth, or is it a proxy for something else? | Causal inference |

Projects 1 and 2 can start immediately. 3 and 4 reuse the dataset built in Project 1, so share it early (see "Shared setup").

---

## What we already know in this repo

Build on these; don't redo them.
- **Maitree (`maitreemody/`, branch `maitreemody/eci-vs-gdp-per-capita`)**: product-level (HS4) ECI from `data/raw/<year>_mega.csv` correlates about 0.8 with log GDP per capita. The lab's grouped ECI only reaches about 0.4. The lab notebook's `compute_eci` sign convention flips in some years. Also has a World Bank GDP-per-capita extract for 2019-2023.
- **Julia (`juliawang/`)**: diversification (entropy, RCA count) explains only about 16% of grouped ECI. Uses a fixed 119-country sample and drops the overlapping High-complexity aggregate.
- **Will (`willbetts/exploration.ipynb`)**: 2019 export entropy has a weak, non-significant link with 2019-2023 nominal GDP growth. Short windows are dominated by commodity prices.

**Key implication:** our local data covers only 2019-2023. That is far too short for growth prediction, since the literature uses 10-year growth. All four projects need **longer history** from outside the repo.

---

## Shared setup (day 1-2, do once, everyone uses it)

**Data to pull**

| What | Source | Notes |
|---|---|---|
| Published ECI, 1995 onward (HS) and 1962 onward (SITC) | Harvard Growth Lab, Atlas of Economic Complexity data on Harvard Dataverse | Use as the "official" ECI so we test the method, not our implementation |
| Country x product trade, HS4 | Same Dataverse (Atlas trade data), or CEPII BACI | Needed for Project 3 to compute our own variants |
| Real GDP per capita | Penn World Table (latest version) and/or World Bank WDI `NY.GDP.PCAP.PP.KD` | Use **real, per capita** growth, not nominal totals (unlike the lab notebook) |
| Natural resource rents (% GDP) | WDI `NY.GDP.TOTL.RT.ZS` | Standard control in the Atlas growth regressions |
| Population | PWT / WDI | For per-capita and for excluding very small countries |

Verify exact file names and versions on download, and record them (with download date) at the top of each notebook.

**Shared conventions** so results are comparable across projects:
- **Outcome**: annualized growth of real GDP per capita (PPP) over 10 years. Use 5 years as a robustness check.
- **Sample**: drop countries with population under 1 million or exports under $1B (the Atlas does something similar). Report sample size every time.
- **Country identifiers**: merge on ISO3 codes, never on names (see the name-matching pain in `exploration.ipynb` and KNOWN-ISSUES D6).
- **ECI sign**: always check that ECI correlates positively with diversity before using it (Maitree found the lab code can flip it).
- **Standard errors**: robust (HC1), clustered by country when pooling multiple decades.
- Save the merged panel as `willbetts/data/eci_growth_panel.csv` so Projects 3 and 4 start from the same file. If the raw files are large, don't commit them; commit the download script instead.

---

## Project 1: Replicate the classic result

**Question:** Does ECI predict a country's growth over the following decade, after controlling for how rich it already is?

**Why it matters:** this is the central empirical claim behind ECI (Hausmann, Hidalgo et al., *Atlas of Economic Complexity*, 2013). Before improving the index, confirm we can reproduce the result it rests on.

**Method**
1. Build a panel of decades: 1998-2008 and 2008-2018 for HS-era data. With SITC, extend back to the 1970s.
2. Baseline regression, one row per country-decade:
   `growth(t, t+10) ~ log GDPpc(t) + ECI(t) + natural resource exports(t) + decade fixed effects`
3. Variants: add `ECI x log GDPpc` (the Atlas finds ECI matters more for poorer countries); 5-year windows; single-decade cross sections.
4. Compare R^2 of income-only vs. income + ECI. The **increase in R^2 from adding ECI** is the headline number.

**Interesting extensions**
- Does the effect hold in every decade, or is it driven by one period (e.g. the 2000s commodity boom, the China-driven catch-up)?
- Does it hold by region and income group? Is it driven by East Asia?
- "ECI gap": countries whose ECI is high relative to their income (e.g. pre-2010 China, Vietnam). Did they grow fastest?

**Deliverable notebook:** replication table next to the original published coefficients; R^2 comparison; coefficient over time plot; findings section stating whether the result replicates and how robust it is.

**Week 1:** data pull and shared panel, baseline regression. **Week 2:** robustness by decade/region, write-up.

---

## Project 2: Did the Atlas predictions come true?

**Question:** Harvard has published growth projections based on complexity for over a decade. How accurate were they, judged on data that did not exist when they were made?

**Why it matters:** in-sample fit (Project 1) can be flattering. A forecast made in, say, 2013 for 2013-2023 is a genuine out-of-sample test, and the one that matters for the lab's forward-looking reports.

**Method**
1. Collect Harvard's published complexity rankings and growth projections from the Growth Lab (Atlas website / Dataverse "Growth Projections" files). Record which edition each projection came from.
2. Match each projection to realized growth over the projected period.
3. Score accuracy: correlation and rank correlation of predicted vs. actual, mean absolute error, share of countries placed in the right growth tercile.
4. **Benchmarks** the forecast has to beat:
   - naive: every country grows at the world average;
   - persistence: each country repeats its previous decade's growth;
   - convergence only: regression on log GDP per capita alone, fitted on data available at the time.
5. Rolling-origin version: refit the Project 1 regression using only data up to year T, predict T to T+10, repeat for several T.

**Interesting extensions**
- Which countries were the biggest misses, and why (conflict, commodity crashes, policy changes)?
- Are misses systematically related to oil dependence or to the pandemic?

**Deliverable notebook:** predicted vs. actual scatter with country labels; accuracy table against benchmarks; list of largest misses with short explanations; findings on whether complexity forecasts add value out of sample.

**Week 1:** gather projections and matching outcomes, scoring code. **Week 2:** rolling-origin refit, misses analysis, write-up.

---

## Project 3: Horse race of complexity measures

**Question:** Is ECI the best predictor of growth, or do simpler or alternative measures do as well? And how does the lab's own 18-group ECI compare?

**Why it matters:** if counting how many products a country exports competitively predicts growth as well as the eigenvector, the extra machinery adds little. And if the lab's 18-group ECI predicts poorly, our reports are building on a weak index (Maitree's results already suggest this for income levels).

**Measures to compare** (all computed from the same HS4 trade data, same countries, same years):
1. Diversity: number of products with RCA >= 1.
2. Export entropy and HHI (from `exploration.ipynb`).
3. Standard ECI, computed ourselves; check it matches Harvard's published ECI.
4. **Fitness** (Tacchella et al., 2012), a nonlinear alternative.
5. ECI from continuous RCA instead of a 0/1 threshold.
6. **The lab's 18-group ECI**: map HS4 to the lab's industry groups (`docs/methodology.md`), with and without the overlapping High-complexity aggregate.

**Method**
1. Same regression as Project 1, swapping in each measure in turn.
2. Score each on **out-of-sample** prediction: fit on 1998-2008, predict 2008-2018 (and the rolling-origin setup from Project 2 if available).
3. Report rank stability: how much does each measure reshuffle countries year to year? (Unstable measures make poor policy targets.)

**Interesting extensions**
- Does ECI's advantage come from the network structure or just from diversity? Test by including both in the same regression.
- Product granularity: ECI from HS2 (about 97 chapters) vs. HS4 (about 1,200 products) vs. the lab's 18 groups. Where does predictive power drop off?

**Deliverable notebook:** one table, one row per measure, with in-sample R^2, out-of-sample error and rank stability; a granularity plot; a findings section with a clear recommendation on which measure the lab should use.

**Week 1:** compute all measures, validate against Harvard's ECI. **Week 2:** horse race, granularity test, write-up.

---

## Project 4: Causation: timing, fixed effects and mediators

**Question:** Does ECI *cause* growth, or does it just tag countries that grow for other reasons (education, institutions, investment), or grow first and become complex afterwards?

**Why it matters:** this is the assumption behind the lab's optimizer. If rising ECI doesn't lead to growth within a country, "maximize your ECI" is the wrong advice.

**Three tests, from easiest to hardest**
1. **Timing (lead-lag):** does a change in ECI today predict growth later, and does growth today predict ECI later? Run both directions with lags of 1, 3 and 5 years. If growth predicts ECI as strongly as ECI predicts growth, reverse causality is a serious concern.
2. **Within-country (fixed effects):** add country fixed effects to the Project 1 regression. This asks whether a country grows faster *in periods after its own ECI rises*, not whether high-ECI countries grow faster than low-ECI ones. Many cross-country results weaken or disappear here; whether ECI's does is the key finding.
3. **Mediators and confounders:** add plausible underlying causes one at a time and watch the ECI coefficient:
   - human capital: years of schooling (Barro-Lee), tertiary enrollment;
   - institutions: World Governance Indicators;
   - investment / capital: investment share of GDP (PWT);
   - innovation: patents per capita, R&D spending.
   If the ECI coefficient falls toward zero, ECI is mostly summarizing these. If it holds up, it captures something they miss.

**Interesting extensions**
- **Coefficient stability** (Oster-style): how strong would an unobserved confounder need to be to explain away the ECI result?
- **Natural experiment (stretch goal):** use an external shock to export structure, such as China's 2001 WTO entry hitting competing exporters, and check whether the affected countries' ECI changes were followed by growth changes. Probably too big for two weeks, but scoping it would be valuable.

**Deliverable notebook:** lead-lag table in both directions; cross-section vs. fixed-effects comparison; a coefficient plot showing the ECI estimate as each control is added; a findings section stating plainly how far the evidence supports a causal reading.

**Week 1:** timing and fixed-effects tests on the shared panel; pull control variables. **Week 2:** mediator analysis, stretch scoping, write-up.

---

## Notebook template (all four projects)

Each notebook goes in its author's folder (e.g. `<name>/eci_growth_<project>.ipynb`) with this structure:
1. **Question and why it matters** (2-3 sentences).
2. **Data**: sources, versions, download dates, sample rules, final sample size.
3. **Method**: equations or short description; anything that differs from the shared conventions.
4. **Results**: tables and figures, each with one sentence saying what it shows.
5. **Robustness**: what changes when you vary the window, sample or controls.
6. **Findings**: 3-5 bullet points answering the question, including "what this does *not* show".
7. **Limitations and next steps.**

Numbers in the findings must come from notebook output, consistent with the lab's rule for reports.

## Two-week timeline

| When | Milestone |
|---|---|
| Day 1-2 | Shared data pull and panel (`eci_growth_panel.csv`) done; Project 2 projection files collected |
| End of week 1 | Check-in: each project shows its baseline result. Flag surprises (e.g. ECI doesn't replicate) early, since they change the others |
| Day 10-12 | Robustness and extensions |
| End of week 2 | Notebooks submitted with findings sections; short group discussion comparing answers |

## How the four answers fit together

- Projects 1 and 2 answer **"does ECI predict growth?"** (in sample, then out of sample).
- Project 3 answers **"is ECI the right measure, and is ours good enough?"**
- Project 4 answers **"is it causal?"**

Together they say whether the lab's recommendation to "maximize ECI" is supported and, if not, what to change. That feeds directly into Questions 2-4 of `research-agenda.md`.

## References
- Hidalgo, C. A., & Hausmann, R. (2009). The building blocks of economic complexity. *PNAS* 106(26).
- Hausmann, R., Hidalgo, C. A., et al. (2013). *The Atlas of Economic Complexity*. MIT Press.
- Tacchella, A., Cristelli, M., Caldarelli, G., Gabrielli, A., & Pietronero, L. (2012). A new metrics for countries' fitness and products' complexity. *Scientific Reports* 2.
- Mealy, P., Farmer, J. D., & Teytelboym, A. (2019). Interpreting economic complexity. *Science Advances* 5(1).
- Oster, E. (2019). Unobservable selection and coefficient stability. *Journal of Business & Economic Statistics* 37(2).
