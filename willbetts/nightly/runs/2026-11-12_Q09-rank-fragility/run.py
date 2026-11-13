"""Q09 - How fragile are ECI ranks? Eigengap, product bootstrap, leave-one-country-out.

Pre-stated metrics: median width of the 90% bootstrap interval of each country's rank,
expressed as a share of the number of countries; mean |rank change| under leave-one-country-out
(LOCO); the eigengap lambda2 - lambda3 of Mcc per year. Grouped = lab rules (zero filter,
strict RCA, oriented); HS4 = repo data, RCA>=1. 2019 primary. 300 bootstrap draws.
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
B = 300
rng = np.random.default_rng(42)
res = {'eigengap': {}}
for y in [2019, 2020, 2021, 2022, 2023]:
    _, dg = R.grouped_eci(y)
    _, _, dh = eci.eci_pci(eci.mcp(R.repo_hs(y, 4)))
    _, _, da = eci.eci_pci(eci.mcp(R.atlas_hs4(y)))
    res['eigengap'][y] = {'grouped': dg, 'hs4_repo': dh, 'hs4_growthlab': da}

def boot(X, strict):
    base = eci.eci_pci(eci.mcp(X, strict=strict))[0]
    n = len(base)
    ranks = []
    for b in range(B):
        cols = rng.integers(0, X.shape[1], X.shape[1])
        Xb = X.iloc[:, cols]; Xb.columns = range(Xb.shape[1])
        e = eci.eci_pci(eci.mcp(Xb, strict=strict))[0]
        if np.corrcoef(e.reindex(base.index).fillna(0), base)[0, 1] < 0:
            e = -e
        ranks.append(e.rank(ascending=False).reindex(base.index))
    Rk = pd.concat(ranks, axis=1)
    lo, hi = Rk.quantile(.05, axis=1), Rk.quantile(.95, axis=1)
    loco = []
    br = base.rank(ascending=False)
    for c in base.index:
        e = eci.eci_pci(eci.mcp(X.drop(index=c), strict=strict))[0]
        r = e.rank(ascending=False)
        rb = br.drop(c); rb = rb.rank()  # re-rank remaining countries
        loco.append((r[rb.index] - rb).abs().mean())
    return base, lo, hi, n, np.array(loco)

Xg = eci.notebook_filter(R.lab_groups_iso3(2019))
Xh = R.repo_hs(2019, 4)
out = {}
for name, X, strict in [('grouped (18, lab rules)', Xg, True), ('HS4 (repo)', Xh, False)]:
    base, lo, hi, n, loco = boot(X, strict)
    width = (hi - lo) / n
    out[name] = {'n': n, 'median_ci_width_share': float(width.median()), 'mean_ci_width_ranks': float((hi - lo).mean()),
                 'share_ci_wider_than_quarter': float((width > .25).mean()),
                 'loco_mean_abs_rank_change': float(loco.mean()), 'loco_max_mean_abs_rank_change': float(loco.max()),
                 'report_countries': {R.REPORT_COUNTRIES[c]: {'rank': int(base.rank(ascending=False)[c]), 'ci90': [float(lo[c]), float(hi[c])]}
                                      for c in R.REPORT_COUNTRIES if c in base.index}}
    pd.DataFrame({'eci': base, 'rank': base.rank(ascending=False), 'ci_lo': lo, 'ci_hi': hi}).sort_values('rank').to_csv(
        HERE / 'figures' / f"rank_ci_{'grouped' if 'grouped' in name else 'hs4'}_2019.csv")
    print(name, {k: v for k, v in out[name].items() if k != 'report_countries'})
    print(out[name]['report_countries'])
res['bootstrap_2019'] = out
fig, axes = plt.subplots(1, 2, figsize=(11, 3.6))
for ax, f, t in zip(axes, ['grouped', 'hs4'], ['Grouped (18 groups)', 'HS4 (~1,200 products)']):
    d = pd.read_csv(HERE / 'figures' / f'rank_ci_{f}_2019.csv')
    ax.vlines(d['rank'], d.ci_lo, d.ci_hi, lw=1); ax.plot(d['rank'], d['rank'], 'k.', ms=2)
    ax.set_title(f'{t}: 90% bootstrap rank interval'); ax.set_xlabel('point rank'); ax.set_ylabel('rank')
fig.tight_layout(); fig.savefig(HERE / 'figures' / 'rank_intervals_2019.png', dpi=110)
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
print(pd.DataFrame({y: {k: v['eigengap_23'] for k, v in d.items()} for y, d in res['eigengap'].items()}).round(3))
print(pd.DataFrame({y: {k: v['lambda2'] for k, v in d.items()} for y, d in res['eigengap'].items()}).round(3))
