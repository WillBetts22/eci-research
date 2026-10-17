# 01 · What is Economic Complexity? (plain-English version)

For the formulas, see [../methodology.md](../methodology.md). This page explains the intuition.

## The core idea
A country's prosperity depends on the **know-how** embedded in what it can make. Know-how is hard to measure directly, but trade data reveals it:
- **Diversity**: how many different things does a country export competitively?
- **Ubiquity**: how many countries export a given product?

A country that exports *many* things, including things *few* others can make (say, Japan with precision machinery), has a lot of know-how. A country that exports a few things that everyone exports (raw commodities) has less. The **ECI** turns this into a single score per country by iterating the diversity/ubiquity logic until it converges, which works out to an eigenvector calculation.

## Our lab's twist: 18 industry groups
Harvard's Atlas works with ~5,000 individual products. We aggregate HS-coded exports into **18 industry groups** (Animals and By-products, Metals, Machinery and Construction, High-complexity Products, Services and Utilities, …). That makes the results interpretable as *industry strategy* rather than product lists. It's also why our ECI values differ from the Atlas's.

## The questions each report answers
| Section | Question | Our tool |
|---|---|---|
| 2. Macroeconomic results | How did GDP and complexity change vs. peers? | GDP & ECI time series, 2019→latest year |
| 3.2 Realized Industry Development | Which industries did the country actually move toward? | **RID**: change in "distance" to each industry |
| 3.3 Regional comparison | How does that compare to leading and emerging economies? | RID tables |
| 4.1 Suggested Development Vector | Which industries *would* raise complexity most? | **Opportunity gain**, ranked = **SDV** |
| 4.2 Budgeted strategy | If exports grew by 5/10/15/20%, where should the money go? | **Two-step greedy** optimizer |
| 4.6 Sensitivity & contingency | Which industries move ECI most if shocked up/down? | **Sensitivity** shocks, contingency tables |
| 5. Macro-level predictions | Has the country followed the optimal path, and did it pay off? | **SOI** (Structural Optimality Index) vs. 5-year GDP growth |

## Glossary
| Term | Meaning |
|---|---|
| **RCA / Mcp** | Revealed Comparative Advantage. `Mcp = 1` if country *c* exports a larger share of industry *p* than the world does. |
| **ECI** | Economic Complexity Index. Standardized (mean 0, sd 1) across countries each year. Higher means more complex. |
| **PCI** | Product Complexity Index, the same idea applied to industries |
| **Proximity** | How often two industries are co-exported competitively. A high value means shared know-how. |
| **Distance** | How far a country is from an industry, given what it already exports. Ranges 0–1; lower is closer. |
| **RID** | Realized Industry Development: the change in distance between two years. Positive RID means the country moved *toward* that industry. |
| **ADI** | The notebook's name for the distance-change array behind RID |
| **Opportunity gain** | How much entering an industry would open up *other* complex industries nearby |
| **SDV** | Suggested Development Vector: industries ranked by opportunity gain |
| **SIDS** | Sequential industry development strategy. These are the `sdv_and_sids<Country>.txt` outputs listing step-by-step export increases. |
| **Greedy / budget allocation** | Splits a hypothetical export increase (5–20% of total exports) into 30–120 parts and assigns each part to whichever industry raises ECI most, looking two steps ahead |
| **SOI** | Structural Optimality Index: how well a country's actual export changes line up with its opportunity gains (regression R²). High SOI means it is following the "optimal" path. |
| **Comparable / peer countries** | Three countries the report compares against. Keep them the same as in the country's previous report. |
| **Category** | `developed` or `emerging`. It changes the wording and the GDP-growth thresholds. |

## Key readings
- Hausmann, Hidalgo et al., *The Atlas of Economic Complexity* (2013). The PDF is in [`docs/original-instructions/2020 Spring - Info & Templates/atlas_2013.pdf`](../original-instructions/2020%20Spring%20-%20Info%20%26%20Templates/atlas_2013.pdf)
- Hidalgo & Hausmann (2009), *The building blocks of economic complexity*, PNAS
- Hidalgo & Stojkoski (2025), *The Theory of Economic Complexity*, arXiv:2506.18829
- The lab's literature review: [`literature/`](../../literature/)
