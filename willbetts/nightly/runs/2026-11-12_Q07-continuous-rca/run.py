"""Q07 - Continuous vs binary RCA at HS4.

Pre-stated metrics: (1) Spearman and R^2 of the score with log GDPpc (WDI PPP), mean of
2019-2022; (2) year-to-year Spearman rank stability on common countries, mean of
2019-20, 20-21, 21-22. Baseline: binary RCA>=1 ECI. 2023 excluded (D1, see Q06).
Data: repo HS4 (data/raw), with the Growth Lab HS4 panel as a replication.
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
YEARS = [2019, 2020, 2021, 2022]
out = {}
for src, loader in [('repo Comtrade HS4', lambda y: R.repo_hs(y, 4)), ('Growth Lab HS4', lambda y: R.atlas_hs4(y))]:
    scores = {}
    for y in YEARS:
        X = loader(y)
        div = (eci.rca(X) >= 1).sum(axis=1)
        for name, W in R.rca_variants(X).items():
            scores.setdefault(name, {})[y] = R.eci_weighted(W, orient_to=div)
    rows = []
    for name, d in scores.items():
        inc = [R.r2_logincome(d[y], y) for y in YEARS]
        stab = [R.spearman(d[a], d[b])[0] for a, b in zip(YEARS[:-1], YEARS[1:])]
        base = scores['binary RCA>=1']
        rows.append({'variant': name, 'spearman_log_gdppc': np.mean([i['spearman'] for i in inc]),
                     'r2_log_gdppc': np.mean([i['r2'] for i in inc]), 'stability': np.mean(stab),
                     'spearman_vs_binary_2019': R.spearman(d[2019], base[2019])[0], 'n_2019': inc[0]['n']})
    out[src] = pd.DataFrame(rows)
    out[src].to_csv(HERE / 'figures' / f"variants_{src.split()[0].lower()}.csv", index=False)
    print(src); print(out[src].round(3).to_string())
R.save_json({k: v.to_dict('records') for k, v in out.items()} | {'runtime_s': time.time() - t0}, HERE / 'results.json')
