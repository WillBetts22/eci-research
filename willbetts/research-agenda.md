# Research Agenda: How Can We Improve the ECI?

Will Betts, started 2026-10-20. A working map of the questions we're asking and the avenues worth exploring under each. Each section ends with concrete starter tasks that can be done with the data already in this repo.

Related: `exploration.ipynb` (this folder), `docs/methodology.md` (the lab's ECI exactly as implemented), `docs/KNOWN-ISSUES.md`.

---

## 0. Why this matters for the lab specifically

Our country reports go beyond describing ECI. The greedy optimizer (`methodology.md` section 7) recommends how a country should allocate a budget so as to **maximize its ECI**. That recommendation is only sound if:

1. ECI predicts growth,
2. that relationship is at least partly **causal**, and
3. pushing exports into a given industry group actually moves the underlying capabilities ECI is meant to proxy, rather than just moving the index.

Every question below is ultimately a test of one of those three links.

---

## 1. How well does ECI predict growth, and is it causal?

### What the literature claims
- Hidalgo and Hausmann (2009) and the *Atlas of Economic Complexity* (2013): countries whose ECI is high relative to their income tend to grow faster over the following decade. ECI adds predictive power beyond GDP per capita, governance and education.
- The claim is about **10-year growth, controlling for initial income**. That design is different from what our reports do (5-year nominal GDP growth, no income control).

### Avenues
- **Replicate the headline result** with our pipeline: regress 10-year growth in GDP per capita on initial ECI plus log initial GDP per capita (convergence control). Does ECI survive? How does R^2 compare with income alone?
- **Horse race against simple baselines**: diversity alone (count of RCA>1 industries), export entropy (already in `exploration.ipynb`), natural-resource share, log GDP per capita. If a one-line diversity measure does as well as the eigenvector, that matters.
- **Correlation vs causation strategies**:
  - *Timing / Granger-style*: does ECI change lead GDP change, or the reverse?
  - *Within-country (fixed effects)*: does a country's ECI rising predict its own subsequent growth, or does ECI only separate rich from poor countries?
  - *Natural experiments*: trade shocks that change export structure for reasons unrelated to domestic growth (e.g. China's WTO entry, commodity price swings, sanctions, tariff changes). Event studies around these.
  - *Instruments*: geography-based or neighbor-based export shocks, though instrument validity will be hard to defend.
- **Reverse causality**: rich countries can afford to build complex industries. Initial-period ECI helps, but does not settle this.

Broken into four two-week projects in `ECI_growth_prediction.md`.

### Starter tasks
- [ ] Extend `exploration.ipynb`: compute the lab's ECI (port `compute_mcp` / `compute_eci`) for 2019 and regress 2019-2023 growth on it, next to entropy.
- [ ] Get longer history (see section 6) to do a proper 10-year test.

**What we found so far:** with 2019 data, export entropy has a weak, non-significant relationship with 2019-2023 nominal growth (p ~ 0.12, R^2 ~ 0.03). Short windows are dominated by commodity prices and exchange rates (Libya, Nigeria, Guyana are the outliers).

---

## 2. If ECI is mostly correlation, what are the underlying causal variables?

ECI is supposed to be a proxy for unobserved **capabilities** (know-how, institutions, infrastructure, skills). Candidate observables to test directly:

| Capability | Possible measures |
|---|---|
| Human capital | years of schooling, tertiary enrollment, PISA scores |
| Know-how / innovation | patents per capita, R&D spending, scientific publications |
| Institutions | rule of law, regulatory quality (World Governance Indicators) |
| Infrastructure | electricity access, logistics performance index, internet penetration |
| Finance | private credit / GDP, FDI inflows |
| Network position | participation in global value chains (OECD TiVA), distance to large markets |

### Avenues
- **Mediation**: if ECI's predictive power disappears once these are controlled for, ECI is a summary of them, not an independent driver.
- **Decomposition**: regress ECI on the capability variables. What share is explained? The residual is what is "new" about ECI.
- **Multidimensional complexity**: recent work computes complexity from patents and research output as well as trade (Stojkoski et al., 2023). Trade-only ECI may miss capabilities that don't show up in exports.

### Starter tasks
- [ ] Pull World Bank WDI indicators (education, R&D, governance) for 2019 and check which ones absorb ECI's predictive power.

---

## 3. What assumptions does ECI make, and do we still agree with them?

### Assumptions in the standard ECI
1. **Exports reveal capabilities.** Only goods a country exports competitively count. Domestic production, non-traded services and the informal sector are invisible.
2. **Binary RCA.** Each country-product pair is in (M=1) or out (M=0), with RCA > 1 as the threshold. A country with RCA 0.99 is treated the same as one with RCA 0.
3. **Gross export value.** It ignores value added, so assembling imported components looks the same as making them from scratch.
4. **Equal weighting of products** after the RCA step. A tiny niche export counts as much as a giant one.
5. **The second eigenvector captures complexity.** Mealy, Farmer and Teytelboym (2019) show that ECI is mathematically equivalent to spectral clustering of countries by export similarity. It measures *how similar your export basket is to that of rich countries*, which is not obviously the same as "capabilities".
6. **Relative, re-standardized every year.** ECI is not comparable across years or country sets (see KNOWN-ISSUES D2/D3).
7. **Ignored variables**: population/size, product quality within a category, import composition, domestic demand, environmental cost, distribution of gains (inequality).

### Assumptions specific to the lab's implementation
These are as important as the textbook ones, and some are easy wins:
- **18 industry groups instead of roughly 1,200 HS4 products.** With 18 columns, the country-product network is tiny and the eigenvector is coarse. This is probably the largest gap between our numbers and published ECI.
- **"High-complexity Products" is a group defined *by* complexity** and overlaps other groups (methodology table). Putting it in the input to a complexity calculation is circular and double-counts trade (possibly related to KNOWN-ISSUES D1, the $45T 2023 total).
- **HS-chapter mapping issues** (KNOWN-ISSUES D4: chapter 84 machinery only appears in the aggregate group; chapter 85 electrical machinery sits in Transportation).
- **Countries with any zero are dropped** (D2), so the country set and therefore everyone's ECI shift year to year.
- **Nominal GDP, levels not per capita**, and the growth average is understated (N1). The United States is also missing from `GDP_2023.csv`.
- **The optimizer treats ECI as the objective.** That builds in the causal assumption from section 1.

### Discussion questions for the group
- Which of these do we disagree with *now*, and which will become worse over time (services, digital trade, value chains)?
- Is "similar to rich countries' exports" a goal we want to recommend, or a description?

---

## 4. Modifications and new variables

### Changes to the existing method
- **Finer product granularity**: compute ECI at HS4 (about 1,200 products) and aggregate to our 18 groups only for presentation. Compare rankings with the 18-group version.
- **Drop the circular aggregate group** and rerun. How much does ECI move?
- **Continuous instead of binary RCA**: use log RCA or RCA capped at a value, rather than a 0/1 threshold.
- **Population-adjusted RCA** (Atlas uses a per-capita variant for small/large countries).
- **Fixed country panel**: compute ECI on a constant set of countries so it is comparable over time.
- **Fitness-Complexity algorithm** (Tacchella et al., 2012): a nonlinear alternative where a product's complexity is set by the *least* capable country that exports it. Often argued to be better at prediction.
- **ECI+** (Albeaik et al., 2017): corrects for how hard it is to export each product. Already in our reference list.

### Variables we might add
- **Services trade** (growing share of world trade; our data includes some).
- **Value-added trade** (OECD TiVA): credit countries for the value they actually add.
- **Product quality / unit values** within categories (German cars vs. budget cars are the same HS code).
- **Patents and research** (multidimensional complexity).
- **Green / sustainability dimension**: complexity of "green" products as a separate index.
- **Resilience**: concentration of export destinations, not just products.
- **Inclusiveness**: link to inequality (Hartmann et al., 2017 found ECI is associated with lower inequality).

### Better data sources

| Concept | Current source | Alternatives |
|---|---|---|
| Trade | UN Comtrade, 18 groups, 2019-2023 | Harvard Atlas / Growth Lab (HS4 from 1995, SITC from 1962), CEPII BACI (reconciled mirror data), OEC |
| Income | World Bank GDP, current US$ | Penn World Table (real, PPP-adjusted GDP per capita), WDI GDP per capita constant US$ |
| Value added | none | OECD TiVA, WIOD |
| Capabilities | none | WDI, WIPO patents, Scimago publications, WGI |

---

## 5. Testing improvements without overfitting to past trade regimes

The risk: we try ten variants, keep whichever fits 1995-2020 best, and call it an improvement.

### Avenues
- **Out-of-time validation**: develop on early decades, then test once on a held-out later period (e.g. build on 1995-2010, test on 2010-2023).
- **Rolling-origin evaluation**: repeatedly predict the next 5/10 years using only data available at the time.
- **Out-of-sample by region or income group**: does an improvement hold when trained without Asia, or without commodity exporters?
- **Pre-commit to the evaluation metric and baselines** before trying variants (write them in this doc first).
- **Penalize complexity**: a variant with more tuning knobs needs to beat the standard ECI by more.
- **Report all variants tried**, not just the winner.

---

## 6. How are modern and future conditions different from the past?

The ECI was developed on trade data from roughly 1960-2010. Things that have changed or are changing:

- **Services and digital trade** are a growing share of value and are poorly measured by goods data.
- **Global value chains**: countries specialize in *tasks* (assembly, design) rather than whole products, so gross exports misrepresent capabilities.
- **Geopolitics**: tariffs, reshoring, "friend-shoring", sanctions and export controls (e.g. semiconductors) change which industries are open to which countries.
- **Energy transition**: demand for fossil fuels vs. critical minerals and green manufacturing.
- **Automation and AI** may weaken the old path of using labor-intensive manufacturing as a stepping stone.
- **China's scale** distorts the network: one country's entry into a product changes that product's ubiquity for everyone.

Question for the group: which of these would show up in historical data, so we could test for them, and which are new enough that only simulation can address them?

---

## 7. Backtesting on historical data vs. simulating the future

| | Backtesting (historical, possibly augmented) | Simulation |
|---|---|---|
| Strength | Grounded in what actually happened; standard in the literature | Can explore regimes that have never happened (AI, deglobalization) |
| Weakness | Past regimes may not repeat; limited number of independent episodes | Results depend entirely on the assumptions we build in |
| Data | Atlas SITC back to 1962 gives about 60 years | Agent-based or network-growth models of countries acquiring products |

### Avenues
- **Backtest first** to establish whether a variant has any value at all.
- **Augmented history**: apply modern adjustments (value added, services) where data allow, and see if conclusions change.
- **Stress-test via simulation**: e.g. remove a large exporter (simulating sanctions or decoupling) and check how stable ECI rankings and our greedy recommendations are. Our existing sensitivity analysis (methodology section 8) is a starting point.
- **Validate the greedy optimizer historically**: did countries that, in hindsight, moved in the direction our optimizer would have recommended, grow faster? This is close to what SOI tries to measure (section 9 of methodology), but SOI is currently flagged as unverified (KNOWN-ISSUES N3).

---

## 8. Side project: visuals for the website

The pre-reading mentions making interactive visuals instead of a paper. Possible pieces using our data:
- Interactive product space for the 18 groups (proximity network from `compute_proximity`).
- A country's ECI path over time with peers.
- Bubble chart of diversification vs. growth (prototype already in `exploration.ipynb`).

---

## Suggested order of work

1. Port the lab's ECI into `exploration.ipynb` and reproduce a few published report numbers (sanity check).
2. Quick wins on our own implementation: drop the circular aggregate, fix the country panel, use GDP per capita. Measure how much each moves ECI.
3. Get HS4 / long-history data (Atlas or BACI) and replicate the standard growth-prediction result.
4. Causality and mediation tests (sections 1-2).
5. Try one or two modifications (Fitness, continuous RCA) under the pre-registered evaluation from section 5.

## Open questions / notes
- Pre-reading links (video, website, abstract) were not included in the copy I have; add them here.
-

## References
- Hidalgo, C. A., & Hausmann, R. (2009). The building blocks of economic complexity. *PNAS* 106(26).
- Hausmann, R., Hidalgo, C. A., et al. (2013). *The Atlas of Economic Complexity*. MIT Press.
- Tacchella, A., Cristelli, M., Caldarelli, G., Gabrielli, A., & Pietronero, L. (2012). A new metrics for countries' fitness and products' complexity. *Scientific Reports* 2.
- Albeaik, S., Kaltenberg, M., Alsaleh, M., & Hidalgo, C. A. (2017). Improving the economic complexity index. arXiv:1707.05826.
- Hartmann, D., Guevara, M. R., Jara-Figueroa, C., Aristarán, M., & Hidalgo, C. A. (2017). Linking economic complexity, institutions, and income inequality. *World Development* 93.
- Mealy, P., Farmer, J. D., & Teytelboym, A. (2019). Interpreting economic complexity. *Science Advances* 5(1).
- Stojkoski, V., Koch, P., & Hidalgo, C. A. (2023). Multidimensional economic complexity and inclusive green growth. *Communications Earth & Environment* 4.
- Hidalgo, C. A., & Stojkoski, V. (2025). The Theory of Economic Complexity. arXiv:2506.18829.
