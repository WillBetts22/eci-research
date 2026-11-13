"""Project 2, step 5: rolling-origin (out-of-time) evaluation of the Project 1 regression.

For each origin T in 1984, 1994, 2004, 2014:
  - training data: every decade window that ENDED by T (starts 1974 .. T-10), so nothing after T is used;
  - forecast: growth over T..T+10 from values observed at T;
  - score against realized T..T+10 growth (2014 origin ends in 2024, the last data year).
Models (all fitted on the training windows only, with decade fixed effects):
  naive        the most recent training decade's mean growth (no country information)
  persistence  each country's own growth over T-10..T
  income only  growth ~ log GDPpc
  convergence  growth ~ log GDPpc + resource rents
  +ECI         growth ~ log GDPpc + resource rents + ECI
  +diversity   growth ~ log GDPpc + resource rents + diversity (simple-count comparison)
Forecasts use the most recent training decade's fixed effect as the common growth term (the Atlas's own
forecasting assumption: next decade's world shock = last decade's). Each model estimates its own decade effects, so
this choice moves each model's error level differently and can change out-of-sample R²; common='mean' uses the
average training decade effect instead, and score_demeaned() removes levels entirely (ranking-only skill).
Regressors are ex ante: rents = mean of available years in [s-2, s]; ECI and diversity standardized within each
decade using that decade's start-year cross-section.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

import panel as P

STARTS = [1974, 1984, 1994, 2004, 2014]
ORIGINS = [1984, 1994, 2004, 2014]
MODELS = {'income only': 'lny0', 'convergence': 'lny0 + rents', '+ECI': 'lny0 + rents + eci',
          '+diversity': 'lny0 + rents + diversity'}


def decade_panel(cy, eci='eci_sitc', min_pop=1e6, min_exports=None):
    """One row per country x decade with ex-ante regressors and realized growth."""
    W = P.window_panel(cy, STARTS, eci=eci, min_pop=min_pop, min_exports=min_exports, rents_avg=False)
    r = []
    for s in STARTS:
        x = cy[(cy.year >= s - 2) & (cy.year <= s)].groupby('iso3').resource_rents_pct_gdp.mean()
        r.append(pd.DataFrame({'iso3': x.index, 'start': s, 'rents_ex': x.values}))
    W = W.merge(pd.concat(r), on=['iso3', 'start'], how='left')
    W['rents'] = W.rents_ex
    W = P.zscore_by(W, ['eci', 'diversity'])
    # persistence: own growth over the previous decade (needs GDP at s-10, available from 1964)
    prev = cy[['iso3', 'year', 'gdppc_const_usd']].rename(columns={'year': 'start', 'gdppc_const_usd': 'y_prev'})
    prev['start'] = prev.start + 10
    W = W.merge(prev, on=['iso3', 'start'], how='left')
    W['persistence'] = P.ann_growth(W.y_prev, W.y0, 10)
    return W


def forecast(W, T, train_mode='expanding', common='last', require_persistence=True):
    """Fit on windows ending by T (all of them, or only the last one if train_mode='last'), forecast the window
    starting at T. Returns a frame of forecasts + actual."""
    need = ['growth', 'lny0', 'rents', 'eci', 'diversity']
    train = W[(W.start + 10 <= T)].dropna(subset=need)
    if train_mode == 'last':
        train = train[train.start == train.start.max()]
    test = W[W.start == T].dropna(subset=need + (['persistence'] if require_persistence else [])).set_index('iso3')
    last = train.start.max()
    out = pd.DataFrame(index=test.index)
    out['naive'] = train[train.start == last].growth.mean()
    out['persistence'] = test.persistence
    for name, rhs in MODELS.items():
        m = smf.ols(f'growth ~ {rhs} + C(start)', train).fit()
        if common == 'last':
            out[name] = m.predict(test.assign(start=last))
        else:  # average of the training decades' effects
            out[name] = np.mean([m.predict(test.assign(start=s)) for s in sorted(train.start.unique())], axis=0)
    out['actual'] = test.growth
    out['origin'] = T
    out['n_train'] = len(train)
    out['name'] = test.name
    return out


def score_origin(F, models):
    rows = []
    for c in models:
        const = F[c].nunique() <= 1
        e = F[c] - F.actual
        rows.append({'model': c, 'n': len(F), 'pearson': np.nan if const else F[c].corr(F.actual),
                     'spearman': np.nan if const else stats.spearmanr(F[c], F.actual)[0],
                     'mae': e.abs().mean(), 'rmse': np.sqrt((e ** 2).mean()), 'bias': e.mean()})
    return pd.DataFrame(rows)


def oos_r2(F, model, base):
    """Out-of-sample R² of `model` relative to `base`: 1 - SSE(model)/SSE(base)."""
    return 1 - ((F[model] - F.actual) ** 2).sum() / ((F[base] - F.actual) ** 2).sum()


def paired_vs(F, a, b):
    """Pooled paired test of squared and absolute errors, a minus b, clustered by country."""
    d = pd.DataFrame({'iso3': F.index, 'sq': (F[a] - F.actual) ** 2 - (F[b] - F.actual) ** 2,
                      'ab': (F[a] - F.actual).abs() - (F[b] - F.actual).abs()})
    g = pd.factorize(d.iso3)[0]
    sq = smf.ols('sq ~ 1', d).fit(cov_type='cluster', cov_kwds={'groups': g})
    ab = smf.ols('ab ~ 1', d).fit(cov_type='cluster', cov_kwds={'groups': g})
    return {'compare': f'{a} vs {b}', 'n': len(d), 'mean sq diff': sq.params['Intercept'], 'p (sq)': sq.pvalues['Intercept'],
            'mean abs diff': ab.params['Intercept'], 'p (abs)': ab.pvalues['Intercept']}


def main(eci='eci_sitc', train_mode='expanding', min_exports=None, common='last', require_persistence=True):
    cy = pd.read_csv(P.DERIVED / 'country_year.csv')
    W = decade_panel(cy, eci=eci, min_exports=min_exports)
    F = pd.concat([forecast(W, T, train_mode, common, require_persistence) for T in ORIGINS])
    models = (['naive', 'persistence'] if require_persistence else ['naive']) + list(MODELS)
    per = pd.concat([score_origin(F[F.origin == T], models).assign(origin=T) for T in ORIGINS])
    per['oos R2 vs convergence'] = [oos_r2(F[F.origin == T], m, 'convergence') for T, m in zip(per.origin, per.model)]
    pooled = score_origin(F, models)
    pooled['oos R2 vs convergence'] = [oos_r2(F, m, 'convergence') for m in models]
    pooled['share of origins better than convergence'] = [
        np.mean([oos_r2(F[F.origin == T], m, 'convergence') > 0 for T in ORIGINS]) for m in models]
    tests = pd.DataFrame([paired_vs(F, '+ECI', b) for b in ['convergence', 'income only', 'naive', '+diversity']
                          + (['persistence'] if require_persistence else [])])
    return {'forecasts': F, 'per_origin': per, 'pooled': pooled, 'tests': tests}


def score_demeaned(F, model, base):
    """Ranking-only out-of-sample R²: demean forecasts and outcomes within each origin, then compare SSE."""
    G = F.copy()
    for c in [model, base, 'actual']:
        G[c] = G[c] - G.groupby('origin')[c].transform('mean')
    return oos_r2(G, model, base)


def trimmed_oos(F, model, base, k):
    """OOS R² after dropping the k cases with the largest |squared-error difference| (either sign)."""
    d = ((F[model] - F.actual) ** 2 - (F[base] - F.actual) ** 2).abs().reset_index(drop=True)
    keep = d.sort_values().index[:len(d) - k]
    return oos_r2(F.reset_index().loc[keep], model, base)


def top_contributors(F, model, base, n=8):
    """Country-decades that contribute most to the squared-error gain of `model` over `base`."""
    G = F.reset_index().assign(gain=lambda d: (d[base] - d.actual) ** 2 - (d[model] - d.actual) ** 2)
    G['share of total gain'] = G.gain / G.gain.sum()
    return G.sort_values('gain', ascending=False)[['iso3', 'name', 'origin', 'actual', base, model, 'gain', 'share of total gain']].head(n)


def q16_like(cy, eci='eci_sitc', year_fe=False):
    """Our data in the nightly Q16 design: annual 10-year windows, test origins 2005-2014 each trained on origins
    <= T-10 (from 1995), pooled OLS (no time effects unless year_fe), $1B export and 1M population filters,
    start-year rents. Q16 also controlled for resource export share, which we do not have."""
    W = P.window_panel(cy, list(range(1995, 2015)), eci=eci, min_exports=1e9, rents_avg=False)
    W = P.zscore_by(W, ['eci']).dropna(subset=['growth', 'lny0', 'rents', 'eci'])
    fe = ' + C(start)' if year_fe else ''
    sse_b = sse_m = 0.0
    for T in range(2005, 2015):
        tr, te = W[W.start <= T - 10], W[W.start == T]
        for rhs, acc in [('lny0 + rents', 'b'), ('lny0 + rents + eci', 'm')]:
            m = smf.ols(f'growth ~ {rhs}{fe}', tr).fit()
            pred = m.predict(te.assign(start=tr.start.max())) if year_fe else m.predict(te)
            e = ((pred - te.growth) ** 2).sum()
            if acc == 'b': sse_b += e
            else: sse_m += e
    return 1 - sse_m / sse_b


if __name__ == '__main__':
    pd.set_option('display.width', 220); pd.set_option('display.max_columns', 20)
    r = main()
    print(r['forecasts'].groupby('origin').agg(n=('actual', 'size'), n_train=('n_train', 'first')))
    print(r['per_origin'].round(3).to_string(index=False))
    print(r['pooled'].round(3).to_string(index=False))
    print(r['tests'].round(4).to_string(index=False))
