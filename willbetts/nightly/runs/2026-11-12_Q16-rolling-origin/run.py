"""Q16 - Rolling-origin out-of-time evaluation of ECI variants.

Pre-registered before looking at results (research-agenda section 5):
  outcome   : annualized log growth of real GDPpc (WDI constant 2015 US$) over t -> t+10
  baseline  : growth ~ log GDPpc_t + resource rents_t + resource export share_t   (pooled OLS)
  candidate : baseline + one complexity score (z-scored within origin year)
  protocol  : for each test origin T in 2005..2014, fit on all origins t <= T-10 (outcomes fully
              observed by T), predict origin T. Metric = pooled out-of-sample RMSE and the
              out-of-sample R^2 relative to the baseline, R2oos = 1 - SSE_cand / SSE_base.
  also      : a single split (develop on origins 1995-2004, test once on 2005-2014) - which is
              the rolling scheme's last fold - and the share of test origins where the
              candidate beats the baseline.
All variants tried are reported. Variants come from external-data/derived/score_panel.csv.
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
import research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
VARS = ['eci_atlas_published', 'eci_binary', 'eci_log1p', 'eci_capped', 'eci_pctile', 'eci_rpca', 'eci_rca_and_rpca',
        'log_fitness', 'diversity', 'entropy', 'coi']
CTRL = ['lny0', 'resource_rents_pct_gdp', 'resource_share']
D = R.window_panel(list(range(1995, 2015)), 10, 'const')
D = R.zscore_within(D, VARS).dropna(subset=['growth'] + CTRL + VARS)

def fit_predict(train, test, xs):
    A = np.c_[np.ones(len(train)), train[xs].to_numpy(float)]
    beta, *_ = np.linalg.lstsq(A, train.growth.to_numpy(float), rcond=None)
    return np.c_[np.ones(len(test)), test[xs].to_numpy(float)] @ beta

rows, folds = [], []
for T in range(2005, 2015):
    tr, te = D[D.start <= T - 10], D[D.start == T]
    if len(tr) == 0 or len(te) == 0:
        continue
    eb = te.growth - fit_predict(tr, te, CTRL)
    em = te.growth - tr.growth.mean()
    f = {'T': T, 'n_train': len(tr), 'n_test': len(te), 'sse_baseline': float((eb ** 2).sum()), 'sse_hist_mean': float((em ** 2).sum())}
    for v in VARS:
        ec = te.growth - fit_predict(tr, te, CTRL + [v])
        f[f'sse_{v}'] = float((ec ** 2).sum())
    folds.append(f)
F = pd.DataFrame(folds)
F.to_csv(HERE / 'figures' / 'folds.csv', index=False)
N = F.n_test.sum()
tab = [{'variant': 'baseline (income + resources)', 'rmse': float(np.sqrt(F.sse_baseline.sum() / N)), 'r2_oos_vs_baseline': 0.0, 'share_folds_better': np.nan}]
for v in VARS:
    tab.append({'variant': v, 'rmse': float(np.sqrt(F[f'sse_{v}'].sum() / N)),
                'r2_oos_vs_baseline': float(1 - F[f'sse_{v}'].sum() / F.sse_baseline.sum()),
                'share_folds_better': float((F[f'sse_{v}'] < F.sse_baseline).mean())})
tab = pd.DataFrame(tab).sort_values('r2_oos_vs_baseline', ascending=False)
tab.to_csv(HERE / 'figures' / 'rolling_summary.csv', index=False)
# single split
tr, te = D[D.start <= 2004], D[(D.start >= 2005)]
# only use origins whose outcome is unknown at 2004+10... single split = develop on 1995-2004 origins, test 2005-2014 origins
eb = te.growth - fit_predict(tr, te, CTRL)
split = [{'variant': 'baseline', 'rmse': float(np.sqrt((eb ** 2).mean())), 'r2_oos_vs_baseline': 0.0}]
for v in VARS:
    ec = te.growth - fit_predict(tr, te, CTRL + [v])
    split.append({'variant': v, 'rmse': float(np.sqrt((ec ** 2).mean())), 'r2_oos_vs_baseline': float(1 - (ec ** 2).sum() / (eb ** 2).sum())})
split = pd.DataFrame(split).sort_values('r2_oos_vs_baseline', ascending=False)
# in-sample for comparison (all origins)
ins = []
b = R.ols(D, 'growth', CTRL)
for v in VARS:
    m = R.ols(D, 'growth', CTRL + [v])
    ins.append({'variant': v, 'in_sample_delta_r2': m['r2'] - b['r2'], 'coef_sd': m['coef'][v]})
ins = pd.DataFrame(ins)
# robustness: holdout by region-free proxy - drop commodity exporters (resource share > 0.5 at origin)
Dn = D[D.resource_share <= 0.5]
fo = []
for T in range(2005, 2015):
    trn, ten = Dn[Dn.start <= T - 10], Dn[Dn.start == T]
    e0 = ten.growth - fit_predict(trn, ten, CTRL)
    fo.append({'sse_base': float((e0 ** 2).sum()), **{v: float(((ten.growth - fit_predict(trn, ten, CTRL + [v])) ** 2).sum()) for v in VARS}})
fo = pd.DataFrame(fo)
noncomm = {v: float(1 - fo[v].sum() / fo.sse_base.sum()) for v in VARS}
fig, ax = plt.subplots(figsize=(6.5, 3.8))
t2 = tab[tab.variant != 'baseline (income + resources)']
ax.barh(t2.variant, t2.r2_oos_vs_baseline * 100); ax.axvline(0, color='k', lw=.8)
ax.set_xlabel('out-of-sample R$^2$ vs baseline (%)'); ax.set_title('Rolling-origin test, origins 2005-2014 (10-yr growth)')
ax.invert_yaxis(); fig.tight_layout(); fig.savefig(HERE / 'figures' / 'rolling_r2oos.png', dpi=110)
res = {'rolling': tab.to_dict('records'), 'single_split': split.to_dict('records'), 'in_sample': ins.to_dict('records'),
       'non_commodity_rolling_r2oos': noncomm, 'n_test_obs': int(N), 'n_origins_test': int(len(F)),
       'n_obs_total': int(len(D)), 'baseline_r2oos_vs_historical_mean': float(1 - F.sse_baseline.sum() / F.sse_hist_mean.sum()), 'n_countries': int(D.iso3.nunique()), 'runtime_s': time.time() - t0}
R.save_json(res, HERE / 'results.json')
print(tab.round(4).to_string()); print(split.round(4).to_string()); print(ins.round(4).to_string()); print({k: round(v, 4) for k, v in noncomm.items()}); print(N, len(D))
