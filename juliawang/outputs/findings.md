# Diversification versus ECI — results

Question: Do more diversified countries always have higher ECI?

No, in this grouped local dataset, entropy and ECI do not give identical country orderings. In 2019, 2,491 of 7,021 country pairs have opposite strict orderings (entropy ties are not violations).

Fixed sample: 119 countries with positive recorded exports in every year, 2019–2023. The overlapping High-complexity Products group is excluded, leaving 17 groups. Zero entries are retained. This is a recomputed grouped-data ECI, not published Harvard ECI.

Entropy and RCA diversity each explain about 16% of ECI variation.
Concentration (HHI) explains about 11%.
Quadratic models offer little improvement and perform slightly worse in leave-one-country-out checks.

## Rank correlations (fixed country sample)

 year        metric  spearman_rho
 2019       entropy      0.412780
 2019 rca_diversity      0.404945
 2019           hhi     -0.333116
 2020       entropy      0.450847
 2020 rca_diversity      0.461438
 2020           hhi     -0.368851
 2021       entropy      0.467370
 2021 rca_diversity      0.450894
 2021           hhi     -0.417997
 2022       entropy      0.488050
 2022 rca_diversity      0.419264
 2022           hhi     -0.448554
 2023       entropy      0.458297
 2023 rca_diversity      0.430381
 2023           hhi     -0.408860

## Interpretation and limits

Entropy measures how evenly export value is distributed across groups. RCA diversity counts groups with RCA > 1. ECI also uses which groups other countries specialize in, so identical diversity counts need not imply identical ECI. The ECI eigenvector sign is oriented to correlate positively with RCA diversity by convention; the sign of that relationship is therefore not an independent finding.

This is descriptive evidence, not a test of causality, growth prediction, or the accuracy of either measure. Broad and potentially problematic industry mappings remain in the source data. Excluding the overlapping aggregate does not repair those mappings. Nominal prices affect shares. The repository flags 2023 totals as potentially anomalous; treat 2019 as primary and later years as sensitivity checks. Fixed country coverage improves comparability but ECI is still standardized separately each year. Available-sample results are saved separately. No country-name harmonization is applied to the fixed-sample intersection.

See correlations.csv, country metrics, and ordering violations for the underlying numbers. A small gap between the second and third eigenvalues can indicate sensitivity of ECI to perturbations; it is reported in correlations.csv.
