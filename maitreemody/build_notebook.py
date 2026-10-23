"""Builds exploration.ipynb. Run once: python3 build_notebook.py"""
import nbformat as nbf
c = []
md = lambda s: c.append(nbf.v4.new_markdown_cell(s))
code = lambda s: c.append(nbf.v4.new_code_cell(s))

md("""# Maitree Mody — ECI versus GDP per capita

**Research question: Do countries with higher ECI have higher GDP per capita?**

This is the central empirical claim behind ECI (Hidalgo & Hausmann 2009; *Atlas of Economic Complexity*): complexity is strongly correlated with income, and natural-resource exporters sit above the line. So this is a **validation check**, not a new finding. The question here: does the lab's own ECI reproduce the pattern?

We compare four country measures against log GDP per capita (PPP, constant 2021 international $, World Bank `NY.GDP.PCAP.PP.KD`):

1. **ECI, HS4 products**: about 1,220 HS 4-digit products built from `data/raw/<year>_mega.csv`. Closest to Harvard's method.
2. **ECI, 17 groups**: the lab's cleaned industry groups (`data/cleaned/<year>clean.csv`) without the overlapping High-complexity Products group, sign fixed.
3. **ECI, lab notebook as-is**: replicates `compute_eci` in `code/current/Spring2026.ipynb`.
4. **Diversity**: number of HS4 products with RCA ≥ 1. A simple benchmark: does ECI add anything beyond counting products?

## Method

Countries with ≥ $1B goods exports. Aggregates (EU-28, "nes" areas) removed. Taiwan is kept (Comtrade code 490). The World Bank doesn't cover Taiwan, so it drops at the merge. Primary year: 2019. 2020–2022 are repeats, and 2023 is shown only for completeness (its raw exports are inflated, `docs/KNOWN-ISSUES.md` D1). Regressions use HC1 robust standard errors.""")

code("""from pathlib import Path
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display, Markdown
HERE = Path.cwd()
sys.path.insert(0, str(HERE))
from analyze import run
d = run()""")

md("""## 1. Does higher ECI go with higher income?

Spearman correlation compares country rankings, by year and measure.""")
code("""corr = pd.read_csv(HERE / 'outputs/correlations.csv')
display(corr.pivot(index='measure', columns='year', values='spearman_rho').round(2))""")

md("""## 2. Picture (2019)

Left: product-level ECI. Right: the lab's 17-group ECI. Red = resource-dependent (≥ 40% of exports are ores, fuels, or precious stones/metals).""")
code("""s = d.loc[2019].dropna(subset=['eci_hs4', 'eci_grp', 'log_gdppc'])
fig, axes = plt.subplots(1, 2, figsize=(13, 5.2), sharey=True)
for ax, col, title in [(axes[0], 'eci_hs4', 'ECI from HS4 products'), (axes[1], 'eci_grp', 'ECI from 17 lab groups')]:
    for dep, color, label in [(0, '#187e9b', 'other'), (1, '#d1495b', 'resource-dependent')]:
        t = s[s.resource_dep == dep]
        ax.scatter(t[col], t.log_gdppc, s=18, alpha=.7, color=color, label=label)
    b = np.polyfit(s[col], s.log_gdppc, 1); xs = np.linspace(s[col].min(), s[col].max(), 2)
    ax.plot(xs, np.polyval(b, xs), color='black', lw=1)
    rho = s[col].corr(s.log_gdppc, method='spearman')
    ax.set(title=f'{title}  (Spearman ρ = {rho:.2f}, n = {len(s)})', xlabel='ECI, 2019')
    for name in ['Qatar', 'Norway', 'Australia', 'United Arab Emirates', 'Japan', 'Philippines', 'India', 'Congo, Dem. Rep.']:
        if name in s.index:
            ax.annotate(name[:14], (s.loc[name, col], s.loc[name, 'log_gdppc']), fontsize=8, xytext=(3, 3), textcoords='offset points')
axes[0].set_ylabel('log GDP per capita, PPP (2019)'); axes[0].legend(frameon=False)
plt.tight_layout(); plt.savefig(HERE / 'outputs/2019_eci_vs_gdppc.png', dpi=130); plt.show()""")

md("""## 3. Regressions (2019)

- **A vs B:** how much income variation each ECI version explains.
- **C, D:** does ECI beat simple diversity?
- **E, F:** resource exports.

LOO RMSE = leave-one-country-out error in log points, a check of how well each model generalizes to a country it didn't see. It is **not** a forecast: ECI is computed from all countries jointly.""")
code("""display(pd.read_csv(HERE / 'outputs/regressions_2019.csv').fillna(''))""")

md("""## 4. Who departs from the line?

Residuals from model A (log GDP per capita ~ HS4 ECI). Positive = richer than complexity predicts.""")
code("""res = pd.read_csv(HERE / 'outputs/2019_residuals.csv', index_col=0)
display(res.tail(10)[::-1].round(2))
display(res.head(10).round(2))""")

md("""## 5. Same check on the lab notebook's ECI

The notebook's ECI correlates *negatively* with income in 2021 and 2023. Its sign is set by whichever country appears in the first row of the data file (`compute_eci`: `if vector[0] < 0`), so the whole ranking can flip from year to year. This is worth raising with the team before anyone uses notebook ECI for growth or income work.""")
code("""nb = corr[corr.measure.str.contains('notebook')].set_index('year')[['n', 'spearman_rho']].round(2)
display(nb)""")

md("""## 6. Results and limitations""")
code("""display(Markdown((HERE / 'outputs/findings.md').read_text()))""")

nb = nbf.v4.new_notebook(cells=c, metadata={'kernelspec': {'name': 'python3', 'display_name': 'Python 3', 'language': 'python'}})
nbf.write(nb, 'exploration.ipynb')
print('wrote exploration.ipynb')
