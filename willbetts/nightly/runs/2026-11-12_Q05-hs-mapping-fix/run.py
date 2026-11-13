"""Q05 - Fix the HS-chapter mapping (D4) and re-measure.

Groups are rebuilt in memory from data/raw (the cleaned CSVs are not touched).
Pre-stated metrics (lab rules: zero filter + strict RCA, sign oriented): Spearman of ECI vs
the cleaned-CSV baseline, mean |rank change|, R^2 with log GDPpc (WDI PPP), Spearman with
HS4 ECI. Variants (all reported):
  rebuilt   : lab mapping (datacleaning2025 cell 5) rebuilt from raw  -> reproduction check
  fix84     : minimal D4 fix, chapter 84 added to Machinery and Construction (83+84)
  table1    : Table-1 consistent: Machinery = 84+85, Transportation = 86-89, 83 -> Metals,
              Daily Instruments = 90,91,93-97, aggregate kept
  table1_noagg : table1 with the High-complexity aggregate dropped (17 groups)
"""
import sys, time, copy
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
L = R.LAB_GROUPS
fix84 = copy.deepcopy(L); fix84['Machinery and Construction'] = [83, 84]
t1 = copy.deepcopy(L)
t1['Machinery and Construction'] = [84, 85]
t1['Transportation'] = [86, 87, 88, 89, 98]
t1['Metals'] = list(range(72, 84))
t1['Daily Instruments'] = [90, 91, 93, 94, 95, 96, 97]
t1_noagg = {k: v for k, v in t1.items() if k != 'High-complexity Products'}
VARIANTS = {'rebuilt': L, 'fix84': fix84, 'table1': t1, 'table1_noagg': t1_noagg}

res = {'mappings': {k: v for k, v in VARIANTS.items() if k != 'rebuilt'}}
all_ch = set(range(1, 98)) | {98, 99}
res['chapters_in_no_regular_group'] = {k: sorted(all_ch - set(c for g, chs in v.items() if g != 'High-complexity Products' for c in chs)) for k, v in VARIANTS.items()}
rows, repro, rc_rows = [], {}, []
for year in [2019, 2020, 2021, 2022, 2023]:
    base_X = R.lab_groups_iso3(year, drop_eu=True)
    rb = R.groups_from_raw(year, L)
    idx = base_X.index.intersection(rb.index)
    rel = (rb.loc[idx].sum().sum() - base_X.loc[idx].sum().sum()) / base_X.loc[idx].sum().sum()
    cell_match = float(np.isclose(rb.loc[idx, base_X.columns].to_numpy(), base_X.loc[idx].to_numpy(), rtol=1e-6).mean())
    repro[year] = {'common_countries': int(len(idx)), 'cleaned_only': int(len(base_X.index.difference(rb.index))),
                   'raw_only': int(len(rb.index.difference(base_X.index))), 'rel_total_diff': float(rel), 'share_cells_equal': cell_match}
    base, _ = R.grouped_eci(year, X=base_X)
    hs4 = eci.eci_from_exports(R.repo_hs(year, 4))
    def score(e, name):
        common = base.index.intersection(e.index)
        rb_, re_ = base[common].rank(ascending=False), e[common].rank(ascending=False)
        rows.append({'year': year, 'variant': name, 'n': int(len(e)),
                     'spearman_vs_baseline': R.spearman(base, e)[0], 'mean_abs_rank_change': float((rb_ - re_).abs().mean()),
                     'max_abs_rank_change': float((rb_ - re_).abs().max()),
                     'r2_log_gdppc': R.r2_logincome(e, year)['r2'], 'spearman_log_gdppc': R.r2_logincome(e, year)['spearman'],
                     'spearman_vs_hs4': R.spearman(e, hs4)[0]})
        if year == 2019:
            for c in R.REPORT_COUNTRIES:
                if c in e.index:
                    rc_rows.append({'variant': name, 'country': R.REPORT_COUNTRIES[c], 'rank': int(e.rank(ascending=False)[c]), 'n': int(len(e))})
    score(base, 'baseline (cleaned CSV)')
    for name, mp in VARIANTS.items():
        X = R.groups_from_raw(year, mp)
        e, _ = R.grouped_eci(year, X=X)
        score(e, name)
tab = pd.DataFrame(rows)
tab.to_csv(HERE / 'figures' / 'variants_by_year.csv', index=False)
rc = pd.DataFrame(rc_rows).pivot(index='country', columns='variant', values='rank')
rc.to_csv(HERE / 'figures' / 'report_country_ranks_2019.csv')
res['reproduction'] = repro
res['by_year'] = tab.to_dict('records')
res['mean_2019_2022'] = tab[tab.year <= 2022].groupby('variant')[['spearman_vs_baseline', 'mean_abs_rank_change', 'r2_log_gdppc', 'spearman_log_gdppc', 'spearman_vs_hs4']].mean().to_dict('index')
res['report_ranks_2019'] = rc.to_dict('index')
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
print(pd.DataFrame(repro).T); print(tab[tab.year == 2019].round(3).to_string()); print(pd.DataFrame(res['mean_2019_2022']).T.round(3)); print(rc)
print(res['chapters_in_no_regular_group'])
