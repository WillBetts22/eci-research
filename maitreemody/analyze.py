"""Do countries with higher ECI have higher GDP per capita?

Reproducible calculation from the repo's export data plus a saved World Bank
GDP-per-capita extract in outputs/. Run from the repo root: python3 maitreemody/analyze.py
Requires numpy, pandas, scipy, statsmodels, matplotlib, pycountry.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import linalg as LA

import pycountry

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUT = HERE / 'outputs'
YEARS = [2019, 2020, 2021, 2022]           # 2023 raw exports are inflated (KNOWN-ISSUES D1)
MIN_EXPORTS = 1e9                          # Atlas-style size filter
RESOURCE_CH = ['26', '27', '71']           # ores, fuels, precious stones/metals
AGGREGATES = {97, 899, 472, 129, 221, 290, 292, 527, 568, 577, 636, 637, 697, 838, 839, 849, 879}
SPECIAL_ISO3 = {842: 'USA', 757: 'CHE', 251: 'FRA', 579: 'NOR', 699: 'IND', 711: 'ZAF', 490: 'TWN'}

codes = pd.read_csv(REPO / 'data/archive/2022-fall/Country_Code.csv', encoding='latin-1').iloc[:, :2]
codes.columns = ['code', 'name']
codes['name'] = codes['name'].str.strip()
NAME2CODE = dict(zip(codes.name, codes.code.astype(int)))


def iso3(code):
    if code in SPECIAL_ISO3:
        return SPECIAL_ISO3[code]
    c = pycountry.countries.get(numeric=f'{int(code):03d}')
    return c.alpha_3 if c else None


def eci_from_exports(X):
    """Standard ECI (binary RCA >= 1), eigenvalues sorted, sign oriented to diversity."""
    X = X.loc[X.sum(axis=1) > 0, X.sum(axis=0) > 0]
    rca = X.div(X.sum(axis=1), axis=0) / (X.sum(axis=0) / X.to_numpy().sum())
    M = (rca >= 1).astype(float)
    M = M.loc[M.sum(axis=1) > 0, M.sum(axis=0) > 0]
    kc, kp = M.sum(axis=1).to_numpy(), M.sum(axis=0).to_numpy()
    B = M.to_numpy() / np.sqrt(kc[:, None] * kp[None, :])
    vals, vecs = np.linalg.eigh(B @ B.T)
    v = vecs[:, -2] / np.sqrt(kc)
    if np.corrcoef(v, kc)[0, 1] < 0:       # convention, not a finding
        v = -v
    return pd.DataFrame({'eci': (v - v.mean()) / v.std(), 'diversity': kc}, index=M.index)


def notebook_eci(X):
    """Replicates code/current/Spring2026.ipynb compute_eci: eig column 1, sign set by first row."""
    X = X.loc[(X > 0).all(axis=1)]          # df_to_matrix drops any country with a zero
    M = (X.div(X.sum(axis=1), axis=0) > X.sum(axis=0) / X.to_numpy().sum()).to_numpy(float)
    mcc = (M / M.sum(1, keepdims=True)) @ (M / M.sum(0, keepdims=True)).T
    v = LA.eig(mcc)[1][:, 1].real
    eci = (v - v.mean()) / v.std() if v[0] < 0 else (v.mean() - v) / v.std()
    return pd.Series(eci, index=X.index)


def load_hs4(year):
    raw = pd.read_csv(REPO / 'data/raw' / f'{year}_mega.csv', index_col=0)
    if 'commodity_code' in raw.columns:                         # 2019-2022 layout
        cmd = raw.pop('commodity_code')
    else:                                                       # 2023 layout: codes are the index
        cmd = pd.Series(raw.index, index=raw.index)
    cmd = cmd.astype(str).str.zfill(6)                          # 5-digit codes lost a leading zero
    raw = raw.apply(pd.to_numeric, errors='coerce').fillna(0)
    keep = ~cmd.str[:2].isin(['98', '99'])
    raw, cmd = raw[keep], cmd[keep]
    resource = raw[cmd.str[:2].isin(RESOURCE_CH)].sum() / raw.sum()
    X = raw.groupby(cmd.str[:4]).sum().T
    X.index = X.index.astype(int)
    resource.index = resource.index.astype(int)
    X = X.drop(index=[c for c in X.index if c in AGGREGATES])
    X = X.loc[X.sum(axis=1) >= MIN_EXPORTS]
    return X, resource


def load_groups(year):
    g = pd.read_csv(REPO / 'data/cleaned' / f'{year}clean.csv').set_index('Country')
    g.columns = g.columns.str.strip()
    g = g.drop(columns=['High-complexity Products'])           # overlaps other groups by design
    g.index = [NAME2CODE.get(n.strip()) for n in g.index]
    g = g.loc[[c is not None and c not in AGGREGATES for c in g.index]]
    return g.loc[g.sum(axis=1) >= MIN_EXPORTS]


def build():
    wb = pd.read_csv(OUT / 'worldbank_gdp_per_capita_2019_2023.csv')
    frames = []
    for y in YEARS + [2023]:
        X, resource = load_hs4(y)
        hs4 = eci_from_exports(X).add_suffix('_hs4')
        G = load_groups(y)
        grp = eci_from_exports(G).add_suffix('_grp')
        nb = notebook_eci(G).rename('eci_notebook')
        d = hs4.join(grp, how='outer').join(nb, how='outer')
        d['resource_share'] = resource.reindex(d.index)
        d['iso3'] = [iso3(c) for c in d.index]
        d['year'] = y
        frames.append(d)
    d = pd.concat(frames).merge(wb, on=['iso3', 'year'], how='inner')
    d['log_gdppc'] = np.log(d.gdppc_ppp)
    d['log_diversity'] = np.log(d.diversity_hs4)
    d['resource_dep'] = (d.resource_share >= 0.40).astype(float)
    return d.set_index(['year', 'name'])


def run():
    OUT.mkdir(exist_ok=True)
    d = build()
    d.to_csv(OUT / 'country_year_metrics.csv')
    lines = ['# Do countries with higher ECI have higher GDP per capita? — results\n']

    # 1. Rank correlations by year and measure
    rows = []
    for y in YEARS + [2023]:
        s = d.loc[y]
        for m, label in [('eci_hs4', 'ECI, HS4 products'), ('eci_grp', 'ECI, 17 groups (sign fixed)'),
                         ('eci_notebook', 'ECI, lab notebook as-is'), ('diversity_hs4', 'Diversity (HS4 RCA count)')]:
            t = s[[m, 'log_gdppc']].dropna()
            rows.append({'year': y, 'measure': label, 'n': len(t),
                         'spearman_rho': t[m].corr(t.log_gdppc, method='spearman')})
    corr = pd.DataFrame(rows)
    corr.to_csv(OUT / 'correlations.csv', index=False)
    lines += ['## 1. Spearman correlation with log GDP per capita (PPP)\n',
              corr.pivot(index='measure', columns='year', values='spearman_rho').round(2).to_markdown(), '',
              '2023 shown for completeness only: its raw export data is inflated (KNOWN-ISSUES D1).\n']

    # 2. Regressions, 2019 (primary year), common sample with both ECIs
    s = d.loc[2019].dropna(subset=['eci_hs4', 'eci_grp', 'log_gdppc', 'resource_share'])
    specs = [('A', 'log_gdppc ~ eci_hs4'), ('B', 'log_gdppc ~ eci_grp'),
             ('C', 'log_gdppc ~ log_diversity'), ('D', 'log_gdppc ~ eci_hs4 + log_diversity'),
             ('E', 'log_gdppc ~ eci_hs4 + resource_share'),
             ('F', 'log_gdppc ~ eci_hs4 * resource_dep')]
    reg_rows = []
    for k, f in specs:
        m = smf.ols(f, data=s).fit(cov_type='HC1')
        loo = np.sqrt(np.mean((m.resid / (1 - m.get_influence().hat_matrix_diag)) ** 2))
        reg_rows.append({'model': k, 'formula': f, 'n': int(m.nobs), 'r2': m.rsquared, 'loo_rmse': loo,
                         **{f'b[{p}]': f'{m.params[p]:+.2f} (p={m.pvalues[p]:.3f})' for p in m.params.index if p != 'Intercept'}})
    reg = pd.DataFrame(reg_rows)
    reg.to_csv(OUT / 'regressions_2019.csv', index=False)
    lines += ['## 2. Regressions, 2019, log GDP per capita (PPP), HC1 standard errors\n',
              f'Common sample: {len(s)} countries with both ECIs, World Bank data and ≥$1B exports.\n',
              reg.fillna('').to_markdown(index=False, floatfmt='.3f'), '',
              'A 1-unit (1 s.d.) ECI increase multiplies GDP per capita by exp(b). LOO RMSE is exact leave-one-country-out error in log points.\n']

    # 3. Outliers from model A
    m = smf.ols('log_gdppc ~ eci_hs4', data=s).fit()
    s = s.assign(resid=m.resid, richer_than_predicted=np.exp(m.resid))
    cols = ['eci_hs4', 'eci_grp', 'gdppc_ppp', 'resource_share', 'resid']
    lines += ['## 3. Largest departures from model A\n', '**Richer than their ECI predicts**\n',
              s.nlargest(10, 'resid')[cols].round(2).to_markdown(), '',
              '**Poorer than their ECI predicts**\n', s.nsmallest(10, 'resid')[cols].round(2).to_markdown(), '',
              f"Mean residual, resource-dependent (≥40% ores/fuels/precious metals): {s.loc[s.resource_dep == 1, 'resid'].mean():+.2f} "
              f"(n={int(s.resource_dep.sum())}); others: {s.loc[s.resource_dep == 0, 'resid'].mean():+.2f}.\n"]
    s.sort_values('resid')[cols].to_csv(OUT / '2019_residuals.csv')
    print('\n'.join(lines))
    return d


if __name__ == '__main__':
    run()
