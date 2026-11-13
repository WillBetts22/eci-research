"""Q12 - Replicate the Atlas 10-year growth regression.

Design (Hausmann, Hidalgo et al. 2013): annualized growth of real GDPpc over 10 years on
initial ECI, log initial GDPpc and natural-resource intensity, with period fixed effects.
Windows: 1995-2005, 2004-2014, 2013-2023 (non-overlapping starts, WDI constant 2015 US$).
Pre-stated baseline: growth ~ log GDPpc + resource rents (% GDP) + resource export share + period FE.
Metric: coefficient on ECI (per 1 SD within period), its p-value (HC1), and the increase in R^2.
ECI sources: Growth Lab published ECI, and our library's ECI on the Growth Lab HS4 data.
Robustness: PPP outcome; PWT (rgdpna/pop) outcome for 1995-2005 and 2005-2015; per-window
cross sections; a within-country (country FE) 5-year panel.
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
STARTS = [1995, 2004, 2013]
SC = ['eci_atlas_published', 'eci_binary', 'diversity', 'entropy']
CTRL = ['lny0', 'resource_rents_pct_gdp', 'resource_share']
res = {}
def run(D, label):
    D = R.zscore_within(D, SC)
    core = D.dropna(subset=['growth'] + CTRL + SC)
    base = R.ols(core, 'growth', CTRL, fe='start')
    rows = [{'model': 'baseline', 'n': base['n'], 'r2': base['r2'], 'coef_lny0': base['coef']['lny0'], 'p_lny0': base['p']['lny0']}]
    for s in SC:
        m = R.ols(core, 'growth', CTRL + [s], fe='start')
        rows.append({'model': f'+ {s}', 'n': m['n'], 'r2': m['r2'], 'delta_r2': m['r2'] - base['r2'], 'coef_sd': m['coef'][s],
                     'se': m['se'][s], 'p': m['p'][s], 'coef_lny0': m['coef']['lny0'], 'p_lny0': m['p']['lny0']})
    noctrl = R.ols(core, 'growth', ['lny0'], fe='start'); noctrl_e = R.ols(core, 'growth', ['lny0', 'eci_atlas_published'], fe='start')
    rows.append({'model': 'income only (no resource controls)', 'n': noctrl['n'], 'r2': noctrl['r2']})
    rows.append({'model': 'income + Growth Lab ECI (no resource controls)', 'n': noctrl_e['n'], 'r2': noctrl_e['r2'],
                 'coef_sd': noctrl_e['coef']['eci_atlas_published'], 'p': noctrl_e['p']['eci_atlas_published']})
    tab = pd.DataFrame(rows)
    tab.to_csv(HERE / 'figures' / f'{label}.csv', index=False)
    print(label, len(core)); print(tab.round(3).to_string())
    return {'table': tab.to_dict('records'), 'n_countries': int(core.iso3.nunique()), 'n_obs': int(len(core)),
            'growth_mean': float(core.growth.mean())}
res['main_const_usd'] = run(R.window_panel(STARTS, 10, 'const'), 'main_const_usd')
res['ppp'] = run(R.window_panel(STARTS, 10, 'ppp'), 'ppp')
res['pwt_1995_2005_2005_2015'] = run(R.window_panel([1995, 2005], 10, 'pwt'), 'pwt')
# per window cross-sections
per = []
for s in STARTS:
    D = R.zscore_within(R.window_panel([s], 10, 'const'), SC).dropna(subset=['growth'] + CTRL + ['eci_atlas_published'])
    b = R.ols(D, 'growth', CTRL); m = R.ols(D, 'growth', CTRL + ['eci_atlas_published'])
    per.append({'window': f'{s}-{s + 10}', 'n': m['n'], 'coef_sd': m['coef']['eci_atlas_published'], 'p': m['p']['eci_atlas_published'],
                'r2_base': b['r2'], 'r2_with_eci': m['r2']})
res['per_window'] = per
print(pd.DataFrame(per).round(3))
# within-country: 5-year windows, country + period FE
D5 = R.zscore_within(R.window_panel(list(range(1995, 2020, 5)), 5, 'const'), ['eci_atlas_published', 'eci_binary'])
D5 = D5.dropna(subset=['growth', 'lny0', 'eci_atlas_published', 'resource_rents_pct_gdp'])
import statsmodels.formula.api as smf
fe = smf.ols('growth ~ eci_atlas_published + lny0 + resource_rents_pct_gdp + C(iso3) + C(start)', data=D5).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(D5.iso3)[0]})
pooled = smf.ols('growth ~ eci_atlas_published + lny0 + resource_rents_pct_gdp + C(start)', data=D5).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(D5.iso3)[0]})
res['five_year_panel'] = {'n': int(fe.nobs), 'n_countries': int(D5.iso3.nunique()),
                          'pooled_coef': float(pooled.params['eci_atlas_published']), 'pooled_p': float(pooled.pvalues['eci_atlas_published']),
                          'country_fe_coef': float(fe.params['eci_atlas_published']), 'country_fe_p': float(fe.pvalues['eci_atlas_published']),
                          'country_fe_coef_lny0': float(fe.params['lny0'])}
print(res['five_year_panel'])
# figure: partial regression of growth on ECI
D = R.zscore_within(R.window_panel(STARTS, 10, 'const'), SC).dropna(subset=['growth'] + CTRL + ['eci_atlas_published'])
import statsmodels.api as sm
Z = pd.get_dummies(D.start, drop_first=True).astype(float).assign(**{c: D[c] for c in CTRL}); Z = sm.add_constant(Z)
ry = sm.OLS(D.growth, Z).fit().resid; rx = sm.OLS(D.eci_atlas_published, Z).fit().resid
fig, ax = plt.subplots(figsize=(5.2, 4))
for s in STARTS:
    k = D.start == s; ax.scatter(rx[k], ry[k], s=10, label=f'{s}-{s+10}')
b = np.polyfit(rx, ry, 1); xs = np.linspace(rx.min(), rx.max(), 10); ax.plot(xs, b[0] * xs + b[1], 'k-')
ax.set_xlabel('ECI (residualized)'); ax.set_ylabel('10-yr growth, % p.a. (residualized)'); ax.legend(fontsize=7)
ax.set_title('Added-variable plot: ECI and 10-year growth'); fig.tight_layout(); fig.savefig(HERE / 'figures' / 'added_variable.png', dpi=110)
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
