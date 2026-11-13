"""Shared helpers for the 2026-11-12 all-questions batch (Q03-Q16).

Builds on ``eci.py``. Everything here is keyed on ISO3 so merges never depend on
country names (KNOWN-ISSUES D6).

Data sources
------------
* repo:     data/raw/<year>_mega.csv (Comtrade HS6, 2019-2023), data/cleaned/<year>clean.csv
* external: willbetts/nightly/external-data/raw/ (see external-data/README.md)
    - atlas_hs92_country_year.csv   Harvard Growth Lab published ECI, 1995-2024
    - atlas_hs4_exports.pkl         Growth Lab HS92 4-digit exports, 1995-2024 (compacted)
    - wdi_panel.csv                 World Bank WDI (GDPpc, population, rents, education, R&D...)
    - wgi_panel.csv                 Worldwide Governance Indicators, 1996-2022
    - pwt1001.dta                   Penn World Table 10.01 (to 2019)
"""
from __future__ import annotations

import json
import sys
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eci  # noqa: E402

REPO = eci.REPO
NIGHTLY = REPO / 'willbetts' / 'nightly'
EXT = NIGHTLY / 'external-data' / 'raw'
REPORT_COUNTRIES = {'CAN': 'Canada', 'DEU': 'Germany', 'POL': 'Poland', 'SGP': 'Singapore',
                    'ARE': 'UAE', 'GBR': 'UK', 'VNM': 'Vietnam'}

# Group -> HS chapters exactly as code/data-retrieval/datacleaning2025.ipynb cell 5.
LAB_GROUPS = {
    'Animals and By-products': [1, 2, 3, 4, 5, 16],
    'Vegetables, Fruits and Plants': [6, 7, 8, 9, 10, 11, 13, 14],
    'Food and Preparations': [12, 15, 17, 18, 19, 20, 21, 22, 23, 24],
    'Energy Drilling and Mining': [25, 26, 27],
    'Chemicals': [28, 29],
    'Chemical Manufacturing': [30, 31, 32, 33, 34, 35, 38],
    'Raw Manufacturing': [37, 39, 40, 41, 42, 43, 46, 69, 68],
    'Wood Products': [44, 45, 47, 48, 49],
    'Clothing and Accessories': [61, 62, 63, 64, 65, 66, 67],
    'Textile': [50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
    'Metals': [72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82],
    'Machinery and Construction': [83],
    'Transportation': [85, 86, 87, 88, 98],
    'Weapons': [92, 36],
    'Daily Instruments': [89, 90, 91, 93, 94, 95],
    'Precious Stones': [70, 71],
    'High-complexity Products': [28, 29, 30, 38, 83, 84, 87, 92, 99],
    'Services and Utilities': [99],
}


# --------------------------------------------------------------------------- io
def save_json(obj, path):
    def conv(o):
        if isinstance(o, (np.integer,)):
            return int(o)
        if isinstance(o, (np.floating,)):
            return None if np.isnan(o) else float(o)
        if isinstance(o, (np.bool_,)):
            return bool(o)
        if isinstance(o, (pd.Series,)):
            return o.to_dict()
        raise TypeError(type(o))
    Path(path).write_text(json.dumps(obj, indent=2, default=conv))


# --------------------------------------------------------------------------- repo trade data
@lru_cache(maxsize=None)
def raw_hs6(year: int) -> pd.DataFrame:
    """Raw Comtrade HS6 (rows = HS6 code str, cols = M49 int reporter). Chapters 98/99 kept."""
    raw = pd.read_csv(REPO / 'data/raw' / f'{year}_mega.csv', index_col=0)
    if 'commodity_code' in raw.columns:
        cmd = raw.pop('commodity_code')
    else:
        cmd = pd.Series(raw.index, index=raw.index)
    raw.index = cmd.astype(str).str.zfill(6).values
    raw = raw.apply(pd.to_numeric, errors='coerce').fillna(0.0)
    raw.columns = raw.columns.astype(int)
    return raw


def repo_hs(year: int, digits: int = 4, min_exports: float = 1e9, drop_chapters=('98', '99'),
            iso3: bool = True) -> pd.DataFrame:
    """Countries x HS products at ``digits`` (2/4/6) from data/raw, aggregates dropped."""
    raw = raw_hs6(year)
    keep = ~raw.index.str[:2].isin(list(drop_chapters))
    r = raw[keep]
    X = r.groupby(r.index.str[:digits]).sum().T
    X = X.drop(index=[c for c in X.index if c in eci.M49_AGGREGATES])
    X = X.loc[X.sum(axis=1) >= min_exports]
    if iso3:
        X.index = [eci.m49_to_iso3(c) for c in X.index]
        X = X.loc[X.index.notna()]
        X = X.groupby(level=0).sum()
    return X


def groups_from_raw(year: int, mapping: dict, min_exports: float = 0.0) -> pd.DataFrame:
    """Rebuild grouped exports from data/raw with a chapter mapping (countries x groups, ISO3)."""
    raw = raw_hs6(year)
    ch = raw.index.str[:2].astype(int)
    out = {}
    for g, chs in mapping.items():
        out[g] = raw[np.isin(ch, chs)].sum()
    X = pd.DataFrame(out)
    X = X.drop(index=[c for c in X.index if c in eci.M49_AGGREGATES])
    X.index = [eci.m49_to_iso3(c) for c in X.index]
    X = X.loc[pd.notna(X.index)].groupby(level=0).sum()
    X = X.loc[X.sum(axis=1) > min_exports]
    return X


def lab_groups_iso3(year: int, drop_aggregate: bool = False, drop_eu: bool = False) -> pd.DataFrame:
    """Cleaned 18-group CSV re-keyed on ISO3. EU-28 (no ISO3) is kept under 'EU28' unless drop_eu."""
    g = eci.load_groups(year, drop_aggregate=drop_aggregate, notebook_names=False)
    iso = eci.group_name_to_iso3(g.index)
    idx = [iso[n] if iso[n] is not None else ('EU28' if 'EU' in str(n) else None) for n in g.index]
    g.index = idx
    g = g.loc[pd.notna(g.index)]
    if drop_eu:
        g = g.drop(index=['EU28'], errors='ignore')
    return g.groupby(level=0).sum()


def unmapped_group_names(year: int):
    g = eci.load_groups(year, notebook_names=False)
    iso = eci.group_name_to_iso3(g.index)
    return [n for n in g.index if iso[n] is None]


def grouped_eci(year: int, lab_rules: bool = True, drop_aggregate=False, drop_eu=False, X=None):
    """Oriented grouped ECI. lab_rules = drop-any-zero filter + strict RCA (the notebook)."""
    if X is None:
        X = lab_groups_iso3(year, drop_aggregate=drop_aggregate, drop_eu=drop_eu)
    if lab_rules:
        X = eci.notebook_filter(X)
    e, p, d, M = eci.eci_from_exports(X, strict=lab_rules, return_all=True)
    return e, d


# --------------------------------------------------------------------------- external data
@lru_cache(maxsize=None)
def wdi() -> pd.DataFrame:
    return pd.read_csv(EXT / 'wdi_panel.csv')


@lru_cache(maxsize=None)
def wgi() -> pd.DataFrame:
    return pd.read_csv(EXT / 'wgi_panel.csv')


@lru_cache(maxsize=None)
def pwt() -> pd.DataFrame:
    d = pd.read_stata(EXT / 'pwt1001.dta', columns=['countrycode', 'year', 'rgdpe', 'rgdpna', 'pop', 'hc'])
    d = d.rename(columns={'countrycode': 'iso3'})
    d['gdppc_pwt'] = d.rgdpe / d['pop']
    return d


@lru_cache(maxsize=None)
def atlas_cy() -> pd.DataFrame:
    d = pd.read_csv(EXT / 'atlas_hs92_country_year.csv')
    return d.rename(columns={'country_iso3_code': 'iso3'})


@lru_cache(maxsize=None)
def atlas_hs4_long() -> pd.DataFrame:
    return pd.read_pickle(EXT / 'atlas_hs4_exports.pkl')


def atlas_hs4(year: int, min_exports: float = 1e9, min_pop: float | None = 1e6,
              drop_services: bool = True) -> pd.DataFrame:
    """Countries x HS4 from the Growth Lab panel for one year (ISO3 index).

    Mirrors the Atlas ranking sample: total exports >= ``min_exports`` and population >= ``min_pop``.
    Non-HS service codes (non-numeric) are dropped when ``drop_services``.
    """
    d = atlas_hs4_long()
    d = d[d.year == year]
    X = d.pivot_table(index='iso3', columns='hs4', values='export_value', aggfunc='sum', observed=True).fillna(0.0)
    X.index = X.index.astype(str)
    X.columns = X.columns.astype(str)
    if drop_services:
        X = X.loc[:, [c for c in X.columns if c.isdigit()]]
    X = X.loc[X.sum(axis=1) >= min_exports]
    if min_pop:
        pop = wdi().query('year == @year').set_index('iso3').population
        X = X.loc[[c for c in X.index if pop.get(c, 0) >= min_pop]]
    return X


def gdppc(year: int, kind: str = 'ppp') -> pd.Series:
    """log-able GDP per capita by ISO3 from WDI: 'ppp' (constant intl $), 'const' (constant 2015 US$), 'current'."""
    col = {'ppp': 'gdppc_ppp_const', 'const': 'gdppc_const2015usd', 'current': 'gdppc_current_usd'}[kind]
    w = wdi()
    return w.loc[w.year == year].set_index('iso3')[col].dropna()


def growth(y0: int, y1: int, kind: str = 'const') -> pd.Series:
    """Annualized log growth of GDP per capita (WDI) between y0 and y1, in % per year."""
    a, b = gdppc(y0, kind), gdppc(y1, kind)
    idx = a.index.intersection(b.index)
    return (np.log(b[idx] / a[idx]) / (y1 - y0) * 100).rename('growth')


def resource_share(X: pd.DataFrame) -> pd.Series:
    """Share of exports in HS chapters 26, 27, 71 (ores, fuels, precious stones/metals)."""
    cols = [c for c in X.columns if str(c)[:2] in ('26', '27', '71')]
    return (X[cols].sum(axis=1) / X.sum(axis=1)).rename('resource_share')


# --------------------------------------------------------------------------- complexity variants
def eci_weighted(W: pd.DataFrame, orient_to: pd.Series | None = None) -> pd.Series:
    """ECI from a non-negative (possibly continuous) country x product matrix W.

    Same spectral construction as eci.eci_pci (Mcc = D_c^-1 W D_p^-1 W^T), so a binary W
    gives the standard ECI. Oriented to correlate positively with ``orient_to``
    (default: binary-RCA diversity of W>0 rows, i.e. row sums).
    """
    W = W.loc[W.sum(axis=1) > 0, W.sum(axis=0) > 0]
    Wv = W.to_numpy(float)
    kc, kp = Wv.sum(1), Wv.sum(0)
    B = Wv / np.sqrt(kc[:, None] * kp[None, :])
    U, S, Vt = np.linalg.svd(B, full_matrices=False)
    k = U[:, 1] / np.sqrt(kc)
    ref = orient_to.reindex(W.index).to_numpy() if orient_to is not None else kc
    if np.corrcoef(k, ref)[0, 1] < 0:
        k = -k
    return pd.Series((k - k.mean()) / k.std(), index=W.index, name='eci')


def fitness(M: pd.DataFrame, n_iter: int = 200, tol: float = 1e-10) -> pd.Series:
    """Tacchella et al. (2012) Fitness-Complexity on binary M. Returns log10 fitness (mean-normalised)."""
    Mv = M.to_numpy(float)
    F = np.ones(Mv.shape[0])
    Q = np.ones(Mv.shape[1])
    for _ in range(n_iter):
        Fn = Mv @ Q
        with np.errstate(divide='ignore'):
            Qn = 1.0 / (Mv.T @ (1.0 / F))
        Fn, Qn = Fn / Fn.mean(), Qn / Qn.mean()
        done = np.max(np.abs(Fn - F)) < tol
        F, Q = Fn, Qn
        if done:
            break
    return pd.Series(np.log10(np.maximum(F, 1e-300)), index=M.index, name='log_fitness')


def entropy(X: pd.DataFrame) -> pd.Series:
    s = X.div(X.sum(axis=1), axis=0).to_numpy()
    with np.errstate(divide='ignore', invalid='ignore'):
        h = -np.nansum(np.where(s > 0, s * np.log(s), 0.0), axis=1)
    return pd.Series(h, index=X.index, name='entropy')


def rca_variants(X: pd.DataFrame) -> dict:
    """Dict of country x product matrices: binary, log1p, capped (at 2), percentile."""
    R = eci.rca(X)
    return {
        'binary RCA>=1': (R >= 1).astype(float),
        'log(1+RCA)': np.log1p(R),
        'capped RCA (min(RCA,2))': R.clip(upper=2.0),
        'RCA percentile (within product)': R.rank(axis=0, pct=True) * (R > 0),
    }


# --------------------------------------------------------------------------- stats
def spearman(a: pd.Series, b: pd.Series):
    idx = a.dropna().index.intersection(b.dropna().index)
    r, p = stats.spearmanr(a[idx], b[idx])
    return float(r), int(len(idx))


def ols(df: pd.DataFrame, y: str, xs: list, robust: bool = True, fe: str | None = None):
    """OLS via statsmodels (HC1 SEs). Returns dict of coefs, ses, pvals, r2, n."""
    import statsmodels.api as sm
    d = df[[y] + xs + ([fe] if fe else [])].dropna()
    Xm = d[xs].astype(float)
    if fe:
        Xm = pd.concat([Xm, pd.get_dummies(d[fe], prefix='fe', drop_first=True).astype(float)], axis=1)
    Xm = sm.add_constant(Xm)
    m = sm.OLS(d[y].astype(float), Xm).fit(cov_type='HC1' if robust else 'nonrobust')
    return {'coef': {k: float(m.params[k]) for k in xs}, 'se': {k: float(m.bse[k]) for k in xs},
            'p': {k: float(m.pvalues[k]) for k in xs}, 'r2': float(m.rsquared),
            'adj_r2': float(m.rsquared_adj), 'n': int(m.nobs)}


def r2_logincome(score: pd.Series, year: int, kind='ppp'):
    """R^2 and Spearman of a country score against log GDPpc (WDI) in ``year``."""
    g = np.log(gdppc(year, kind))
    idx = score.dropna().index.intersection(g.index)
    r = np.corrcoef(score[idx], g[idx])[0, 1]
    rho, _ = stats.spearmanr(score[idx], g[idx])
    return {'r2': float(r ** 2), 'pearson': float(r), 'spearman': float(rho), 'n': int(len(idx))}


# --------------------------------------------------------------------------- long panel (Q12-Q16)
@lru_cache(maxsize=None)
def score_panel() -> pd.DataFrame:
    return pd.read_csv(NIGHTLY / 'external-data' / 'derived' / 'score_panel.csv')


def window_panel(starts, horizon: int = 10, kind: str = 'const') -> pd.DataFrame:
    """One row per (country, start year): scores at the start, annualized log growth of real
    GDPpc over [start, start+horizon] (WDI; 'const' = constant 2015 US$, 'ppp', or 'pwt'),
    log initial GDPpc, and start-year controls. Countries need GDPpc at both ends."""
    P = score_panel()
    col = {'const': 'gdppc_const2015usd', 'ppp': 'gdppc_ppp_const'}.get(kind)
    out = []
    for s in starts:
        a = P[P.year == s].set_index('iso3')
        if kind == 'pwt':
            pw = pwt().assign(g=lambda d: d.rgdpna / d['pop'])
            y0 = pw[pw.year == s].set_index('iso3').g; y1 = pw[pw.year == s + horizon].set_index('iso3').g
        else:
            w = wdi()
            y0 = w[w.year == s].set_index('iso3')[col]; y1 = w[w.year == s + horizon].set_index('iso3')[col]
        d = a.copy()
        d['y0'], d['y1'] = y0.reindex(d.index), y1.reindex(d.index)
        d['growth'] = np.log(d.y1 / d.y0) / horizon * 100
        d['lny0'] = np.log(d.y0)
        d['start'] = s
        out.append(d.reset_index())
    D = pd.concat(out)
    return D.dropna(subset=['growth', 'lny0'])


def zscore_within(D: pd.DataFrame, cols, by='start') -> pd.DataFrame:
    D = D.copy()
    for c in cols:
        D[c] = D.groupby(by)[c].transform(lambda s: (s - s.mean()) / s.std())
    return D
