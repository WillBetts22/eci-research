"""Q13 - Our HS4 ECI vs Harvard Growth Lab's published ECI, 2019-2023.

Pre-stated metric: Spearman (and Pearson) with the published ECI on common countries.
Compared: (a) library ECI on repo Comtrade HS4 (data/raw); (b) library ECI on the Growth Lab's
own HS4 trade (isolates method from data differences); (c) the lab's grouped ECI (lab rules,
oriented); (d) the notebook as-is (unoriented). Plus the largest disagreements for (a) in 2019.
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
A = R.atlas_cy()
rows = []
for y in [2019, 2020, 2021, 2022, 2023]:
    pub = A[A.year == y].set_index('iso3').eci.dropna()
    repo = eci.eci_from_exports(R.repo_hs(y, 4))
    repo_pop = repo.loc[[c for c in repo.index if R.wdi().query('year == @y').set_index('iso3').population.get(c, 0) >= 1e6]]
    gl = eci.eci_from_exports(R.atlas_hs4(y))
    grp, _ = R.grouped_eci(y)
    g = eci.load_groups(y, notebook_names=False); iso = eci.group_name_to_iso3(g.index)
    nb = eci.notebook_eci(g); nb.index = [iso[n] for n in nb.index]; nb = nb[nb.index.notna()]
    for name, s in [('repo HS4 (all >= $1B)', repo), ('repo HS4 (pop >= 1M)', repo_pop), ('Growth Lab HS4 + our library', gl),
                    ('lab grouped, oriented', grp), ('notebook as-is', nb)]:
        idx = s.index.intersection(pub.index)
        rows.append({'year': y, 'version': name, 'n': int(len(idx)), 'spearman': R.spearman(s, pub)[0],
                     'pearson': float(np.corrcoef(s[idx], pub[idx])[0, 1])})
    if y == 2019:
        idx = repo_pop.index.intersection(pub.index)
        d = pd.DataFrame({'repo_rank': repo_pop[idx].rank(ascending=False), 'atlas_rank': pub[idx].rank(ascending=False)})
        d['diff'] = d.repo_rank - d.atlas_rank
        top = d.reindex(d['diff'].abs().sort_values(ascending=False).index).head(10)
        top.to_csv(HERE / 'figures' / 'largest_disagreements_2019.csv')
        dis = top.to_dict('index')
        # trade totals for the top disagreements: repo vs Growth Lab
        raw = R.repo_hs(2019, 4).sum(axis=1); gl_tot = A[A.year == 2019].set_index('iso3').export_value
        dis_tot = {c: {'repo_bn': float(raw.get(c, np.nan) / 1e9), 'growthlab_bn': float(gl_tot.get(c, np.nan) / 1e9)} for c in top.index}
        fig, ax = plt.subplots(figsize=(5, 4.2))
        ax.scatter(pub[idx], repo_pop[idx], s=10)
        for c in top.index[:6]:
            ax.annotate(c, (pub[c], repo_pop[c]), fontsize=7)
        ax.set_xlabel('Growth Lab published ECI 2019'); ax.set_ylabel('our HS4 ECI (repo Comtrade) 2019')
        fig.tight_layout(); fig.savefig(HERE / 'figures' / 'repo_vs_atlas_2019.png', dpi=110)
tab = pd.DataFrame(rows)
tab.to_csv(HERE / 'figures' / 'agreement.csv', index=False)
res = {'table': tab.to_dict('records'), 'largest_disagreements_2019': dis, 'disagreement_trade_totals': dis_tot,
       'mean_2019_2022': tab[tab.year <= 2022].groupby('version')[['spearman', 'pearson', 'n']].mean().to_dict('index'),
       'runtime_s': time.time() - t0}
R.save_json(res, HERE / 'results.json')
print(tab.pivot(index='version', columns='year', values='spearman').round(3)); print(dis); print(dis_tot)
