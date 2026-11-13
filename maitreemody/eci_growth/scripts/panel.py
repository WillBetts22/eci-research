"""Build the country-year and window panels for the ECI-growth replication (Projects 1 and 2).

Written independently of willbetts/nightly/lib so the two pipelines can check each other.
Run from anywhere: python3 maitreemody/eci_growth/scripts/panel.py
Writes data/derived/country_year.csv.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data' / 'raw'
DERIVED = ROOT / 'data' / 'derived'


def load_country_year():
    meta = pd.read_csv(RAW / 'wb_countries.csv')          # real countries only (aggregates dropped)
    wdi = pd.read_csv(RAW / 'wdi_panel.csv')
    hs = pd.read_csv(RAW / 'atlas_hs92_country_year.csv').rename(columns={
        'country_iso3_code': 'iso3', 'eci': 'eci_hs', 'coi': 'coi_hs', 'diversity': 'diversity_hs',
        'export_value': 'exports_hs', 'growth_proj': 'growth_proj_current'})
    sitc = pd.read_csv(RAW / 'atlas_sitc_country_year.csv').rename(columns={
        'country_iso3_code': 'iso3', 'eci': 'eci_sitc', 'coi': 'coi_sitc', 'diversity': 'diversity_sitc',
        'export_value': 'exports_sitc'})
    pwt = pd.read_stata(RAW / 'pwt1001.dta', columns=['countrycode', 'year', 'rgdpna', 'pop', 'hc'])
    pwt = pwt.rename(columns={'countrycode': 'iso3'})
    pwt['gdppc_pwt'] = pwt.rgdpna / pwt['pop']

    df = wdi.merge(meta, on='iso3', how='inner')
    df = df.merge(sitc[['iso3', 'year', 'eci_sitc', 'coi_sitc', 'diversity_sitc', 'exports_sitc']],
                  on=['iso3', 'year'], how='left')
    df = df.merge(hs[['iso3', 'year', 'eci_hs', 'coi_hs', 'diversity_hs', 'exports_hs', 'growth_proj_current']],
                  on=['iso3', 'year'], how='left')
    df = df.merge(pwt[['iso3', 'year', 'gdppc_pwt', 'hc']], on=['iso3', 'year'], how='left')
    return df.sort_values(['iso3', 'year']).reset_index(drop=True)


def ann_growth(y0, y1, years):
    """Annualized growth in percent per year."""
    return 100 * (np.log(y1) - np.log(y0)) / years


def window_panel(cy, starts, length=10, gdp='gdppc_const_usd', eci='eci_sitc',
                 min_pop=1e6, min_exports=None, rents_avg=True):
    """One row per country x window: growth over [start, start+length] and start-year regressors.

    Resource rents are averaged over the window by default (the Atlas controls for expected growth
    in natural-resource exports over the period; the window average is the closest proxy we have,
    though it uses information from after the start year). rents_avg=False uses start-year rents,
    which is the strictly out-of-sample version.
    """
    rows = []
    idx = cy.set_index(['iso3', 'year'])
    for s in starts:
        e = s + length
        a = cy[cy.year == s].set_index('iso3')
        b = cy[cy.year == e].set_index('iso3')
        w = pd.DataFrame(index=a.index)
        w['start'] = s
        w['end'] = e
        w['y0'] = a[gdp]
        w['y1'] = b[gdp].reindex(w.index)
        w['growth'] = ann_growth(w.y0, w.y1, length)
        w['lny0'] = np.log(w.y0)
        w['eci'] = a[eci]
        w['coi'] = a[eci.replace('eci', 'coi')]
        w['diversity'] = a[eci.replace('eci', 'diversity')]
        w['exports'] = a[eci.replace('eci', 'exports')]
        w['population'] = a['population']
        w['region'] = a['region']
        w['income_group'] = a['income_group']
        w['name'] = a['name']
        if rents_avg:
            span = cy[(cy.year >= s) & (cy.year < e)]
            w['rents'] = span.groupby('iso3').resource_rents_pct_gdp.mean().reindex(w.index)
        else:
            w['rents'] = a['resource_rents_pct_gdp']
        rows.append(w.reset_index())
    W = pd.concat(rows, ignore_index=True)
    W = W[W.population >= min_pop]
    if min_exports is not None:
        W = W[W.exports >= min_exports]
    return W


def zscore_by(df, cols, by='start'):
    """Standardize columns within each window so coefficients read as 'per 1 SD'."""
    df = df.copy()
    for c in cols:
        g = df.groupby(by)[c]
        df[c] = (df[c] - g.transform('mean')) / g.transform('std')
    return df


if __name__ == '__main__':
    DERIVED.mkdir(parents=True, exist_ok=True)
    cy = load_country_year()
    cy.to_csv(DERIVED / 'country_year.csv', index=False)
    print('country_year', cy.shape, cy.year.min(), cy.year.max(), cy.iso3.nunique())
    # ECI sign sanity check (shared convention): ECI must correlate positively with diversity
    for e, d in [('eci_sitc', 'diversity_sitc'), ('eci_hs', 'diversity_hs')]:
        r = cy.groupby('year').apply(lambda g: g[e].corr(g[d]))
        print(e, 'corr with diversity: min', round(r.min(), 2), 'years<0:', int((r < 0).sum()))
