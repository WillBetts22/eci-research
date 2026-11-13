"""Shared ECI helpers for the nightly research runs (created by nightly Q01, 2026-11-11).

Two families of functions:

* ``notebook_*`` -- a faithful, vectorised port of the lab notebook
  (``code/current/Spring2026.ipynb``: ``df_to_matrix`` #6, ``compute_mcp`` #11,
  ``compute_mcc`` #12, ``compute_eci`` #14). Use these only to reproduce what
  the reports printed. They keep the notebook's quirks on purpose:
  - countries with a zero in *any* column are dropped (KNOWN-ISSUES D2);
  - RCA uses a strict ``>`` (share > world share);
  - the eigenvector is *column 1 of scipy.linalg.eig*, which is unsorted, so it
    is not guaranteed to be the second-largest eigenvalue;
  - the sign is set by whichever country happens to be in row 0.

* ``mcp`` / ``eci_pci`` / ``eci_from_exports`` -- the standard method
  (Hidalgo & Hausmann 2009) with the eigenvalues **sorted** and the sign
  **oriented so that ECI correlates positively with diversity** (PCI oriented
  negatively with ubiquity). Use these for research.

Loaders: ``load_groups`` (the 18-group cleaned CSVs) and ``load_hs4`` (HS4
products built from ``data/raw/<year>_mega.csv``, following Maitree's
``maitreemody/analyze.py``). ``m49_to_iso3`` / ``group_name_to_iso3`` give ISO3
keys so merges never depend on names (KNOWN-ISSUES D6).

Import from a notebook in ``willbetts/nightly/runs/<run>/``::

    import sys; sys.path.insert(0, '../../lib')
    import eci
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import linalg as LA

REPO = Path(__file__).resolve().parents[3]

AGGREGATE_GROUP = 'High-complexity Products'

# Cell #6 (index 11) of Spring2026.ipynb, applied to every cleaned CSV before ECI.
NOTEBOOK_RENAMES = {
    'Plurinational State of Bolivia': 'Bolivia',
    'Norway, Svalbard and Jan Mayen': 'Norway',
    'Russian Federation': 'Russia',
    'Korea, Rep.': 'South Korea',
    'Republic of Korea': 'South Korea',
    'France, Monaco': 'France',
    'Congo, Dem. Rep.': 'Congo',
    'Congo, Rep.': 'Congo',
    "Côte d'Ivoire": "Cote d'Ivoire",
    'Bahamas, The': 'Bahamas',
    'Yemen, Rep.': 'Yemen',
    'Viet Nam': 'Vietnam',
    'USA, Puerto Rico and US Virgin Islands': 'USA',
    'United States': 'USA',
}

# Comtrade reporter codes that are regional aggregates, not countries (from maitreemody/analyze.py).
M49_AGGREGATES = {97, 899, 472, 129, 221, 290, 292, 527, 568, 577, 636, 637, 697, 838, 839, 849, 879}
# Comtrade codes that pycountry does not map (or maps to a different ISO numeric).
M49_SPECIAL_ISO3 = {842: 'USA', 757: 'CHE', 251: 'FRA', 579: 'NOR', 699: 'IND', 711: 'ZAF', 490: 'TWN',
                    381: 'ITA'}  # 381 added 2026-11-12 (data-request 2026-11-12-eu28-and-italy-codes)


# --------------------------------------------------------------------------- loaders
def load_groups(year: int, drop_aggregate: bool = False, notebook_names: bool = True,
                path: Path | None = None) -> pd.DataFrame:
    """Cleaned 18-group exports (countries x groups), as the notebook reads them.

    Column names are stripped (the raw header has ``'Precious Stones\\t'``, D5).
    ``notebook_names`` applies the notebook's rename cell. Duplicated names after
    renaming (none expected) raise.
    """
    path = path or REPO / 'data/cleaned' / f'{year}clean.csv'
    g = pd.read_csv(path)
    if notebook_names:
        g['Country'] = g['Country'].replace(NOTEBOOK_RENAMES)
    g = g.set_index('Country')
    g.columns = g.columns.str.strip()
    if g.index.duplicated().any():
        raise ValueError(f'duplicate countries after renaming: {list(g.index[g.index.duplicated()])}')
    g = g.apply(pd.to_numeric, errors='coerce').fillna(0.0)
    if drop_aggregate:
        g = g.drop(columns=[AGGREGATE_GROUP])
    return g


def load_hs4(year: int, min_exports: float = 1e9, drop_chapters=('98', '99'),
             drop_aggregates: bool = True, return_resource_share: bool = False):
    """HS4 exports (M49 reporter code x HS4) from ``data/raw/<year>_mega.csv``.

    Mirrors ``maitreemody/analyze.py::load_hs4``: zero-pads codes to 6 digits,
    drops HS chapters 98/99, drops regional aggregates and reporters with total
    exports below ``min_exports`` (US$).
    """
    raw = pd.read_csv(REPO / 'data/raw' / f'{year}_mega.csv', index_col=0)
    if 'commodity_code' in raw.columns:          # 2019-2022 layout
        cmd = raw.pop('commodity_code')
    else:                                        # 2023 layout: codes are the index
        cmd = pd.Series(raw.index, index=raw.index)
    cmd = cmd.astype(str).str.zfill(6)
    raw = raw.apply(pd.to_numeric, errors='coerce').fillna(0)
    keep = ~cmd.str[:2].isin(list(drop_chapters))
    raw, cmd = raw[keep], cmd[keep]
    resource = raw[cmd.str[:2].isin(['26', '27', '71'])].sum() / raw.sum()
    X = raw.groupby(cmd.str[:4].values).sum().T
    X.index = X.index.astype(int)
    resource.index = resource.index.astype(int)
    if drop_aggregates:
        X = X.drop(index=[c for c in X.index if c in M49_AGGREGATES])
    X = X.loc[X.sum(axis=1) >= min_exports]
    return (X, resource.reindex(X.index)) if return_resource_share else X


def m49_to_iso3(code: int) -> str | None:
    import pycountry
    code = int(code)
    if code in M49_SPECIAL_ISO3:
        return M49_SPECIAL_ISO3[code]
    c = pycountry.countries.get(numeric=f'{code:03d}')
    return c.alpha_3 if c else None


def _name_to_m49() -> dict:
    codes = pd.read_csv(REPO / 'data/archive/2022-fall/Country_Code.csv', encoding='latin-1').iloc[:, :2]
    codes.columns = ['code', 'name']
    codes['name'] = codes['name'].str.strip()
    return dict(zip(codes.name, codes.code.astype(int)))


def group_name_to_iso3(names) -> pd.Series:
    """ISO3 for country names as they appear in the cleaned CSVs (raw, *before* notebook renames)."""
    n2c = _name_to_m49()
    out = {}
    for n in names:
        c = n2c.get(str(n).strip())
        out[n] = m49_to_iso3(c) if c is not None and c not in M49_AGGREGATES else None
    return pd.Series(out, name='iso3')


# --------------------------------------------------------------------------- notebook port
def notebook_filter(X: pd.DataFrame) -> pd.DataFrame:
    """``df_to_matrix``: keep only countries with strictly positive exports in every column."""
    return X.loc[(X > 0).all(axis=1)]


def notebook_mcp(X: pd.DataFrame) -> pd.DataFrame:
    """``compute_mcp``: M=1 iff country share > world share (strict)."""
    share = X.div(X.sum(axis=1), axis=0)
    world = X.sum(axis=0) / X.to_numpy().sum()
    return (share > world).astype(float)


def notebook_eci(X: pd.DataFrame, apply_filter: bool = True, return_diag: bool = False):
    """Faithful port of the notebook's ECI (cells #11, #12, #14).

    With ``return_diag`` also returns which eigenvalue rank (1 = largest) the
    notebook's column 1 corresponds to, and whether its sign agrees with diversity.
    """
    if apply_filter:
        X = notebook_filter(X)
    M = notebook_mcp(X).to_numpy()
    kc, kp = M.sum(1), M.sum(0)
    with np.errstate(divide='ignore', invalid='ignore'):
        W = M / kc[:, None] / kp[None, :]
    W = np.nan_to_num(W, nan=0.0, posinf=0.0, neginf=0.0)   # notebook skips inf/nan terms
    mcc = W @ M.T
    vals, vecs = LA.eig(mcc)
    v = vecs[:, 1].real
    eci = (v - v.mean()) / v.std() if v[0] < 0 else (v.mean() - v) / v.std()
    s = pd.Series(eci, index=X.index, name='eci_notebook')
    if not return_diag:
        return s
    order = np.argsort(-vals.real)
    rank_of_col1 = int(np.where(order == 1)[0][0]) + 1
    diag = {
        'n_countries': len(X),
        'col1_eigenvalue': float(vals.real[1]),
        'col1_eigen_rank': rank_of_col1,
        'second_largest_eigenvalue': float(vals.real[order[1]]),
        'sign_agrees_with_diversity': bool(np.corrcoef(eci, kc)[0, 1] > 0),
    }
    return s, diag


# --------------------------------------------------------------------------- standard method
def rca(X: pd.DataFrame) -> pd.DataFrame:
    X = X.loc[X.sum(axis=1) > 0, X.sum(axis=0) > 0]
    return X.div(X.sum(axis=1), axis=0) / (X.sum(axis=0) / X.to_numpy().sum())


def mcp(X: pd.DataFrame, threshold: float = 1.0, strict: bool = False) -> pd.DataFrame:
    """Binary RCA matrix. ``strict=True`` uses ``>`` (notebook), else ``>=`` (Atlas/Maitree)."""
    R = rca(X)
    M = (R > threshold) if strict else (R >= threshold)
    M = M.astype(float)
    return M.loc[M.sum(axis=1) > 0, M.sum(axis=0) > 0]


def eci_pci(M: pd.DataFrame, orient: str = 'diversity'):
    """ECI and PCI from a binary M (countries x products).

    Uses the symmetric form B = Dc^-1/2 M Dp^-1/2 so the eigen-decomposition is
    real and sorted. Returns (eci Series, pci Series, diag dict) where diag holds
    the top-3 eigenvalues and the eigengap lambda2 - lambda3.
    """
    Mv = M.to_numpy(float)
    kc, kp = Mv.sum(1), Mv.sum(0)
    B = Mv / np.sqrt(kc[:, None] * kp[None, :])
    U, S, Vt = np.linalg.svd(B, full_matrices=False)    # eigvals of Mcc = S**2, sorted desc
    k = U[:, 1] / np.sqrt(kc)
    q = Vt[1, :] / np.sqrt(kp)
    if orient == 'diversity':
        if np.corrcoef(k, kc)[0, 1] < 0:
            k = -k
        if np.corrcoef(q, kp)[0, 1] > 0:
            q = -q
    eci = pd.Series((k - k.mean()) / k.std(), index=M.index, name='eci')
    pci = pd.Series((q - q.mean()) / q.std(), index=M.columns, name='pci')
    lam = S ** 2
    diag = {'lambda1': float(lam[0]), 'lambda2': float(lam[1]),
            'lambda3': float(lam[2]) if len(lam) > 2 else np.nan,
            'eigengap_23': float(lam[1] - lam[2]) if len(lam) > 2 else np.nan,
            'n_countries': M.shape[0], 'n_products': M.shape[1]}
    return eci, pci, diag


def eci_from_exports(X: pd.DataFrame, threshold: float = 1.0, strict: bool = False,
                     return_all: bool = False):
    """Standard ECI (sorted eigenvalues, oriented to diversity) straight from export values."""
    M = mcp(X, threshold=threshold, strict=strict)
    e, p, d = eci_pci(M)
    if return_all:
        return e, p, d, M
    return e
