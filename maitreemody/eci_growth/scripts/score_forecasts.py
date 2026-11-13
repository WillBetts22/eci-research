"""Project 2: score Growth Lab growth projections against realized growth, vs simple benchmarks.

Real-time test: the June 2019 edition's forecasts for base year 2017 (released 2019-06-03, before 2019-2024 was observed),
scored on realized 2017-2024 growth. Benchmarks use only data through 2017 (but today's revised vintage of that data):
  naive         every country grows at the 2007-2017 mean of the fitting sample (population >= 1M)
  persistence   each country repeats its own 2007-2017 growth
  income only   growth(2007-17) ~ lny0(2007), applied to 2017 values (the spec's convergence benchmark)
  convergence   same plus resource rents
  income+ECI    same plus Atlas SITC ECI(2007), applied to 2017 values (our own simple complexity model)
Rents: the model is fitted on each country's mean rents over 2007-2016 and applied to its mean over the available years
in 2008-2017 (same definition; Venezuela's WDI rents stop in 2014, so it uses 2008-2014).
"Naive" is the unweighted mean across countries, not a GDP-weighted world average.
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

import panel as P
from vintages import load_vintages

BENCH = ['naive', 'persistence', 'income only', 'convergence', 'income+ECI']


def realized(cy, s, e, kind='pc'):
    a = cy[cy.year == s].set_index('iso3')
    b = cy[cy.year == e].set_index('iso3')
    y0, y1 = a.gdppc_const_usd, b.gdppc_const_usd.reindex(a.index)
    if kind == 'total':
        y0, y1 = y0 * a.population, y1 * b.population.reindex(a.index)
    return P.ann_growth(y0, y1, e - s).rename(f'g_{kind}')


def tercile(s):
    return pd.qcut(s.rank(method='first'), 3, labels=False)


def scores(pred, actual):
    d = pd.concat([pred.rename('p'), actual.rename('a')], axis=1).dropna()
    const = d.p.nunique() <= 1   # a constant forecast has no ranking
    return {'n': len(d), 'pearson': np.nan if const else d.p.corr(d.a),
            'spearman': np.nan if const else stats.spearmanr(d.p, d.a)[0],
            'mae': (d.p - d.a).abs().mean(), 'rmse': np.sqrt(((d.p - d.a) ** 2).mean()),
            'bias': (d.p - d.a).mean(), 'tercile_hit': np.nan if const else (tercile(d.p) == tercile(d.a)).mean()}


def window_mean(cy, col, lo, hi):
    """Mean of the non-missing values of `col` per country with lo < year <= hi."""
    return cy[(cy.year > lo) & (cy.year <= hi)].groupby('iso3')[col].mean()


def benchmarks(cy, base, lookback=10):
    """Per-capita forecasts for base..base+10 that use only data through `base`.
    Returns (forecasts, index of the fitting sample)."""
    s0 = base - lookback
    a0 = cy[cy.year == s0].set_index('iso3')
    a1 = cy[cy.year == base].set_index('iso3')
    past = realized(cy, s0, base).rename('growth').to_frame()
    past['lny0'] = np.log(a0.gdppc_const_usd)
    past['rents'] = cy[(cy.year >= s0) & (cy.year < base)].groupby('iso3').resource_rents_pct_gdp.mean()
    past['eci'] = a0.eci_sitc
    past = past[a0.population.reindex(past.index) >= 1e6].dropna()
    now = pd.DataFrame({'lny0': np.log(a1.gdppc_const_usd), 'eci': a1.eci_sitc,
                        'rents': window_mean(cy, 'resource_rents_pct_gdp', s0, base)})
    out = pd.DataFrame(index=a1.index)
    out['naive'] = past.growth.mean()
    out['persistence'] = realized(cy, s0, base)
    out['income only'] = smf.ols('growth ~ lny0', past).fit().predict(now)
    out['convergence'] = smf.ols('growth ~ lny0 + rents', past).fit().predict(now)
    out['income+ECI'] = smf.ols('growth ~ lny0 + rents + eci', past).fit().predict(now)
    return out, past.index


def to_total(B, fit_idx, cy, base, lookback=10):
    """Convert per-capita benchmarks to total-GDP terms by adding each country's population growth over the
    lookback window (known at forecast time). Naive = mean total growth of the same fitting sample."""
    a0 = cy[cy.year == base - lookback].set_index('iso3').population
    a1 = cy[cy.year == base].set_index('iso3').population
    popg = P.ann_growth(a0, a1.reindex(a0.index), lookback)
    T = B.add(popg.reindex(B.index), axis=0)
    T['persistence'] = realized(cy, base - lookback, base, 'total')
    T['naive'] = T['persistence'].reindex(fit_idx).mean()
    return T


def realtime_frame(cy, V, base=2017, end=2024, kind='total', vintage='v1.0_2019-06-03', log_forecast=False):
    """One row per country: Growth Lab forecast, every benchmark, realized growth. Keeps every country that has
    a forecast and realized growth; benchmarks may be NaN for a few (reported, not silently dropped)."""
    gl = V[(V.vintage == vintage) & (V.base_year == base)].set_index('iso3').growth_proj
    if log_forecast:  # treat growth_proj as a compound annual rate and convert to a log rate like `realized`
        gl = 100 * np.log1p(gl / 100)
    Bpc, fit_idx = benchmarks(cy, base)
    B = Bpc if kind == 'pc' else to_total(Bpc, fit_idx, cy, base)
    act = realized(cy, base, end, kind)
    D = pd.concat([gl.rename('Growth Lab (2019 edition)'), B.reindex(gl.index), act.reindex(gl.index).rename('actual')], axis=1)
    return D  # rows with any NaN are reported by dropped() and excluded by scorecard()/paired_tests()


def dropped(D):
    """Countries with a forecast that cannot be scored, and why."""
    bad = D[D.isna().any(axis=1)]
    return {iso: [c for c in D.columns if pd.isna(r[c])] for iso, r in bad.iterrows()}


def scorecard(D):
    cols = [c for c in D.columns if c != 'actual']
    common = D.dropna().index
    return pd.DataFrame([{'forecast': c, **scores(D.loc[common, c], D.loc[common, 'actual'])} for c in cols]).set_index('forecast')


def paired_tests(D, exclude=()):
    """Growth Lab error minus each benchmark's error, per country (negative = Growth Lab better).
    Assumes per-country loss differences are independent; common shocks (Covid) make p-values optimistic."""
    D = D.dropna().drop(index=list(exclude), errors='ignore')
    gl = D['Growth Lab (2019 edition)']
    rows = []
    for c in BENCH:
        ea, eb = (gl - D.actual).abs(), (D[c] - D.actual).abs()
        da, ds = ea - eb, ea ** 2 - eb ** 2
        rows.append({'benchmark': c, 'n': len(D), 'mean |err| diff': da.mean(), 'p (abs, t-test)': stats.ttest_1samp(da, 0).pvalue,
                     'p (abs, Wilcoxon)': stats.wilcoxon(da).pvalue,
                     'mean sq err diff': ds.mean(), 'p (squared, t-test)': stats.ttest_1samp(ds, 0).pvalue})
    return pd.DataFrame(rows)


def revisions(V):
    """Compare consecutive editions for every base year: one row per (edition pair, base year) whose VALUES changed.
    Countries added to or removed from an edition are not counted here (see coverage_changes)."""
    order = V.drop_duplicates('vintage').sort_values(['release_date', 'vintage']).vintage.tolist()
    W = V.pivot_table(index=['iso3', 'base_year'], columns='vintage', values='growth_proj')[order]
    rows = []
    for a, b in zip(order, order[1:]):
        d = (W[b] - W[a]).dropna().abs()
        for y, g in d.groupby(level='base_year'):
            if (g > 1e-6).any():
                rows.append({'from': a, 'to': b, 'base_year': y, 'countries changed': int((g > 1e-6).sum()),
                             'mean |change|': g[g > 1e-6].mean(), 'max |change|': g.max()})
    return pd.DataFrame(rows), order


def coverage_changes(V, order):
    """Country-base-year rows that appear in or disappear from consecutive editions."""
    keys = {v: set(map(tuple, V[V.vintage == v][['iso3', 'base_year']].values)) for v in order}
    rows = []
    for a, b in zip(order, order[1:]):
        added, removed = keys[b] - keys[a], keys[a] - keys[b]
        if added or removed:
            rows.append({'from': a, 'to': b, 'rows added': len(added), 'rows removed': len(removed),
                         'removed (examples)': sorted(removed)[:4]})
    return pd.DataFrame(rows)


def main():
    cy = pd.read_csv(P.DERIVED / 'country_year.csv')
    V = load_vintages()
    res = {}
    res['realtime_total'] = realtime_frame(cy, V, kind='total')
    res['realtime_pc'] = realtime_frame(cy, V, kind='pc')
    res['precovid_total'] = realtime_frame(cy, V, end=2019, kind='total')
    res['realtime_total_log'] = realtime_frame(cy, V, kind='total', log_forecast=True)
    rows = []
    for vint in ['v1.0_2019-06-03']:
        for b in range(2004, 2015):
            p = V[(V.vintage == vint) & (V.base_year == b)].set_index('iso3').growth_proj
            for kind in ['pc', 'total']:
                rows.append({'base_year': b, 'outcome': kind, **scores(p, realized(cy, b, b + 10, kind))})
    res['backcasts'] = pd.DataFrame(rows)
    res['revisions'], res['vintage_order'] = revisions(V)
    res['coverage'] = coverage_changes(V, res['vintage_order'])
    return res


if __name__ == '__main__':
    pd.set_option('display.width', 200)
    r = main()
    for k in ['realtime_total', 'precovid_total']:
        print('==', k); print(scorecard(r[k]).round(3)); print(paired_tests(r[k]).round(3))
    print(r['revisions'].round(3))
