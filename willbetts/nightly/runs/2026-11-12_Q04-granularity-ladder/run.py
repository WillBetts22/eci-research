"""Q04 - Granularity ladder: 18 groups vs HS sections vs HS2 vs HS4 vs HS6.

Pre-stated metric: R^2 of log GDPpc (WDI, PPP constant) on ECI, same country sample at every
level (reporters with >= $1B exports and GDP data). Baseline: the lab's 18-group ECI.
Also: random partitions of HS6 into k pseudo-products (10 seeds) to trace R^2 vs k.
2019 primary, 2021 as a check.
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
SECTIONS = {'I': range(1, 6), 'II': range(6, 15), 'III': [15], 'IV': range(16, 25), 'V': range(25, 28),
            'VI': range(28, 39), 'VII': [39, 40], 'VIII': range(41, 44), 'IX': range(44, 47), 'X': range(47, 50),
            'XI': range(50, 64), 'XII': range(64, 68), 'XIII': range(68, 71), 'XIV': [71], 'XV': range(72, 84),
            'XVI': [84, 85], 'XVII': range(86, 90), 'XVIII': range(90, 93), 'XIX': [93], 'XX': range(94, 97), 'XXI': [97]}
res = {}
for year in [2019, 2021]:
    hs6 = R.repo_hs(year, 6)
    countries = hs6.index.intersection(R.gdppc(year).index)
    hs6 = hs6.loc[countries]
    rows = []
    def add(level, k, X, rules='open'):
        X = X.loc[X.index.intersection(countries)]
        e = eci.eci_from_exports(X)
        r = R.r2_logincome(e, year)
        rows.append({'level': level, 'n_products': k, **r, 'max_abs_eci': float(e.abs().max()), 'max_abs_country': e.abs().idxmax()})
    for d in (2, 4, 6):
        X = hs6.T.groupby(hs6.columns.str[:d]).sum().T
        add(f'HS{d}', X.shape[1], X)
    ch = hs6.columns.str[:2].astype(int)
    sec = {c: s for s, chs in SECTIONS.items() for c in chs}
    Xs = hs6.T.groupby([sec.get(c, 'other') for c in ch]).sum().T
    add('HS sections', Xs.shape[1], Xs)
    # lab groups, both rule sets, restricted to the same countries where possible
    G = R.lab_groups_iso3(year, drop_eu=True)
    Gc = G.loc[G.index.intersection(countries)]
    add('lab 18 groups (open rules, same sample)', 18, Gc)
    e_lab, _ = R.grouped_eci(year, drop_eu=True)
    r = R.r2_logincome(e_lab.loc[e_lab.index.intersection(countries)], year)
    rows.append({'level': 'lab 18 groups (lab rules: zero filter + strict RCA)', 'n_products': 18, **r})
    # lab mapping rebuilt from raw (so chapter coverage is identical to HS levels)
    Xg = R.groups_from_raw(year, R.LAB_GROUPS).loc[lambda d: d.index.intersection(countries)]
    add('lab 18 groups rebuilt from raw', 18, Xg)
    # random partitions
    rng = np.random.default_rng(0)
    rand = []
    for k in [5, 10, 18, 30, 50, 100, 200, 500, 1000, 2000]:
        for s in range(10):
            lab = rng.integers(0, k, hs6.shape[1])
            X = hs6.T.groupby(lab).sum().T
            try:
                e = eci.eci_from_exports(X)
                rand.append({'k': k, 'seed': s, **R.r2_logincome(e, year)})
            except Exception as ex:
                rand.append({'k': k, 'seed': s, 'r2': np.nan})
    rand = pd.DataFrame(rand)
    rsum = rand.groupby('k').r2.agg(['mean', 'min', 'max']).reset_index()
    ladder = pd.DataFrame(rows)
    ladder.to_csv(HERE / 'figures' / f'ladder_{year}.csv', index=False)
    rsum.to_csv(HERE / 'figures' / f'random_partitions_{year}.csv', index=False)
    hs4_r2 = ladder.set_index('level').loc['HS4', 'r2']
    first_90 = rsum.loc[rsum['mean'] >= 0.9 * hs4_r2, 'k']
    res[year] = {'ladder': ladder.to_dict('records'), 'random': rsum.to_dict('records'),
                 'n_countries': int(len(countries)),
                 'min_k_random_reaching_90pct_of_hs4_r2': int(first_90.min()) if len(first_90) else None}
    if year == 2019:
        fig, ax = plt.subplots(figsize=(6.5, 4))
        ax.fill_between(rsum.k, rsum['min'], rsum['max'], alpha=.2, label='random HS6 partitions (range, 10 seeds)')
        ax.plot(rsum.k, rsum['mean'], 'o-', label='random partitions (mean)')
        for _, r in ladder.iterrows():
            if r.level in ('HS2', 'HS4', 'HS6', 'HS sections', 'lab 18 groups (lab rules: zero filter + strict RCA)', 'lab 18 groups rebuilt from raw'):
                ax.scatter(r.n_products, r.r2, marker='s', zorder=5)
                ax.annotate(r.level.replace(' (lab rules: zero filter + strict RCA)', ' (lab rules)'), (r.n_products, r.r2), fontsize=7, xytext=(4, -10), textcoords='offset points')
        ax.set_xscale('log'); ax.set_xlabel('number of products (log)'); ax.set_ylabel('R$^2$: log GDPpc (PPP) on ECI')
        ax.set_title(f'Granularity ladder, {year}'); ax.legend(fontsize=7, loc='lower right')
        fig.tight_layout(); fig.savefig(HERE / 'figures' / 'ladder_2019.png', dpi=110)
    print(year); print(ladder.round(3).to_string()); print(rsum.round(3).to_string())
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
