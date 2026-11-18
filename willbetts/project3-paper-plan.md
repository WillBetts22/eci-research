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

**Important design note (now in SPEC §3).** The Atlas resource control that made Will's Project 1 replicate (`willbetts/project1/README.md`) is the *increase* in resource exports over the decade. That is future information, so it is valid in-sample but cannot be used in a true forecast. The paper should say this explicitly. It is probably why in-sample and out-of-time results disagree.

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

## 3. This week's to-dos (rewritten 2026-11-18): one each

**The spec is frozen:** [`willbetts/project3/SPEC.md`](project3/SPEC.md). Everyone runs on it. Its §7 decision rule decides the headline, so nobody picks a winner on Friday.

Each to-do ends in a **section packet**: `findings.md` in your folder with 3–5 findings (each number traced to a saved output file), the table or figure files, one "what this does not show" line, and the command that reproduces it.

| Who | The one to-do | Done when | Due |
|---|---|---|---|
| **Julia** | **Run the primary horse race under SPEC.md** (Arms A and B, all 10 origins 2005–2014, Clark–West with cluster bootstrap, Holm correction, ECI vs diversity CI) and apply the §7 decision rule. Start from `juliawang/project3_horse_race.py`; the Arm B merge is in `willbetts/forecast-reconciliation/julia_plus_resource_share.py`. | `juliawang/outputs/project3/spec/master_table.csv` (one row per measure × arm) + `findings.md` stating which §7 verdict holds | Thu 11/19, 18:00 |
| **Will** | **Build the specification curve** (SPEC §8: 96 specs × {eci_hs4, diversity}) and plot it with Arms A and B highlighted. Start from `willbetts/forecast-reconciliation/step_will_to_julia.py`. | `willbetts/project3/spec_curve.csv` + `spec_curve.png` + `findings.md` (share of specs where ECI > baseline and where ECI > diversity) | Thu 11/19, 18:00 |
| **Maitree** | **Run the in-sample horse race:** the Project 1 regression with each SPEC §4 measure swapped in, **plus** ECI and diversity together **plus** ECI residualized on diversity. Use Arm A controls; the Atlas decade-change control goes in a separate column labelled "in-sample only". | `maitreemody/project3/in_sample_table.csv` (coef, SE, ΔR², N per measure) + `findings.md` | Thu 11/19, 18:00 |
| **Towa** | **Write the "previous horse races" table:** Hausmann et al. 2013, Tacchella et al. 2012 and 2018, Albeaik et al. 2017, Mealy, Farmer & Teytelboym 2019, Hidalgo & Stojkoski 2025. Columns: measures compared, sample and years, horizon, in- vs out-of-sample, resource control used, winner. Check each one against the source; `/lit-review` can draft entries. | `literature/project3_horse_races.md` with the table + ~1.5-page §2 draft | Thu 11/19, 18:00 |
| **Aiden** | **Make Fitness converge:** normalize each iteration, stop when ranks are stable, and record per year whether it converged. Output in the `all_measures.csv` format (`iso3, year, log_fitness_conv`). Start from `willbetts/nightly/lib/eci.py` and `juliawang/outputs/project3/full/fitness_diagnostics.csv`. | `aiden/project3/fitness_converged.csv` (new folder) + per-year convergence log, **handed to Julia** | **Thu 11/19, 12:00** (Julia needs it for her run. If it's late, Fitness is reported as "unresolved") |

**Cut from this week** (moved to future work): SITC 1962 extension, ECI+, model confidence set, new granularity figure (reuse Julia's `granularity_comparison.png`), extended rank-stability bootstrap (reuse Julia's `stability.csv`).

---

## 4. Calendar (revised 2026-11-18)

| When | Milestone | Who |
|---|---|---|
| ~~Mon 11/16~~ | ~~Spec frozen~~ (slipped two days) | — |
| **Wed 11/18 (today)** | Check-in: **Julia signs off on SPEC.md** (or the two of you change it now and log it). Each person confirms their to-do and start file | all |
| **Thu 11/19, 12:00** | Aiden's converged Fitness goes to Julia | Aiden → Julia |
| **Thu 11/19, 18:00** | **Code and numbers freeze.** Packets committed | all |
| **Fri 11/20** | **Writing session.** Apply SPEC §7 to Julia's table; §5 numbers come only from Julia's master table, §6 only from Will's curve | all |

## 5. Risks to watch
- **Someone drifts from SPEC.md.** Any result not on the frozen spec goes in the robustness section, not the headline. Spec changes need Julia + Will and a change-log line.
- **Aiden's Fitness is late.** Julia runs without it at 12:00 Thursday. Don't hold the freeze for it.
- **Resource-control leakage.** Don't use the decade-change Atlas control in any out-of-time model.
- **Number conflicts on Friday.** Each number should have one owner: §5's numbers come from Julia's master table, and §6's from Will's curve.
- **Scope creep.** Causality and fixed effects belong to Project 4, not here. GENEPY and other measures go in "future work".
