"""Q03 - Fixed country panel vs per-year sample (D2/D3).

Pre-stated metric: year-to-year Spearman rank stability (on countries present in both years)
and the 2020->2021 mean ECI change of the Spring 2026 report countries.
Baseline: the notebook as-is (per-year sample, unoriented sign).
Variants: (a) per-year sample, sign oriented; (b) balanced panel (countries passing the
zero filter in all 5 years), oriented; (c) open rules (no zero filter, RCA>=1), per-year;
(d) HS4 per-year vs HS4 balanced panel (repo data).
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
YEARS = [2019, 2020, 2021, 2022, 2023]
res = {'years': YEARS}

# notebook-as-is ECI keyed to ISO3 (computed on name-indexed data so the row-0 sign rule is faithful)
nb, per, cov = {}, {}, {}
for y in YEARS:
    g = eci.load_groups(y, notebook_names=False)
    iso = eci.group_name_to_iso3(g.index)
    s = eci.notebook_eci(g)
    s.index = [iso[n] if iso[n] else ('EU28' if 'EU' in n else n) for n in s.index]
    nb[y] = s
    e, _ = R.grouped_eci(y)
    per[y] = e
    cov[y] = {'rows_in_csv': int(len(g)), 'pass_zero_filter': int(len(e))}
res['coverage'] = cov
panel_set = sorted(set.intersection(*[set(per[y].index) for y in YEARS]))
res['balanced_panel_n'] = len(panel_set)
panel = {}
for y in YEARS:
    X = R.lab_groups_iso3(y).loc[panel_set]
    panel[y], _ = R.grouped_eci(y, X=X)
open_ = {y: R.grouped_eci(y, lab_rules=False)[0] for y in YEARS}
res['open_rules_n'] = {y: int(len(open_[y])) for y in YEARS}

def stability(d):
    out = {}
    for a, b in zip(YEARS[:-1], YEARS[1:]):
        r, n = R.spearman(d[a], d[b]); out[f'{a}-{b}'] = {'rho': r, 'n': n}
    return out
res['stability'] = {'notebook (as-is)': stability(nb), 'per-year, oriented': stability(per),
                    'balanced panel, oriented': stability(panel), 'open rules, oriented': stability(open_)}
res['per_vs_panel_spearman'] = {y: R.spearman(per[y], panel[y])[0] for y in YEARS}

# D3: mean ECI change 2020->2021 of panel countries and report countries
def mean_change(d, idx, a=2020, b=2021):
    idx = [i for i in idx if i in d[a].index and i in d[b].index]
    return float((d[b][idx] - d[a][idx]).mean()), len(idx)
rc = list(R.REPORT_COUNTRIES)
res['d3_mean_change_2020_2021'] = {
    name: {'panel_countries': mean_change(d, panel_set)[0], 'report_countries': mean_change(d, rc)[0],
           'report_n': mean_change(d, rc)[1]}
    for name, d in [('notebook (as-is)', nb), ('per-year, oriented', per), ('balanced panel, oriented', panel)]}
# share of countries whose sign flips between 2020 and 2021 under each
def sign_flip_share(d, a=2020, b=2021):
    idx = d[a].index.intersection(d[b].index)
    return float((np.sign(d[a][idx]) != np.sign(d[b][idx])).mean())
res['sign_flip_share_2020_2021'] = {'notebook (as-is)': sign_flip_share(nb), 'per-year, oriented': sign_flip_share(per),
                                    'balanced panel, oriented': sign_flip_share(panel)}
# which report countries ever drop out
res['report_country_years_missing'] = {c: [y for y in YEARS if c not in per[y].index] for c in rc}
res['philippines_years_missing_lab'] = [y for y in YEARS if 'PHL' not in per[y].index]
res['philippines_years_missing_open'] = [y for y in YEARS if 'PHL' not in open_[y].index]

# HS4 per-year vs balanced panel
hs4 = {y: R.repo_hs(y, 4) for y in YEARS}
hs_per = {y: eci.eci_from_exports(hs4[y]) for y in YEARS}
hset = sorted(set.intersection(*[set(hs_per[y].index) for y in YEARS]))
hs_pan = {y: eci.eci_from_exports(hs4[y].loc[hset]) for y in YEARS}
res['hs4_panel_n'] = len(hset)
res['hs4_n_per_year'] = {y: int(len(hs_per[y])) for y in YEARS}
res['stability']['HS4 per-year'] = stability(hs_per)
res['stability']['HS4 balanced panel'] = stability(hs_pan)

summ = pd.DataFrame({k: [v[f'{a}-{b}']['rho'] for a, b in zip(YEARS[:-1], YEARS[1:])] for k, v in res['stability'].items()},
                    index=[f'{a}-{b}' for a, b in zip(YEARS[:-1], YEARS[1:])])
summ.to_csv(HERE / 'figures' / 'stability.csv')
res['mean_stability'] = summ.mean().to_dict()
res['mean_stability_excl_2023'] = summ.iloc[:3].mean().to_dict()

fig, axes = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
for ax, (name, d) in zip(axes, [('Notebook as-is', nb), ('Per-year, sign oriented', per), ('Balanced panel, oriented', panel)]):
    for c in rc:
        ys = [y for y in YEARS if c in d[y].index]
        ax.plot(ys, [d[y][c] for y in ys], marker='o', label=R.REPORT_COUNTRIES[c])
    ax.set_title(name); ax.axvspan(2020.5, 2021.5, color='grey', alpha=.15); ax.set_xticks(YEARS)
axes[0].set_ylabel('grouped ECI (z-score)'); axes[2].legend(fontsize=7, loc='lower right')
fig.tight_layout(); fig.savefig(HERE / 'figures' / 'report_country_paths.png', dpi=110)
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
print(summ.round(3)); print(res['d3_mean_change_2020_2021']); print(res['coverage'], res['balanced_panel_n'])
