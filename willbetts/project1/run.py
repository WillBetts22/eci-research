"""Project 1: does ECI predict 10-year growth, controlling for income? (willbetts/ECI_growth_prediction.md)

Builds on Maitree's merged answer (maitreemody/eci_growth/, PR #6) and does three things it left open:

A. The Atlas's own resource control. Maitree used WDI resource rents (coefficient ~0) and flagged, untested,
   that the Atlas's "increase in natural-resource exports, constant $, share of initial GDP" might explain her
   smaller R^2 gain (+0.105 vs published +0.181). We build that control from Growth Lab SITC 2-digit data and
   rerun the Atlas decades (1978/88/98), then the five decades 1974-2014.
B. Reconcile the two lab answers on the most recent decade: Maitree finds 1.12 per SD for 2014-24 ("one weak
   decade, then it comes back"), the nightly Q12 run found 0.44 for 2013-23 ("it fades"). We move from her
   spec to Q12's one switch at a time.
C. Re-run the decade-by-decade and ECI x income checks with the Atlas control, since the 2004-14 dip is
   attributed to the commodity boom, which is exactly what that control measures.

Pre-stated metric: ECI coefficient (pp/yr of real GDPpc growth per 1 SD of ECI, SD within decade), its p-value
(country-clustered for pooled, HC1 for cross-sections), and the increase in R^2 from adding ECI.
Everything printed here is saved to results.json.
"""
import json, sys, warnings
from pathlib import Path
import numpy as np, pandas as pd
import statsmodels.formula.api as smf
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
FIG = HERE / 'figures'; FIG.mkdir(exist_ok=True)
cy = pd.read_csv(HERE / 'data' / 'derived' / 'country_year_p1.csv')
res = {}


def window(starts, length=10, eci='eci_sitc', gdp='gdppc_const_usd', nr='nr_core', min_pop=1e6, min_exports=None):
    idx = cy.set_index(['iso3', 'year'])
    rows = []
    for s in starts:
        e = s + length
        a = cy[cy.year == s].set_index('iso3'); b = cy[cy.year == e].set_index('iso3')
        w = pd.DataFrame(index=a.index)
        w['start'] = s
        w['growth'] = 100 * (np.log(b[gdp].reindex(w.index)) - np.log(a[gdp])) / length
        w['lny0'] = np.log(a[gdp])
        w['eci'] = a[eci]
        w['population'] = a.population; w['exports'] = a.exports_sitc
        w['region'] = a.region; w['name'] = a.name
        span = cy[(cy.year >= s) & (cy.year < e)]
        w['rents_avg'] = span.groupby('iso3').resource_rents_pct_gdp.mean().reindex(w.index)
        w['rents_start'] = a.resource_rents_pct_gdp
        # Atlas control: increase in NR exports over the decade, constant US$, as % of initial nominal GDP
        nr_end_real = b[nr].reindex(w.index) * a.us_deflator / b.us_deflator.reindex(w.index)
        w['nr_increase'] = 100 * (nr_end_real - a[nr]) / a.gdp_current_usd
        w['nr_share_start'] = a[nr] / a.exports_sitc2_total
        rows.append(w.reset_index())
    W = pd.concat(rows, ignore_index=True)
    W = W[W.population >= min_pop]
    if min_exports:
        W = W[W.exports >= min_exports]
    return W


def z(W, cols=('eci',)):
    W = W.copy()
    for c in cols:
        g = W.groupby('start')[c]; W[c] = (W[c] - g.transform('mean')) / g.transform('std')
    return W


def fit(D, f, cluster=True):
    if cluster and D.start.nunique() > 1:
        return smf.ols(f, D).fit(cov_type='cluster', cov_kwds={'groups': pd.factorize(D.iso3)[0]})
    return smf.ols(f, D).fit(cov_type='HC1')


def compare(W, ctrl, label, fe=True):
    D = z(W.dropna(subset=['growth', 'lny0', 'eci'] + ctrl))
    rhs = ' + '.join(['lny0'] + ctrl) + (' + C(start)' if fe and D.start.nunique() > 1 else '')
    b = fit(D, f'growth ~ {rhs}'); m = fit(D, f'growth ~ {rhs} + eci')
    return {'spec': label, 'n': int(m.nobs), 'countries': int(D.iso3.nunique()),
            'adj_r2_base': b.rsquared_adj, 'adj_r2_eci': m.rsquared_adj, 'delta_adj_r2': m.rsquared_adj - b.rsquared_adj,
            'delta_r2': m.rsquared - b.rsquared, 'eci_coef': m.params['eci'], 'eci_se': m.bse['eci'], 'eci_p': m.pvalues['eci'],
            **{f'coef_{c}': m.params[c] for c in ctrl}, **{f'p_{c}': m.pvalues[c] for c in ctrl}}


def show(rows, title):
    t = pd.DataFrame(rows)
    print(f'\n== {title}'); print(t.round(3).to_string(index=False))
    return t


ATLAS = [1978, 1988, 1998]
def drop_atlas_outliers(W):
    return W[~(((W.iso3 == 'LBR') & (W.start == 1988)) | ((W.iso3 == 'ZWE') & (W.start == 1998)))]

# Atlas-like country set: population >= 1.2M and exports >= $1B in 2008 (Atlas 2013 ranks 128 such countries)
a08 = cy[cy.year == 2008]
ATLAS_SET = set(a08[(a08.population >= 1.2e6) & (a08.exports_sitc >= 1e9)].iso3)

# ---------------- A. Atlas replication with the Atlas's resource control ----------------
Wa = drop_atlas_outliers(window(ATLAS))
Wa_set = Wa[Wa.iso3.isin(ATLAS_SET)]
A = [
    {'spec': 'PUBLISHED Atlas 2013 Table 3.1.1', 'n': 301, 'adj_r2_base': 0.291, 'adj_r2_eci': 0.472,
     'delta_adj_r2': 0.181, 'eci_coef': 1.9},
    compare(Wa, ['rents_avg'], 'Maitree control (rents, decade avg), pop>=1M'),
    compare(Wa, ['nr_increase'], 'Atlas control (NR export increase), pop>=1M'),
    compare(Wa_set, ['nr_increase'], f'Atlas control, Atlas-like {len(ATLAS_SET)}-country set'),
    compare(Wa_set, ['rents_avg'], 'Maitree control, Atlas-like country set'),
    compare(drop_atlas_outliers(window(ATLAS, nr='nr_gold')).pipe(lambda d: d[d.iso3.isin(ATLAS_SET)]), ['nr_increase'], 'Atlas control incl. gold, Atlas-like set'),
    compare(drop_atlas_outliers(window(ATLAS, nr='nr_broad')).pipe(lambda d: d[d.iso3.isin(ATLAS_SET)]), ['nr_increase'], 'Atlas control incl. agriculture, Atlas-like set'),
    compare(Wa_set, ['nr_increase', 'rents_avg'], 'Both controls, Atlas-like set'),
]
res['A_atlas_replication'] = show(A, 'A. Atlas decades 1978/88/98').to_dict('records')
print('Atlas-like set size:', len(ATLAS_SET))

# ---------------- C. Five decades, decade-by-decade, interaction, with the Atlas control ----------------
DEC = [1974, 1984, 1994, 2004, 2014]
W5 = window(DEC)
CP = [compare(W5, ['rents_avg'], 'Maitree main (rents avg), 1974-2024'),
     compare(W5, ['nr_increase'], 'Atlas control, 1974-2024'),
     compare(W5[W5.iso3.isin(ATLAS_SET)], ['nr_increase'], 'Atlas control, Atlas-like set, 1974-2024')]
res['C_pooled'] = show(CP, 'C. Five decades pooled').to_dict('records')

per = []
for s in DEC:
    for ctrl, lab in [(['rents_avg'], 'rents'), (['nr_increase'], 'nr_increase')]:
        r = compare(W5[W5.start == s], ctrl, f'{s}-{s+10}')
        r['control'] = lab; per.append(r)
per = show(per, 'C. By decade (HC1)')[['spec', 'control', 'n', 'eci_coef', 'eci_se', 'eci_p', 'delta_r2']]
res['C_by_decade'] = per.to_dict('records')

fig, ax = plt.subplots(figsize=(6.4, 3.4))
for k, (lab, off, col) in enumerate([('rents', -0.1, '#888'), ('nr_increase', 0.1, '#1f5fa8')]):
    d = per[per.control == lab]; x = np.arange(len(d)) + off
    ax.errorbar(x, d.eci_coef, yerr=1.96 * d.eci_se, fmt='o', capsize=3, color=col,
                label={'rents': 'Control: resource rents (Maitree)', 'nr_increase': 'Control: NR export increase (Atlas)'}[lab])
ax.set_xticks(range(len(DEC))); ax.set_xticklabels([f'{s}-{s+10}' for s in DEC])
ax.axhline(0, color='k', lw=0.6); ax.set_ylabel('ECI coefficient\n(pp/yr per SD, 95% CI)'); ax.legend(fontsize=7, frameon=False)
fig.tight_layout(); fig.savefig(FIG / 'coef_by_decade.png', dpi=130)

Wi = z(W5.dropna(subset=['growth', 'lny0', 'eci', 'nr_increase']))
Wi['lny0c'] = Wi.lny0 - Wi.lny0.mean(); Wi['eci_x_income'] = Wi.eci * Wi.lny0c
inter = {}
for ctrl in ['rents_avg', 'nr_increase']:
    m = fit(Wi.dropna(subset=[ctrl]), f'growth ~ lny0 + {ctrl} + eci + eci_x_income + C(start)')
    inter[ctrl] = {'coef': m.params['eci_x_income'], 'se': m.bse['eci_x_income'], 'p': m.pvalues['eci_x_income'], 'n': int(m.nobs)}
Wa_i = z(Wa_set.dropna(subset=['growth', 'lny0', 'eci', 'nr_increase'])); Wa_i['eci_x_income'] = Wa_i.eci * (Wa_i.lny0 - Wa_i.lny0.mean())
m = fit(Wa_i, 'growth ~ lny0 + nr_increase + eci + eci_x_income + C(start)')
inter['atlas_decades_atlas_set'] = {'coef': m.params['eci_x_income'], 'se': m.bse['eci_x_income'], 'p': m.pvalues['eci_x_income'], 'n': int(m.nobs)}
res['C_interaction'] = inter
print('\n== C. ECI x log GDPpc (negative = matters more for poorer countries)'); print(pd.DataFrame(inter).T.round(3))

# ---------------- B. Reconcile Maitree 2014-24 vs nightly Q12 2013-23 ----------------
sp = pd.read_csv(REPO / 'willbetts/nightly/external-data/derived/score_panel.csv')[['iso3', 'year', 'resource_share']]
def recent(start, eci, rents, share, q12_sample, nr=False):
    W = window([start], eci=eci)
    W = W.merge(sp.rename(columns={'year': 'start'}), on=['iso3', 'start'], how='left')
    if q12_sample:
        W = W[W.resource_share.notna()]          # score_panel = exports >= $1B and pop >= 1M at start
    ctrl = [rents] + (['resource_share'] if share else []) + (['nr_increase'] if nr else [])
    return compare(W, ctrl, '')

M_KW = dict(start=2014, eci='eci_sitc', rents='rents_avg', share=False, q12_sample=False)
Q_KW = dict(start=2013, eci='eci_hs', rents='rents_start', share=True, q12_sample=True)
steps = [('Maitree: 2014-24, SITC ECI, rents avg, pop>=1M', M_KW),
         ('+ start 2013 (ends 2023)', dict(M_KW, start=2013)),
         ('+ HS ECI', dict(M_KW, start=2013, eci='eci_hs')),
         ('+ start-year rents', dict(M_KW, start=2013, eci='eci_hs', rents='rents_start')),
         ('+ Q12 sample (exports >= $1B)', dict(Q_KW, share=False)),
         ('+ resource export share = Q12 spec', Q_KW)]
B = []
for lab, kw in steps:
    r = recent(**kw); r['spec'] = lab; B.append(r)
for lab, change in [('only start 2013', dict(start=2013)), ('only HS ECI', dict(eci='eci_hs')),
                    ('only start-year rents', dict(rents='rents_start')), ('only Q12 sample', dict(q12_sample=True)),
                    ('only Q12 sample + resource share', dict(q12_sample=True, share=True))]:
    r = recent(**dict(M_KW, **change)); r['spec'] = f'Maitree spec, {lab}'; B.append(r)
for lab, change in [('without resource share', dict(share=False)), ('with SITC ECI', dict(eci='eci_sitc')),
                    ('with 2014 start', dict(start=2014)), ('with Atlas NR-increase control added', dict(nr=True)),
                    ('resource share swapped for Atlas NR-increase', dict(share=False, nr=True))]:
    r = recent(**dict(Q_KW, **change)); r['spec'] = f'Q12 spec, {lab}'; B.append(r)
for s in range(2010, 2015):
    for e in ['eci_sitc', 'eci_hs']:
        r = recent(s, e, 'rents_avg', False, False); r['spec'] = f'start {s}, {e}, rents avg'; B.append(r)
res['B_reconcile'] = show(B, 'B. Recent decade: Maitree -> Q12, one switch at a time')[['spec', 'n', 'eci_coef', 'eci_se', 'eci_p', 'delta_r2']].to_dict('records')

# ---------------- what a bad start year does: 2013 vs 2014 influential countries ----------------
d13 = z(window([2013], eci='eci_sitc').dropna(subset=['growth', 'lny0', 'eci', 'rents_avg']))
d14 = z(window([2014], eci='eci_sitc').dropna(subset=['growth', 'lny0', 'eci', 'rents_avg']))
m13 = smf.ols('growth ~ lny0 + rents_avg + eci', d13).fit(); m14 = smf.ols('growth ~ lny0 + rents_avg + eci', d14).fit()
infl = []
for lab, d, m in [('2013', d13, m13), ('2014', d14, m14)]:
    dfb = m.get_influence().dfbetas[:, list(m.params.index).index('eci')]
    t = d.assign(dfbeta_eci=dfb).reindex(columns=['name', 'growth', 'eci', 'dfbeta_eci'])
    t = t.reindex(t.dfbeta_eci.abs().sort_values(ascending=False).index).head(6); t['start'] = lab
    infl.append(t)
infl = pd.concat(infl); print('\n== Most influential countries on the ECI coefficient (dfbeta)'); print(infl.round(3).to_string(index=False))
res['B_influence'] = infl.to_dict('records')

json.dump(res, open(HERE / 'results.json', 'w'), indent=1, default=float)
print('\nsaved results.json')
