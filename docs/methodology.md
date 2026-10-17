# Methodology

This page gives the formulas exactly as implemented in `code/current/Spring2026.ipynb`, with the cell number for each. For intuition, see [onboarding/01-what-is-eci.md](onboarding/01-what-is-eci.md).

Notation: $X_{cp}$ is the export value of country $c$ in industry group $p$ for one year (from `<year>clean.csv`).

## 1. Revealed comparative advantage (`compute_mcp`, #11)
$$M_{cp} = \begin{cases}1 & \text{if } \dfrac{X_{cp}}{\sum_p X_{cp}} > \dfrac{\sum_c X_{cp}}{\sum_{c,p} X_{cp}} \\ 0 & \text{otherwise}\end{cases}$$
In words: $M_{cp} = 1$ when industry $p$ makes up a larger share of country $c$'s exports than it does of world exports.

Diversity is $k_{c,0} = \sum_p M_{cp}$, and ubiquity is $k_{p,0} = \sum_c M_{cp}$.

## 2. ECI and PCI (`compute_mcc`, `compute_mpp`, `compute_eci`, `compute_pci`, #12–#15)
$$\tilde M_{cc'} = \sum_p \frac{M_{cp} M_{c'p}}{k_{c,0}\,k_{p,0}}, \qquad \tilde M_{pp'} = \sum_c \frac{M_{cp} M_{cp'}}{k_{c,0}\,k_{p,0}}$$
**ECI** is the eigenvector associated with the **second-largest** eigenvalue of $\tilde M_{cc'}$, standardized:
$$ECI_c = \frac{K_c - \langle K\rangle}{\operatorname{sd}(K)}$$
The sign is fixed by a convention in the code. **PCI** is the same calculation applied to $\tilde M_{pp'}$.

ECI is **relative**: it's re-standardized every year over whichever countries are in that year's data, so changes in country coverage move everyone's score (see [KNOWN-ISSUES D2/D3](KNOWN-ISSUES.md)).

## 3. Proximity and distance (`compute_proximity` #30, `compute_distance` #31)
$$\phi_{pp'} = \frac{\sum_c M_{cp} M_{cp'}}{\max(k_{p,0}, k_{p',0})}$$
$$d_{cp} = 1 - \frac{\sum_{p'\neq p} M_{cp'}\,\phi_{pp'}}{\sum_{p' \neq p} \phi_{pp'}}$$
Distance runs from 0 to 1. A low $d_{cp}$ means country $c$ already exports industries close to $p$.

## 4. Realized Industry Development (RID) (`compute_adi` #32)
$$RID_{cp} = d_{cp}^{\,\text{start}} - d_{cp}^{\,\text{end}}$$
The code computes `distance2 − distance` (later year minus earlier year) and reports it with sign conventions so that **positive RID = moved closer** to industry $p$. The report counts positive vs. negative RID groups (`[POS RID END]`, `[NEG RID END]`).

## 5. Opportunity gain → SDV (`compute_opportunity_gain` #38)
$$OG_{cp} = \sum_{p'} \frac{\phi_{pp'}}{\sum_{p''}\phi_{p''p'}}\,(1 - M_{cp'})\,PCI_{p'} \;-\; (1 - d_{cp})\,PCI_p, \qquad OG_{cp} = 0 \text{ if } M_{cp}=1$$
The **Suggested Development Vector (SDV)** is industries ranked by $OG_{cp}$. Report colouring: dark blue for positive, light blue for zero, white for negative.

Marginal opportunity gain (#39) scales $OG$ by the export increase needed to reach $M_{cp}=1$.

## 6. Sequential strategy (SIDS) (`main()` in SDV & SIDS)
Repeatedly raise exports in the industry with the best opportunity gain until it reaches RCA, then recompute everything. The outputs `sdv_and_sids<Country>.txt` / `sequential vector of <Country>.xls` list the "Before Iteration" opportunity gains and each step ("increase Textile in China by 15,404,927 USD").

## 7. Budgeted greedy allocation (`two_step_greedy` #64)
Hypothetical budget $B = s \cdot \sum_p X_{cp}$ for $s \in \{5, 10, 15, 20\}\%$, split into $n \in \{30, 60, 90, 120\}$ equal parts. Each part goes to the industry that maximizes ECI **two steps ahead**. This lookahead is a heuristic for the non-convex problem
$$\max_{x \ge 0,\ \sum x_p \le B} ECI_c(X + x)$$
Any surplus goes to the industry with the smallest required increase. Outputs are pickles of `(allocation, ECI path, ECI increments)`, which feed the pie charts, the ECI-increment chart, and the portfolio table.

## 8. Sensitivity & contingency (Section 4)
- **ECI sensitivity:** shock each industry's exports by ±x% (all else equal) and recompute ECI. The result is the positive and negative shocking charts (Figures 6a/6b). The most sensitive industries become `[Industry 4–6]`.
- **SDV sensitivity:** how the SDV ranking changes under shocks to *High-complexity Products* and *Clothing and Accessories*
- **Contingency (`cont`)**: which industries to fall back on if a key industry is shocked

## 9. Structural Optimality Index (SOI) (#42–#46, "SOI w/ ADI")
For each country, regress realized movement (ADI/RID, or the export change) on opportunity gain across the 18 industries:
$$\text{RID}_{cp} = \alpha + \beta\, OG_{cp} + \varepsilon \quad\Rightarrow\quad SOI_c = \text{signed adj. } R^2$$
A high SOI means the country moved toward the industries the model recommended. Across countries, we regress 5-year GDP growth on SOI (Figure 9), and place the country in an SOI quartile (Figure 10).  See [KNOWN-ISSUES N3](KNOWN-ISSUES.md).

## 10. GDP growth (`aagrate` #20)
The average of year-over-year % changes.  See [KNOWN-ISSUES N1](KNOWN-ISSUES.md). Quality thresholds (main country): > 3% is `high`, > 1% is `moderate`, otherwise `low`. Relative quality is the country's percentile among its peers (> 66% → high, > 33% → moderate).

## Industry groups
18 groups built from HS 2-digit chapters (`code/data-retrieval/datacleaning2025.ipynb`):

| Group | HS chapters | Description (Table 1 of every report) |
|---|---|---|
| Animals and By-products | 1–5, 16 | All kinds of meat, livestock and related by-products |
| Vegetables, Fruits and Plants | 6–11, 13, 14 | Plants, edible vegetables and fruits |
| Food and Preparations | 12, 15, 17–24 | Edible preparations, raw cooking materials |
| Energy Drilling and Mining | 25–27 | Mining for energy, minerals, stone materials |
| Chemicals | 28, 29 | Raw chemical materials and by-products |
| Chemical Manufacturing | 30–35, 38 | Advanced chemical and pharmaceutical products |
| Raw Manufacturing | 37, 39–43, 46, 68, 69 | Basic products from plastic, rubber, leather, etc. |
| Wood Products | 44, 45, 47–49 | Book, paper and other wood products |
| Clothing and Accessories | 61–67 | Fabrics, filament, clothing and accessories |
| Textile | 50–60 | Textile articles |
| Metals | 72–82 | Raw metals |
| Machinery and Construction | 83 | Machinery and mechanical appliances (see KNOWN-ISSUES D4) |
| Transportation | 85–88, 98 | Vehicles, aircraft, ships, railway |
| Weapons | 36, 92 | Explosives, arms and ammunition |
| Daily Instruments | 89–91, 93–95 | Sport requisites, timing and measuring tools |
| Precious Stones | 70, 71 | Refined or processed stone, pearls, ceramics |
| High-complexity Products | 28–30, 38, 83, 84, 87, 92, 99 | **Aggregate** of the highest-PCI chapters (overlaps other groups by design) |
| Services and Utilities | 99 (+ Comtrade services EB02) | Financial, business, legal, communication, travel |

## References
- Hidalgo, C. A., & Hausmann, R. (2009). The building blocks of economic complexity. *PNAS* 106(26).
- Hausmann, R., Hidalgo, C. A., et al. (2013). *The Atlas of Economic Complexity*. MIT Press.
- Albeaik, S., Kaltenberg, M., Alsaleh, M., & Hidalgo, C. A. (2017). Improving the economic complexity index. arXiv:1707.05826.
- Hidalgo, C. A., & Stojkoski, V. (2025). The Theory of Economic Complexity. arXiv:2506.18829.
- The full reference list used in reports is at the end of `templates/Auto Report Template.docx`.
