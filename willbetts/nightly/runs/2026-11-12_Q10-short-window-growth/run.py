"""Q10 - Short-window growth test (pilot): does 2019 complexity predict 2019-2023 real growth?

Outcome: annualized log growth of real GDP per capita 2019->2023 (WDI constant 2015 US$),
PPP constant as a robustness check. Pre-stated baseline: growth ~ log GDPpc 2019 + resource
export share (HS 26/27/71). Metric: increase in R^2 and the coefficient (per 1 SD) of each
candidate added alone. Same country sample for every candidate except the grouped ECI
(its zero filter drops countries; reported on its own sample with its own baseline).
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
X = R.repo_hs(2019, 4)
M = eci.mcp(X)
cands = {
    'HS4 ECI (repo)': eci.eci_pci(M)[0],
    'HS4 ECI log(1+RCA)': R.eci_weighted(np.log1p(eci.rca(X)), orient_to=M.sum(axis=1)),
    'log Fitness (HS4)': R.fitness(M),
    'diversity (HS4)': M.sum(axis=1),
    'export entropy (HS4)': R.entropy(X),
    'Growth Lab published ECI': R.atlas_cy().query('year == 2019').set_index('iso3').eci,
}
grouped, _ = R.grouped_eci(2019, drop_eu=True)
res = {}
for kind in ['const', 'ppp']:
    df = pd.DataFrame({'growth': R.growth(2019, 2023, kind), 'lny0': np.log(R.gdppc(2019, kind)),
                       'resource': R.resource_share(X)})
    for k, v in cands.items():
        df[k] = (v - v.mean()) / v.std()
    df['grouped ECI (lab rules)'] = (grouped - grouped.mean()) / grouped.std()
    core = df.dropna(subset=['growth', 'lny0', 'resource'] + list(cands))
    base = R.ols(core, 'growth', ['lny0', 'resource'])
    rows = [{'model': 'baseline: log GDPpc + resource share', 'n': base['n'], 'r2': base['r2'], 'coef_sd': np.nan, 'p': np.nan,
             'coef_lny0': base['coef']['lny0']}]
    for k in cands:
        m = R.ols(core, 'growth', ['lny0', 'resource', k])
        alone = R.ols(core, 'growth', [k])
        rows.append({'model': f'+ {k}', 'n': m['n'], 'r2': m['r2'], 'delta_r2': m['r2'] - base['r2'],
                     'coef_sd': m['coef'][k], 'se': m['se'][k], 'p': m['p'][k], 'coef_lny0': m['coef']['lny0'],
                     'r2_alone': alone['r2']})
    gs = df.dropna(subset=['growth', 'lny0', 'resource', 'grouped ECI (lab rules)'])
    gb = R.ols(gs, 'growth', ['lny0', 'resource']); gm = R.ols(gs, 'growth', ['lny0', 'resource', 'grouped ECI (lab rules)'])
    rows.append({'model': '+ grouped ECI (lab rules) [own sample]', 'n': gm['n'], 'r2': gm['r2'], 'delta_r2': gm['r2'] - gb['r2'],
                 'coef_sd': gm['coef']['grouped ECI (lab rules)'], 'se': gm['se']['grouped ECI (lab rules)'],
                 'p': gm['p']['grouped ECI (lab rules)'], 'coef_lny0': gm['coef']['lny0']})
    tab = pd.DataFrame(rows)
    tab.to_csv(HERE / 'figures' / f'growth_models_{kind}.csv', index=False)
    res[kind] = {'table': tab.to_dict('records'), 'n_core': int(len(core)),
                 'growth_mean': float(core.growth.mean()), 'growth_sd': float(core.growth.std()),
                 'top_abs_growth': core.growth.abs().sort_values(ascending=False).head(5).index.tolist()}
    print(kind); print(tab.round(3).to_string())
# robustness: drop the 5% most extreme growth observations
df = pd.DataFrame({'growth': R.growth(2019, 2023, 'const'), 'lny0': np.log(R.gdppc(2019, 'const')), 'resource': R.resource_share(X),
                   'eci': cands['HS4 ECI (repo)']}).dropna()
q = df.growth.quantile([.025, .975]); trim = df[(df.growth > q.iloc[0]) & (df.growth < q.iloc[1])]
m = R.ols(trim, 'growth', ['lny0', 'resource', 'eci'])
res['trimmed_hs4_eci'] = {'n': m['n'], 'coef_per_unit_eci': m['coef']['eci'], 'p': m['p']['eci']}
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
print(res['trimmed_hs4_eci'], res['const']['top_abs_growth'])
