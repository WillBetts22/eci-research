# Nightly Research Queue

Will owns this file. The nightly agent takes the **highest question that no run folder in `runs/` (on `main` or an open nightly PR) has claimed yet**. To steer it, reorder, add, or delete questions on `main`. New ideas from the agent land in `proposals/`. Promote the good ones here.

Tags: `repo-data` = doable with data already in the repo. `needs-data` = blocked until external data is added (see `data-requests/`).

## Phase A: Foundations and quick wins on our own implementation (agenda section 3)

- **Q01 — Shared ECI library + reproduction check** `repo-data`
  Port the lab's `compute_mcp` / `compute_eci` from `code/current/Spring2026.ipynb` into `willbetts/nightly/lib/eci.py`, with a sign fix (orient to diversity). Add an HS4 ECI builder from `data/raw`. Check that it reproduces the grouped ECI the notebook produces for a few countries and years, and Maitree's HS4 vs grouped income correlations. Everything after this builds on it.

- **Q02 — How much does the circular "High-complexity Products" group move ECI?** `repo-data`
  Grouped ECI with vs. without the aggregate, 2019–2023. Rank correlation, top movers, and the effect on the spring 2026 report countries (Canada, Germany, Poland, Singapore, UAE, UK, Vietnam) and their peers.

- **Q03 — Fixed country panel vs. per-year sample (D2/D3)** `repo-data`
  Is the 2020→2021 ECI drop an artifact of the changing country set? Compare per-year ECI against a fixed balanced panel, and measure year-to-year rank stability.

- **Q04 — Granularity ladder: 18 groups vs. HS2 vs. HS4** `repo-data`
  Which aggregation level is the minimum that recovers the ECI–log GDPpc relationship? Plot R² against the number of products. This tells us how far the lab's 18-group ECI is from a usable signal.

- **Q05 — Fix the HS-chapter mapping (D4) and re-measure** `repo-data`
  Remap chapters 84/85 (and anything else misfiled) per methodology Table 1, rebuild the grouped data in memory, and measure how ECI ranks change. Don't overwrite the cleaned CSVs.

- **Q06 — Where does 2023's $45T come from? (D1)** `repo-data`
  Reconcile `2023_mega.csv` totals against `2023clean.csv` and against 2019–2022, by reporter and by HS chapter. Identify the inflating reporters or chapters, and say whether it's a pull problem or a cleaning problem.

## Phase B: Method variants (agenda section 4), evaluated on income fit plus rank stability

- **Q07 — Continuous RCA vs. binary RCA** `repo-data`
  Binary RCA>1, log(1+RCA), capped RCA, and an RCA percentile, at HS4. Compare correlation with log GDPpc and stability across years.

- **Q08 — Fitness-Complexity (Tacchella et al., 2012) vs. ECI** `repo-data`
  Implement Fitness at HS4. Compare its correlation with log GDPpc, its year-to-year stability, and its rank disagreements with ECI.

- **Q09 — How fragile are ECI ranks? (eigengap and bootstrap)** `repo-data`
  Resample products or drop one country at a time. Compare rank confidence intervals for grouped vs. HS4 ECI, and report the eigengap for each year.

- **Q10 — Short-window growth test** `repo-data`
  Does 2019 HS4 ECI plus log GDPpc predict 2019–2023 real GDPpc growth (PPP, constant)? Compare against entropy, diversity, and the lab's grouped ECI. Five years is short, so treat this as a pilot for the 10-year test.

- **Q11 — Does the greedy optimizer's target change under HS4 ECI?** `repo-data`
  Without running greedy: compare, for each report country, which industry group gives the largest marginal ECI gain from a 5% export bump, under grouped ECI vs. HS4 ECI aggregated to groups.

## Phase C: Needs external data (agenda sections 1, 2, 5, 7)

- **Q12 — Replicate the Atlas 10-year growth regression** `needs-data` (Atlas ECI + PWT/WDI GDPpc and resource rents)
- **Q13 — Our HS4 ECI vs. Harvard's published ECI** `needs-data` (Atlas ECI 2019–2023)
- **Q14 — Mediation: does ECI survive education, R&D, and governance controls?** `needs-data` (WDI, WGI)
- **Q15 — Population-adjusted RCA** `needs-data` (population, which the WB extract may lack)
- **Q16 — Rolling-origin out-of-time evaluation of ECI variants** `needs-data` (Atlas HS4 trade, 1995+)
