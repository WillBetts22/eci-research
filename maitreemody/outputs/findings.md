# ECI versus GDP per capita — findings

Question: Do countries with higher ECI have higher GDP per capita?

**Yes, when ECI is computed at the product level. Only weakly when it's computed on the lab's 17 industry groups.**

- **Product-level (HS4) ECI** has a Spearman correlation of 0.77–0.81 with log GDP per capita (PPP) in every year 2019–2023. In 2019 it alone explains 56% of cross-country variation in log income (n = 126). One standard deviation more ECI goes with about 2.2× higher GDP per capita (exp(0.79)).
- **The lab's 17-group ECI** (sign fixed) correlates only about 0.36–0.51 (depending on year and sample) and explains 8% (R² = 0.08). It does no better than simply counting products with RCA ≥ 1 (R² = 0.10).
- **The lab notebook's ECI as-is** correlates −0.47 with income in 2021 and −0.38 in 2023. That's the sign-convention problem, not an economic result.
- **ECI beats raw diversity.** Holding product-level ECI fixed, diversity enters negatively (model D). The information is in *which* products a country makes, not how many. This matches Mealy, Farmer & Teytelboym (2019).
- **Resource exporters are richer than their complexity predicts** (Qatar, Australia, UAE, Norway, Oman, Kazakhstan). Average residual +0.23 log points vs −0.11 for others. Adding resource share raises R² from 0.56 to 0.63. This is the known Atlas pattern (and why Harvard's growth projections control for natural-resource exports), reproduced here, not discovered.
- **Poorer than predicted:** mostly low-income African economies plus India and the Philippines. India and the Philippines have mid-range ECI but low income, the "complexity ahead of income" cases Harvard's framework predicts will grow faster. Testing that is a growth question, not this one.

## Interpretation and limits

- **Correlation, not causation.** Rich countries may become complex rather than the reverse, and both may be driven by institutions, human capital or geography. A cross-section can't tell these apart.
- **The 17-group result is mainly a measurement finding.** With 17 groups, the RCA matrix has too little detail to separate countries' capabilities. That matters for the lab's reports, which all use the grouped ECI.
- **Not Harvard's ECI.** The data is exporter-reported only (Harvard reconciles exporter and importer reports), uses whatever HS revision each country reported, has no population filter, and uses binary RCA (Harvard moved to a continuous measure in 2026). The HS4 top 6 in 2019 (Japan, Korea, Switzerland, Taiwan, Singapore, Germany) match Atlas 10.0's top six, which is reassuring but not a formal check.
- **Resource definition is crude.** HS chapters 26, 27 and 71 miss refined copper (ch. 74), so Zambia and DR Congo show low resource shares. The 40% cutoff is arbitrary. Residual patterns should be rechecked with a better definition.
- **2023 exports are inflated** in the raw pull (KNOWN-ISSUES D1). Its row is for completeness only.
- **Single cross-sections.** Years 2019–2023 aren't independent evidence: the same countries, with very persistent ECI.

## Next steps

1. Download Harvard's published ECI (Atlas data downloads) and correlate it with our HS4 ECI. A formal replication check.
2. Redo the resource definition (add ch. 74–81 refined metals) and see whether the resource residual pattern holds.
3. Panel version: within-country changes in ECI vs changes in income (country fixed effects). This moves toward the "complexity predicts growth" question.
4. Flag the notebook sign issue and the group-vs-product gap to the team.
