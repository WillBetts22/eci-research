"""Q14 - Mediation: does ECI survive education, R&D and governance controls?

Same 10-year design as Q12 (windows 1995-2005, 2004-2014, 2013-2023; WDI constant US$;
period FE; HC1 SEs). All models on ONE common sample so coefficients are comparable.
Capability controls measured at the window start (WGI 1996 used for the 1995 start):
  human capital  : PWT hc (years of schooling + returns)
  governance     : WGI government effectiveness, rule of law
  R&D            : R&D spending % GDP (sparse; separate smaller sample)
  infrastructure : internet users %, private credit % GDP
Pre-stated metric: the ECI coefficient (per SD) and how much of it remains when the controls
are added (ratio to the controls-free coefficient on the same sample).
Decomposition: R^2 of ECI regressed on the capability variables, 2013 cross-section.
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
STARTS = [1995, 2004, 2013]
D = R.window_panel(STARTS, 10, 'const')
# WGI starts in 1996: use 1996 values for the 1995 window
W96 = R.wgi().query('year == 1996').set_index('iso3')
for c in ['wgi_gov_effectiveness', 'wgi_rule_of_law', 'wgi_regulatory_quality', 'wgi_control_corruption']:
    k = D.start == 1995
    D.loc[k, c] = D.loc[k, 'iso3'].map(W96[c]).values
D['ln_hc'] = np.log(D.hc)
CAP = ['ln_hc', 'wgi_gov_effectiveness', 'wgi_rule_of_law']
BASE = ['lny0', 'resource_rents_pct_gdp', 'resource_share']
D = R.zscore_within(D, ['eci_atlas_published', 'eci_binary'] + CAP + ['internet_users_pct', 'private_credit_pct_gdp', 'rnd_pct_gdp', 'tertiary_enrollment'])
res = {}
def ladder(core, eci_col, extra_sets, label):
    rows = []
    ref = None
    for name, xs in extra_sets:
        m = R.ols(core, 'growth', BASE + [eci_col] + xs, fe='start')
        if ref is None:
            ref = m['coef'][eci_col]
        rows.append({'model': name, 'n': m['n'], 'r2': m['r2'], 'eci_coef_sd': m['coef'][eci_col], 'eci_se': m['se'][eci_col],
                     'eci_p': m['p'][eci_col], 'share_of_ref_coef': m['coef'][eci_col] / ref,
                     **{f'coef_{x}': m['coef'][x] for x in xs}, **{f'p_{x}': m['p'][x] for x in xs}})
    tab = pd.DataFrame(rows); tab.to_csv(HERE / 'figures' / f'{label}.csv', index=False)
    print(label); print(tab[['model', 'n', 'r2', 'eci_coef_sd', 'eci_p', 'share_of_ref_coef']].round(3).to_string())
    return tab.to_dict('records')
sets = [('ECI + income + resources', []), ('+ human capital', ['ln_hc']), ('+ governance', ['wgi_gov_effectiveness', 'wgi_rule_of_law']),
        ('+ human capital + governance', ['ln_hc', 'wgi_gov_effectiveness', 'wgi_rule_of_law'])]
core = D.dropna(subset=['growth', 'eci_atlas_published'] + BASE + CAP)
res['main_atlas_eci'] = ladder(core, 'eci_atlas_published', sets, 'mediation_atlas_eci')
res['main_our_eci'] = ladder(core, 'eci_binary', sets, 'mediation_our_eci')
res['main_n_countries'] = int(core.iso3.nunique())
# capabilities without ECI (do they predict growth on their own?)
m = R.ols(core, 'growth', BASE + CAP, fe='start')
res['capabilities_without_eci'] = m
# infrastructure / finance
core2 = D.dropna(subset=['growth', 'eci_atlas_published'] + BASE + CAP + ['internet_users_pct', 'private_credit_pct_gdp'])
res['with_infrastructure'] = ladder(core2, 'eci_atlas_published', sets[:1] + [('+ all capabilities + internet + credit', CAP + ['internet_users_pct', 'private_credit_pct_gdp'])], 'mediation_infra')
# R&D (sparse)
core3 = D.dropna(subset=['growth', 'eci_atlas_published'] + BASE + ['rnd_pct_gdp', 'ln_hc'])
res['with_rnd'] = ladder(core3, 'eci_atlas_published', sets[:1] + [('+ R&D', ['rnd_pct_gdp']), ('+ R&D + human capital', ['rnd_pct_gdp', 'ln_hc'])], 'mediation_rnd')
# decomposition: what share of ECI is explained by capabilities (2013 cross-section, raw values)
P = R.score_panel().query('year == 2013').copy()
P['ln_hc'] = np.log(P.hc); P['lny'] = np.log(P.gdppc_const2015usd)
dec = {}
for name, xs in [('capabilities', ['ln_hc', 'wgi_gov_effectiveness', 'wgi_rule_of_law']),
                 ('capabilities + income', ['ln_hc', 'wgi_gov_effectiveness', 'wgi_rule_of_law', 'lny']),
                 ('income only', ['lny']),
                 ('capabilities + income + resources', ['ln_hc', 'wgi_gov_effectiveness', 'wgi_rule_of_law', 'lny', 'resource_share'])]:
    d = P.dropna(subset=['eci_atlas_published', 'ln_hc', 'wgi_gov_effectiveness', 'wgi_rule_of_law', 'lny', 'resource_share'])
    dec[name] = R.ols(d, 'eci_atlas_published', xs)
res['decomposition_2013'] = dec
print({k: (round(v['r2'], 3), v['n']) for k, v in dec.items()})
res['runtime_s'] = time.time() - t0
R.save_json(res, HERE / 'results.json')
