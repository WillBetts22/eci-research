"""Audit Project 3 inputs; run with .venv/bin/python juliawang/prepare_growth_data.py.

Download source first (451 MB, deliberately excluded from git):
curl --fail --location --output juliawang/data/raw/atlas_hs92_country_product_year_4.csv \
  'https://dataverse.harvard.edu/api/access/datafile/13685110?format=original'
Metadata: https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/T4CHWJ
"""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RAW = HERE / 'data/raw'
OUT = HERE / 'data/derived'
YEARS = [1997, 1998, 1999, 2007, 2008, 2009]


def prepare():
    OUT.mkdir(parents=True, exist_ok=True)
    source = RAW / 'atlas_hs92_country_product_year_4.csv'
    metadata = json.loads((RAW / 'atlas_dataset_metadata.json').read_text())['data']['latestVersion']
    file_meta = next(f['dataFile'] for f in metadata['files'] if f['dataFile']['id'] == 13685110)
    with source.open('rb') as f:
        checksum = hashlib.file_digest(f, 'md5').hexdigest()
    assert checksum == file_meta['checksum']['value'], 'Source checksum does not match Dataverse.'
    parts = []
    year_counts = {}
    for chunk in pd.read_csv(source, dtype={'country_iso3_code': str, 'product_hs92_code': str},
                             usecols=['country_iso3_code', 'product_hs92_code', 'year', 'export_value'],
                             chunksize=250_000):
        for year, n in chunk.groupby('year').size().items():
            year_counts[int(year)] = year_counts.get(int(year), 0) + int(n)
        parts.append(chunk.loc[chunk.year.isin(YEARS)].copy())
    trade = pd.concat(parts, ignore_index=True).rename(columns={
        'country_iso3_code': 'iso3', 'product_hs92_code': 'hs4'})
    assert set(YEARS) <= set(trade.year), 'Required years missing.'
    assert not trade.duplicated(['iso3', 'hs4', 'year']).any(), 'Duplicate country-product-year keys.'
    assert trade.iso3.notna().all() and trade.hs4.notna().all()
    assert np.isfinite(trade.export_value).all() and (trade.export_value >= 0).all()
    goods_mask = trade.hs4.str.fullmatch(r'\d{4}')
    non_goods = sorted(trade.loc[~goods_mask, 'hs4'].unique().tolist())
    goods = trade.loc[goods_mask].sort_values(['year', 'iso3', 'hs4'])
    goods.to_csv(OUT / 'hs92_hs4_selected_years.csv.gz', index=False, compression='gzip')
    coverage = goods.groupby('year').agg(rows=('hs4', 'size'), countries=('iso3', 'nunique'),
                                       products=('hs4', 'nunique'), exports_usd=('export_value', 'sum'))
    coverage.to_csv(OUT / 'trade_coverage.csv')
    cy = pd.read_csv(ROOT / 'maitreemody/eci_growth/data/derived/country_year.csv')
    assert not cy.duplicated(['iso3', 'year']).any()
    assert cy.iso3.str.fullmatch(r'[A-Z]{3}').all()
    audit, eligible_rows, stages = [], [], []
    for start in [1998, 2008]:
        a = cy.loc[cy.year.eq(start)].set_index('iso3')
        b = cy.loc[cy.year.eq(start + 10)].set_index('iso3')
        w = a[['gdppc_ppp_const', 'population', 'resource_rents_pct_gdp', 'exports_hs',
               'eci_hs', 'diversity_hs']].copy()
        w['y1'] = b.gdppc_ppp_const.reindex(w.index)
        totals = goods.loc[goods.year.eq(start)].groupby('iso3').export_value.sum()
        w['hs4_goods_exports_usd'] = totals.reindex(w.index)
        w['start'] = start
        w['end'] = start + 10
        # Use the consistent goods-only source for the actual export eligibility threshold.
        rules = {
            'positive GDP at both endpoints': w.gdppc_ppp_const.gt(0) & w.y1.gt(0),
            'population >= 1 million': w.population.ge(1e6),
            'HS4 goods exports >= $1 billion': w.hs4_goods_exports_usd.ge(1e9),
            'start-year resource rents available': w.resource_rents_pct_gdp.notna(),
        }
        keep = pd.Series(True, index=w.index)
        stages.append({'start': start, 'stage': 'start-year rows', 'remaining': int(keep.sum()), 'excluded': 0})
        for label, mask in rules.items():
            before = int(keep.sum())
            keep &= mask
            stages.append({'start': start, 'stage': label, 'remaining': int(keep.sum()),
                           'excluded': before - int(keep.sum())})
        w['eligible'] = keep
        w['eligible_using_published_exports'] = (rules['positive GDP at both endpoints'] &
            rules['population >= 1 million'] & w.exports_hs.ge(1e9) & rules['start-year resource rents available'])
        w['growth'] = np.nan
        positive = rules['positive GDP at both endpoints']
        w.loc[positive, 'growth'] = 100 * np.log(w.loc[positive, 'y1'] / w.loc[positive, 'gdppc_ppp_const']) / 10
        w['log_initial_income'] = np.log(w.gdppc_ppp_const.where(w.gdppc_ppp_const.gt(0)))
        w['goods_to_published_exports_ratio'] = w.hs4_goods_exports_usd / w.exports_hs.where(w.exports_hs.gt(0))
        audit.append(w.reset_index())
        eligible_rows.append(w.loc[keep].reset_index())
    audit = pd.concat(audit, ignore_index=True)
    eligible = pd.concat(eligible_rows, ignore_index=True)
    audit.to_csv(OUT / 'country_window_audit.csv', index=False)
    eligible.to_csv(OUT / 'growth_windows_preliminary.csv', index=False)
    pd.DataFrame(stages).to_csv(OUT / 'sample_flow.csv', index=False)
    # Define a fixed trade-network universe over these six years, separate from regression eligibility.
    totals = goods.groupby(['iso3', 'year']).export_value.sum().unstack('year').reindex(columns=YEARS)
    network = totals.index[totals.gt(0).all(axis=1)]
    pd.DataFrame({'iso3': network}).to_csv(OUT / 'network_countries.csv', index=False)
    all_countries = set(goods.iso3)
    unrecognized = sorted(all_countries - set(cy.iso3))
    summary = {
        'dataset_doi': '10.7910/DVN/T4CHWJ',
        'version': f"{metadata['versionNumber']}.{metadata['versionMinorNumber']}",
        'release_time': metadata.get('releaseTime'), 'download_date': '2026-11-13',
        'source_url': 'https://dataverse.harvard.edu/api/access/datafile/13685110?format=original',
        'file_id': 13685110, 'bytes': source.stat().st_size, 'md5': checksum,
        'classification': 'HS 1992, 4 digits', 'units': 'current USD',
        'source_year_min': min(year_counts), 'source_year_max': max(year_counts),
        'source_rows': sum(year_counts.values()), 'selected_years': YEARS,
        'non_four_digit_codes_excluded': non_goods,
        'unmatched_trade_country_codes': unrecognized,
        'fixed_positive_trade_network_countries': len(network),
        'eligible_countries': {str(s): int(n) for s, n in eligible.groupby('start').size().items()},
        'eligible_countries_missing_from_fixed_network': sorted(set(eligible.iso3) - set(network)),
        'threshold_disagreements_vs_published_exports': int((audit.eligible != audit.eligible_using_published_exports).sum()),
        'missing_trade_cells': 'Not converted to zero here. A later matrix construction must explicitly justify zero-filling absent country-product records.',
        'network_rule': 'Candidate: positive goods exports in all six selected years. No GDP or outcome eligibility used to construct network.',
        'status': 'Data readiness audit only; no competing measures or growth regressions computed.'
    }
    (OUT / 'data_manifest.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))
    print('\nTrade coverage:\n', coverage.to_string())
    print('\nSample flow:\n', pd.DataFrame(stages).to_string(index=False))
    return summary


if __name__ == '__main__':
    prepare()
