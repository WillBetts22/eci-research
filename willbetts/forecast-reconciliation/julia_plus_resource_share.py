"""Reverse check: Julia's designs, scores and samples, plus Will's start-year resource export share (HS 26/27/71)."""
import sys, numpy as np, pandas as pd, statsmodels.api as sm, warnings
warnings.filterwarnings('ignore')
ROOT = '/Users/wbetts/eci-research'
sys.path.insert(0, ROOT + '/juliawang')
import project3_horse_race as J
scores = pd.read_csv(ROOT + '/juliawang/outputs/project3/full/all_measures.csv')
cy = pd.read_csv(ROOT + '/maitreemody/eci_growth/data/derived/country_year.csv')
rs = pd.read_csv(ROOT + '/willbetts/nightly/external-data/derived/score_panel.csv', usecols=['iso3','year','resource_share'])
W = {(s,h): J.window(scores, cy, s, h).merge(rs.rename(columns={'year':'start'}), on=['iso3','start'], how='left')
     for h in [5,10] for s in range(1995,2020) if s+h <= 2024}
designs = [('primary_1998_2008', W[1998,10], W[2008,10])]
for h, origins in [(10,[2005,2008,2014]), (5,[2005,2010,2015,2019])]:
    for o in origins:
        designs.append((f'rolling_h{h}_{o}', pd.concat([w for (s,k),w in W.items() if k==h and s+h<=o]), W[o,h]))
MS = ['eci_hs4','eci_harvard','diversity','entropy','eci_groups18_goods']
def race(tr, te, ctrl):
    need = ['growth','income','rents','resource_share'] + J.MEASURES   # same complete-case sample for both specs
    tr, te = tr.dropna(subset=need), te.dropna(subset=need); out = {}
    for name, extra in ({'baseline':[]} | {m:[m] for m in MS}).items():
        cols = ctrl + extra; m, s = tr[cols].mean(), tr[cols].std(ddof=0)
        xt = sm.add_constant((tr[cols]-m)/s, has_constant='add'); xv = sm.add_constant((te[cols]-m)/s, has_constant='add')
        for y in sorted(tr.start.unique())[1:]:
            ind = (tr.start==y).astype(float); xt[f'p{y}'] = ind-ind.mean(); xv[f'p{y}'] = 0.
        p = sm.OLS(tr.growth, xt).fit().predict(xv); out[name] = np.mean((te.growth.to_numpy()-p.to_numpy())**2)
    return {k: round(100*(1-v/out['baseline']),1) for k,v in out.items() if k!='baseline'}, len(te)
rows=[]
for lab,tr,te in designs:
    a,n = race(tr,te,['income','rents']); b,_ = race(tr,te,['income','rents','resource_share'])
    rows.append({'design':lab,'n_test':n, **{f'{k} | J':v for k,v in a.items()}, **{f'{k} | J+RS':v for k,v in b.items()}})
out = pd.DataFrame(rows).set_index('design'); pd.set_option('display.width',300)
print(out[[c for c in out.columns if c.startswith(('eci_hs4','eci_harvard','diversity'))]].to_string())
print('\nDesigns where ECI-HS4 beats baseline: Julia spec', (out['eci_hs4 | J']>0).sum(), '/ 8; with resource share', (out['eci_hs4 | J+RS']>0).sum(), '/ 8')
out.to_csv('/Users/wbetts/eci-research/willbetts/forecast-reconciliation/outputs/julia_plus_resource_share.csv')
