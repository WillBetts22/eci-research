"""Q08 - Fitness-Complexity (Tacchella et al. 2012) vs ECI at HS4.

Pre-stated metrics as Q07 (income Spearman/R^2 and year-to-year rank stability, 2019-2022),
plus rank disagreements with ECI in 2019. Baseline: binary ECI. Also diversity (k_c,0) as a
naive benchmark. Repo HS4 primary; Growth Lab HS4 as replication.
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
YEARS = [2019, 2020, 2021, 2022]
res = {}
for src, loader in [('repo Comtrade HS4', lambda y: R.repo_hs(y, 4)), ('Growth Lab HS4', lambda y: R.atlas_hs4(y))]:
    S = {'ECI (binary)': {}, 'log Fitness': {}, 'diversity': {}}
    for y in YEARS:
        M = eci.mcp(loader(y))
        S['ECI (binary)'][y] = eci.eci_pci(M)[0]
        S['log Fitness'][y] = R.fitness(M)
        S['diversity'][y] = M.sum(axis=1).rename('diversity')
    rows = []
    for name, d in S.items():
        inc = [R.r2_logincome(d[y], y) for y in YEARS]
        stab = [R.spearman(d[a], d[b])[0] for a, b in zip(YEARS[:-1], YEARS[1:])]
        rows.append({'measure': name, 'spearman_log_gdppc': np.mean([i['spearman'] for i in inc]),
                     'r2_log_gdppc': np.mean([i['r2'] for i in inc]), 'stability': np.mean(stab)})
    tab = pd.DataFrame(rows)
    e, f = S['ECI (binary)'][2019], S['log Fitness'][2019]
    rk = pd.DataFrame({'eci_rank': e.rank(ascending=False), 'fitness_rank': f.rank(ascending=False)})
    rk['diff'] = rk.fitness_rank - rk.eci_rank
    if src.startswith('repo'):
        rk['iso3'] = rk.index
        big = rk.reindex(rk['diff'].abs().sort_values(ascending=False).index).head(10)
        big.to_csv(HERE / 'figures' / 'largest_disagreements_2019.csv')
        fig, ax = plt.subplots(figsize=(5, 4.2))
        ax.scatter(e, f[e.index], s=12)
        for c in big.index[:8]:
            ax.annotate(c, (e[c], f[c]), fontsize=7)
        ax.set_xlabel('ECI (HS4, 2019)'); ax.set_ylabel('log10 Fitness'); ax.set_title('Fitness vs ECI, repo HS4 2019')
        fig.tight_layout(); fig.savefig(HERE / 'figures' / 'fitness_vs_eci_2019.png', dpi=110)
        res['largest_disagreements_2019'] = big[['eci_rank', 'fitness_rank', 'diff']].to_dict('index')
    res[src] = {'table': tab.to_dict('records'), 'spearman_eci_fitness_2019': R.spearman(e, f)[0],
                'mean_abs_rank_diff_2019': float(rk['diff'].abs().mean()), 'n_2019': int(len(e))}
    print(src); print(tab.round(3).to_string()); print(res[src]['spearman_eci_fitness_2019'], res[src]['mean_abs_rank_diff_2019'])
# convergence diagnostic: rank correlation is stable in n_iter, Pearson R^2 is not (bottom log-fitness diverges)
M = eci.mcp(R.repo_hs(2019, 4))
res['iteration_diagnostic_2019'] = [{'n_iter': n, **{k: v for k, v in R.r2_logincome(R.fitness(M, n_iter=n, tol=0), 2019).items()}}
                                    for n in [10, 20, 50, 100, 200]]
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
print(res.get('largest_disagreements_2019'))
