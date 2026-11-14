# Project 3 paper plan: horse race of complexity measures

Research PM draft, 2026-11-14. **Writing session: Friday 2026-11-20.**
Question (from `willbetts/ECI_growth_prediction.md`, Project 3): *Is ECI the best predictor of growth, or do simpler or alternative measures do as well? And how does the lab's own 18-group ECI compare?*

---

## 1. Where we are: what Julia and Will have already shown

### Settled: both agree, and the paper can state these
| Finding | Evidence |
|---|---|
| Our ECI code is correct | Julia: Pearson 0.920–0.963, rank 0.968–0.982 vs Harvard (`juliawang/outputs/project3/eci_validation.csv`). Will Q13: Spearman 0.975–0.985 on Growth Lab trade, 0.967–0.975 on our Comtrade pull |
| HS4 is the right granularity; the lab's 18 groups lose most of the signal | Will Q04: income R² is 0.58 at HS4, 0.33 at HS2 and 0.15–0.17 for the 18 groups; HS6 collapses (0.002). Julia: 18-group test RMSE 2.171 is worse than the baseline's 2.164; HS4 is 2.115 |
| Grouped ECI ranks are too noisy to use | Will Q09: Germany is ranked 2nd with a 90% interval of 1.5–55 under the groups, and 4–7 at HS4. Julia: minimum rank stability is 0.48 for the 17 groups vs 0.96 for HS4 |
| Continuous RCA and Fitness don't beat binary ECI | Julia: continuous RMSE 2.220, Fitness(200) 2.293. Will Q07/Q08/Q16: neither improves the out-of-time test |
| Overlap and coverage are separate problems for the grouped index | Julia: in 1998 the 18 groups sum to 117.8% of goods exports, and dropping the overlapping group cuts coverage to 84.2% |

### Contested: this is the paper's real question
**Does ECI improve out-of-time 10-year growth forecasts over income plus resources, and over plain diversity?**
- **Julia:** a small gain over the baseline (MSE improvement 4.5%), but the paired 95% interval spans zero ([-0.279, 0.755]). ECI vs diversity is not distinguishable ([-0.278, 0.456]). It beats the baseline in 7 of 8 designs.
- **Will (Q16):** every variant, including Harvard's published ECI, makes rolling forecasts *worse* (binary ECI −1.8%, Harvard −7.0%).
- **Reconciliation** (`willbetts/forecast-reconciliation/README.md`): neither person made a coding error. The gap comes from three specification choices, largest first:
  1. the **start-year resource export share** control, which correlates −0.32 to −0.66 with ECI;
  2. **which forecast origins are scored** (ECI loses in 2009–2012);
  3. constant US$ vs PPP outcomes.

  Going one step at a time from Will's spec to Julia's moves HS4 ECI from −1.8% to +4.8%.

**Implication for the paper:** don't pick a winner in advance. Make the specification dependence the headline, using a pre-registered primary spec plus a full **specification curve** across every defensible choice.

### Open gaps a robust paper needs to close
1. **One agreed primary spec**, fixed before anyone looks at new results.
2. **Proper forecast-comparison tests.** ECI models nest the baseline, so the right test is Clark–West, not a raw RMSE ranking. With about 12 measures we also need a multiple-comparison control, such as a model confidence set.
3. **More test decades.** Julia's HS data start in 1995. Maitree's SITC panel goes back to 1962, which allows more non-overlapping out-of-time origins.
4. **A converged Fitness.** In Julia's run no annual network converged. Will compared ranks only.
5. **Network vs diversity.** Does ECI add anything once diversity is in the model? This is the Mealy et al. (2019) question.
6. **The lab index we actually use**, including Will's Q05 HS84 fix, tested in the same horse race.
7. **A literature frame.** Albeaik et al. (2017, ECI+) and Hidalgo & Stojkoski (2025) are in `literature/`, and earlier forecasting horse races need to be summarized.

**Important design note for Monday.** The Atlas resource control that made Will's Project 1 replicate (`willbetts/project1/README.md`) is the *increase* in resource exports over the decade. That is future information, so it is valid in-sample but cannot be used in a true forecast. The paper should say this explicitly. It is probably why in-sample and out-of-time results disagree.

---

## 2. Proposed paper outline (for Friday)

Working title: *Does the Eigenvector Earn Its Keep? A Horse Race of Economic Complexity Measures for Growth*

| § | Section | Lead | Supporting |
|---|---|---|---|
| 1 | Introduction: why the lab cares (the reports maximize ECI) | Will | Towa |
| 2 | Related literature and earlier horse races | Towa | — |
| 3 | Data, measures, validation against Harvard | Julia | — |
| 4 | In-sample horse race (Atlas-style regression, one measure at a time) | Maitree | — |
| 5 | Out-of-time horse race, primary spec, with Clark–West tests and a confidence set | Julia | Will |
| 6 | Specification curve: why the answer depends on choices | Will | Julia |
| 7 | Alternative measures: converged Fitness, ECI+, rank stability | Aiden | Will (code review) |
| 8 | Granularity and the lab's 18-group index | Maitree | Aiden |
| 9 | Implications for the lab's reports and optimizer | Will | everyone |
| 10 | Limitations (no causal claim, which is Project 4; revised data; overlapping windows) | Julia | — |

---

## 3. This week's assignments

### Critical path, by Monday 11/16 evening: freeze the spec (Julia + Will, 1 hour)
Agree on a one-page `willbetts/project3/SPEC.md` covering:
- outcome: real GDP per capita (PPP), annualized over 10 years;
- baseline: log income, resource rents, and whether resource share is in the primary spec or a robustness arm;
- sample rule: population at least 1M and exports at least $1B, merged on ISO3;
- the list of measures;
- the scored origins;
- the metric: out-of-sample R² vs baseline, Clark–West, paired bootstrap.

**Everyone else runs on this spec**, so it has to come first. Suggested default: Julia's pipeline and samples, scoring *all* rolling origins 2005–2014 (Will's design), with resource share as a pre-specified second arm reported alongside.

### Julia: primary out-of-time horse race (§3, §5, §10)
- Starts from: `juliawang/project3_horse_race.py`, `outputs/project3/full/`
- Rerun every measure under the frozen spec.
- Add **Clark–West** tests vs baseline and vs diversity, plus a **model confidence set** (or a Holm correction) across measures.
- Deliver one master table, one row per measure: in-sample ΔR², out-of-sample R², folds won, CW p-value, rank stability.
- Write §3 from the existing data README and validation outputs.

### Will: specification curve and extended history (§1, §6, §9)
- Starts from: `willbetts/forecast-reconciliation/`, nightly Q16
- Turn the step-by-step reconciliation into a full **specification curve** for HS4 ECI and for diversity. Vary resource control (none / share / rents / both), units (const US$ / PPP), origins (all / Julia's 3 / excluding the commodity peak), sample (all / non-commodity) and horizon (5 / 10 years). Plot the ECI gain across every combination.
- Stretch: extend the out-of-time test with **SITC ECI from 1962** (Maitree's panel) to get more test decades.
- Draft §1 and §9 and own paper assembly (the LaTeX skeleton from `nightly/paper/`).

### Maitree: in-sample horse race and the lab's index (§4, §8)
- Starts from: `maitreemody/eci_growth/` panel, `willbetts/project1/` (Atlas resource control)
- Run the Project 1 regression swapping in each measure: diversity, entropy, HHI, HS4 / HS2 / Harvard ECI, Fitness, the 18 and 17 groups, and the **18 groups with the Q05 HS84 fix**. Report coefficient, R² gain and N, with the Atlas control and with resource rents.
- **Network vs diversity:** ECI and diversity in the same regression, plus ECI residualized on diversity.
- Build a forecast-setting granularity figure (out-of-sample R² vs number of products: 18 → HS2 → HS4), extending Julia's `granularity_comparison.png` and Will's Q04 ladder.

### Towa: literature and framing (§2, §1 support)
- Starts from: `literature/README.md`; the `/lit-review` workflow can draft entries in the lab's 3-question format.
- Write a **"previous horse races" table**: paper, measures compared, sample and years, outcome horizon, in-sample vs out-of-sample, who won. Must-cover: Hausmann et al. 2013 (Atlas), Tacchella et al. 2012/2018 (Fitness and forecasting), Albeaik et al. 2017 (ECI+), Mealy, Farmer & Teytelboym 2019, and Hidalgo & Stojkoski 2025. Verify each citation from the source.
- Identify which specs earlier papers used for the resource control and the forecast origins. That directly supports the Monday spec decision, so send early notes to Julia and Will by Monday.
- Draft §2 (about 1.5 pages).

### Aiden: alternative measures and stability (§7)
- Starts from: `willbetts/nightly/lib/eci.py`, nightly Q08/Q09 runs, `juliawang/outputs/project3/full/fitness_diagnostics.csv`. Pair with Will for a 30-minute code walkthrough on Sunday or Monday.
- **Fitness done properly:** implement a convergence-based stopping rule (ranks stable, values normalized each iteration) and report whether it converges per year. Feed the converged scores into Julia's horse race.
- **ECI+** (Albeaik et al. 2017) at HS4, if time allows. Coordinate with Towa on the exact formula.
- **Rank stability for every measure:** extend Will's Q09 bootstrap (90% rank intervals) to all measures, giving the "policy-target quality" column of the master table.

---

## 4. Calendar

| Day | Milestone | Who |
|---|---|---|
| Sun 11/15 | Everyone reads this plan, `ECI_growth_prediction.md` §Project 3, and the reconciliation README. Aiden + Will code walkthrough | all |
| **Mon 11/16** | **Spec frozen** (`SPEC.md`). Towa's early notes on earlier specs | Julia, Will, Towa |
| Wed 11/18 | Mid-week check-in (15 min): each person shows one first result. Flag surprises early | all |
| Thu 11/19 (evening) | **Code and numbers freeze.** Each person commits code, outputs and a **section packet** | all |
| **Fri 11/20** | **Writing session.** Merge packets into §1–10, reconcile any number conflicts, agree on the headline and abstract | all |

**What a section packet is:** a short `findings.md` in your folder containing:
- 3–5 bullet findings, with every number copied from saved output (lab rule: no number without an output file behind it);
- the table and figure files;
- a "what this does not show" line;
- the exact command to reproduce it.

Friday then becomes assembly and argument, not analysis.

---

## 5. Risks to watch
- **The spec slips past Monday.** Then everyone runs on different specs and we rebuild the Julia/Will disagreement five times over. Protect Monday.
- **Resource-control leakage.** Don't use the decade-change Atlas control in any out-of-time model.
- **Number conflicts on Friday.** Each number should have one owner: §5's numbers come from Julia's master table, and §6's from Will's curve.
- **Scope creep.** Causality and fixed effects belong to Project 4, not here. GENEPY and other measures go in "future work".
