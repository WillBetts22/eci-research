"""Q15 - Population-adjusted RCA.

RpcA_cp = (x_cp / pop_c) / (sum_c x_cp / sum_c pop_c): exports per person relative to the
world's exports per person in that product. Variants (Growth Lab HS4, sample exports >= $1B and
pop >= 1M, built in external-data/scripts/build_score_panel.py):
  eci_binary        : M = RCA >= 1 (baseline)
  eci_rpca          : M = RpcA >= 1
  eci_rca_and_rpca  : M = RCA >= 1 AND RpcA >= 1
Repo Comtrade HS4 (2019) is used as a second data source.
Pre-stated metrics: Spearman/R^2 with log GDPpc (mean 2019-2022), year-to-year rank stability,
Spearman with the published ECI, and the Q12 10-year growth regression (coefficient per SD,
delta R^2 over the income + resources baseline).
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
P = R.score_panel()
V = ['eci_binary', 'eci_rpca', 'eci_rca_and_rpca']
rows = []
for v in V:
    inc = [R.r2_logincome(P[P.year == y].set_index('iso3')[v], y) for y in range(2019, 2023)]
    stab = [R.spearman(P[P.year == a].set_index('iso3')[v], P[P.year == a + 1].set_index('iso3')[v])[0] for a in range(2019, 2022)]
    pub = [R.spearman(P[P.year == y].set_index('iso3')[v], P[P.year == y].set_index('iso3').eci_atlas_published)[0] for y in range(2019, 2023)]
    rows.append({'variant': v, 'spearman_log_gdppc': np.mean([i['spearman'] for i in inc]), 'r2_log_gdppc': np.mean([i['r2'] for i in inc]),
                 'stability': np.mean(stab), 'spearman_vs_published': np.mean(pub)})
desc = pd.DataFrame(rows)
# growth regression (Q12 design)
CTRL = ['lny0', 'resource_rents_pct_gdp', 'resource_share']
D = R.zscore_within(R.window_panel([1995, 2004, 2013], 10, 'const'), V).dropna(subset=['growth'] + CTRL + V)
b = R.ols(D, 'growth', CTRL, fe='start')
g = []
for v in V:
    m = R.ols(D, 'growth', CTRL + [v], fe='start')
    g.append({'variant': v, 'n': m['n'], 'coef_sd': m['coef'][v], 'p': m['p'][v], 'delta_r2': m['r2'] - b['r2']})
gtab = pd.DataFrame(g)
both = R.ols(D, 'growth', CTRL + ['eci_binary', 'eci_rpca'], fe='start')
# small vs large countries: who moves most?
p19 = P[P.year == 2019].set_index('iso3')
rk = pd.DataFrame({'rca_rank': p19.eci_binary.rank(ascending=False), 'rpca_rank': p19.eci_rpca.rank(ascending=False), 'pop': p19.population})
rk['diff'] = rk.rpca_rank - rk.rca_rank
corr_pop = R.spearman(rk['diff'], np.log(rk['pop']))[0]
movers = rk.reindex(rk['diff'].abs().sort_values(ascending=False).index).head(10)
movers.to_csv(HERE / 'figures' / 'largest_movers_2019.csv')
# repo data 2019
X = R.repo_hs(2019, 4)
pop = R.wdi().query('year == 2019').set_index('iso3').population.reindex(X.index).dropna()
X = X.loc[pop.index]; X = X.loc[pop >= 1e6]; pop = pop[X.index]
Rc = eci.rca(X); Rp = X.div(pop, axis=0) / (X.sum(axis=0) / pop.sum())
div = (Rc >= 1).sum(axis=1)
repo = {'RCA>=1': R.eci_weighted((Rc >= 1).astype(float)), 'RpcA>=1': R.eci_weighted((Rp >= 1).astype(float), orient_to=div),
        'RCA>=1 & RpcA>=1': R.eci_weighted(((Rc >= 1) & (Rp >= 1)).astype(float), orient_to=div)}
repo_tab = {k: R.r2_logincome(v, 2019) for k, v in repo.items()}
res = {'descriptive': desc.to_dict('records'), 'growth': gtab.to_dict('records'), 'growth_n_obs': int(len(D)),
       'both_in_model': {'coef_binary': both['coef']['eci_binary'], 'p_binary': both['p']['eci_binary'],
                         'coef_rpca': both['coef']['eci_rpca'], 'p_rpca': both['p']['eci_rpca']},
       'spearman_rankdiff_vs_log_pop_2019': corr_pop, 'largest_movers_2019': movers[['rca_rank', 'rpca_rank', 'diff']].to_dict('index'),
       'repo_2019_income': repo_tab, 'runtime_s': time.time() - t0}
R.save_json(res, HERE / 'results.json')
print(desc.round(3).to_string()); print(gtab.round(3).to_string()); print(res['both_in_model'], corr_pop); print(movers); print(repo_tab)
