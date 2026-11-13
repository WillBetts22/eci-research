"""Load every published edition (vintage) of the Growth Lab growth projections into one long table.

Columns: vintage (e.g. 'v1.0_2019-06-03'), release_date, iso3, base_year, growth_proj.
"""
from pathlib import Path

import pandas as pd

VDIR = Path(__file__).resolve().parents[1] / 'data' / 'raw' / 'growth_proj_vintages'


def m49_to_iso3():
    """Growth Lab country_id (augmented UN M49) -> ISO3, from the Atlas country-year file."""
    a = pd.read_csv(VDIR.parent / 'atlas_hs92_country_year.csv', usecols=['country_id', 'country_iso3_code'])
    return a.drop_duplicates().set_index('country_id').country_iso3_code


def load_vintages():
    out = []
    m49 = m49_to_iso3()
    for f in sorted(VDIR.glob('*')):
        if not (f.name.endswith('rankings.dta') or f.name.endswith('growth_proj_eci_rankings.csv')):
            continue
        d = pd.read_stata(f) if f.suffix == '.dta' else pd.read_csv(f)
        if 'code' in d.columns:
            d = d.rename(columns={'code': 'iso3'})
        elif 'country_iso3_code' in d.columns:
            d = d.rename(columns={'country_iso3_code': 'iso3'})
            # some 2025 rows have a blank ISO3 code; fall back to the numeric country_id
            d['iso3'] = d.iso3.fillna(d.country_id.astype(int).map(m49))
        else:  # 2024 editions carry only the numeric country_id
            d['iso3'] = d.country_id.astype(int).map(m49)
        d = d.rename(columns={'year': 'base_year'})
        d = d.dropna(subset=['growth_proj'])[['iso3', 'base_year', 'growth_proj']]
        d['base_year'] = d.base_year.astype(int)
        tag = f.name.split('__')[0]
        d['vintage'] = tag
        d['release_date'] = pd.Timestamp(tag.split('_')[1])
        out.append(d)
    V = pd.concat(out, ignore_index=True)
    # Dataverse sometimes republished identical files under a new version; keep them but flag duplicates
    return V


if __name__ == '__main__':
    V = load_vintages()
    print(V.groupby('vintage').agg(release=('release_date', 'first'), first_base=('base_year', 'min'),
                                   last_base=('base_year', 'max'), n_last=('base_year', lambda s: (s == s.max()).sum())))
