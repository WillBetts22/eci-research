"""Reconcile Will Q16 vs Julia Project 3: start from Will's Q16 spec and change one thing at a time."""
import sys, numpy as np, pandas as pd, warnings
warnings.filterwarnings('ignore')
sys.path.insert(0, '/Users/wbetts/eci-research/willbetts/nightly/lib')
import research as R

VARS = ['eci_binary', 'eci_atlas_published', 'diversity', 'entropy', 'log_fitness', 'eci_log1p']
ALLV = ['eci_atlas_published','eci_binary','eci_log1p','eci_capped','eci_pctile','eci_rpca','eci_rca_and_rpca','log_fitness','diversity','entropy','coi']

def panel(kind):
    D = R.window_panel(list(range(1995, 2015)), 10, kind)
    D = R.zscore_within(D, ALLV)
    return D.dropna(subset=['growth','lny0','resource_rents_pct_gdp','resource_share'] + ALLV)

def fit_pred(tr, te, xs, period_fe=False, train_std=False):
    Xtr, Xte = tr[xs].astype(float).copy(), te[xs].astype(float).copy()
    if train_std:
        m, s = Xtr.mean(), Xtr.std(ddof=0); Xtr, Xte = (Xtr-m)/s, (Xte-m)/s
    if period_fe:
        for y in sorted(tr.start.unique())[1:]:
            ind = (tr.start == y).astype(float); Xtr[f'p{y}'] = ind - ind.mean(); Xte[f'p{y}'] = 0.
    A = np.c_[np.ones(len(Xtr)), Xtr.to_numpy()]
    b, *_ = np.linalg.lstsq(A, tr.growth.to_numpy(float), rcond=None)
    return np.c_[np.ones(len(Xte)), Xte.to_numpy()] @ b

def run(D, ctrl, origins, **kw):
    sse = {v: 0. for v in ['base'] + VARS}; wins = {v: 0 for v in VARS}; n = 0
    for T in origins:
        tr, te = D[D.start <= T-10], D[D.start == T]
        if len(tr) == 0 or len(te) == 0: continue
        eb = ((te.growth - fit_pred(tr, te, ctrl, **kw))**2).sum(); sse['base'] += eb; n += len(te)
        for v in VARS:
            ec = ((te.growth - fit_pred(tr, te, ctrl+[v], **kw))**2).sum(); sse[v] += ec; wins[v] += ec < eb
    return {v: 100*(1 - sse[v]/sse['base']) for v in VARS}, n

W_CTRL = ['lny0','resource_rents_pct_gdp','resource_share']; J_CTRL = ['lny0','resource_rents_pct_gdp']
ALL_O = list(range(2005, 2015)); J_O = [2005, 2008, 2014]
Dc, Dp = panel('const'), panel('ppp')
steps = [
 ('0 Will Q16 as published (const US$, +resource share, origins 2005-14)', Dc, W_CTRL, ALL_O, {}),
 ('1 drop resource export share',                                     Dc, J_CTRL, ALL_O, {}),
 ('2 PPP outcome only',                                               Dp, W_CTRL, ALL_O, {}),
 ('3 drop resource share + PPP',                                      Dp, J_CTRL, ALL_O, {}),
 ('4 = 3 + Julia period effects & train-only scaling',                Dp, J_CTRL, ALL_O, dict(period_fe=True, train_std=True)),
 ('5 = 4 on Julia origins only (2005, 2008, 2014)',                   Dp, J_CTRL, J_O, dict(period_fe=True, train_std=True)),
 ('6 Will spec (resource share, const) on Julia origins',             Dc, W_CTRL, J_O, {}),
]
rows = []
for name, D, ctrl, O, kw in steps:
    r, n = run(D, ctrl, O, **kw); rows.append({'step': name, 'n_test': n, **{k: round(v, 1) for k, v in r.items()}})
out = pd.DataFrame(rows).set_index('step')
pd.set_option('display.width', 250); print(out.to_string())
# per-origin view of the cleanest comparison
print('\nPer-origin MSE gain (%), eci_binary: Will spec vs Julia-like spec')
for T in ALL_O:
    a, _ = run(Dc, W_CTRL, [T]); b, _ = run(Dp, J_CTRL, [T], period_fe=True, train_std=True)
    print(T, round(a['eci_binary'], 1), round(b['eci_binary'], 1), '| atlas', round(a['eci_atlas_published'], 1), round(b['eci_atlas_published'], 1))
print('\ncorr(resource_share, eci_binary) by start year:', Dc.groupby('start').apply(lambda g: g.resource_share.corr(g.eci_binary)).round(2).to_dict())
out.to_csv('/Users/wbetts/eci-research/willbetts/forecast-reconciliation/outputs/steps_will_to_julia.csv')
