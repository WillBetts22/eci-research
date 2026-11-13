"""Q06 - Where does 2023's $45T come from? (D1)

Reconcile totals across: cleaned CSV (with/without the High-complexity aggregate, with/without
EU-28), raw mega (with/without regional aggregates and chapters 98/99), the Growth Lab's
world goods exports, and WDI merchandise exports. Then attribute the 2022->2023 change by
reporter and by HS chapter.
"""
import sys, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / 'lib'))
import numpy as np, pandas as pd
import eci, research as R
import warnings; warnings.filterwarnings('ignore')

t0 = time.time()
YEARS = [2019, 2020, 2021, 2022, 2023]
T = 1e12
rows = []
atl = R.atlas_cy()
w = R.wdi()
for y in YEARS:
    g = eci.load_groups(y, notebook_names=False)
    eu = [n for n in g.index if 'EU' in str(n)]
    raw = R.raw_hs6(y)
    agg_cols = [c for c in raw.columns if c in eci.M49_AGGREGATES]
    ch = raw.index.str[:2]
    nonagg = raw.drop(columns=agg_cols)
    a = atl[atl.year == y]
    rows.append({
        'year': y,
        'cleaned_all_columns': g.to_numpy().sum() / T,
        'cleaned_without_HC_aggregate': g.drop(columns=[eci.AGGREGATE_GROUP]).to_numpy().sum() / T,
        'cleaned_without_HC_and_EU28': g.drop(columns=[eci.AGGREGATE_GROUP], index=eu).to_numpy().sum() / T,
        'HC_aggregate_column': g[eci.AGGREGATE_GROUP].sum() / T,
        'EU28_row': g.loc[eu].to_numpy().sum() / T,
        'raw_all_reporters': raw.to_numpy().sum() / T,
        'raw_regional_aggregate_reporters': raw[agg_cols].to_numpy().sum() / T,
        'raw_countries_only': nonagg.to_numpy().sum() / T,
        'raw_countries_ch99': nonagg[ch == '99'].to_numpy().sum() / T,
        'raw_countries_ch98': nonagg[ch == '98'].to_numpy().sum() / T,
        'raw_n_reporters': raw.shape[1], 'raw_n_hs6_rows': raw.shape[0],
        'atlas_goods_exports_all_countries': a.export_value.sum() / T,
        'wdi_world_merch_exports': w[(w.iso3 == 'WLD') & (w.year == y)].merch_exports_usd.sum() / T,
    })
tot = pd.DataFrame(rows).set_index('year')
tot.to_csv(HERE / 'figures' / 'totals_trillions.csv')

# 2022 -> 2023 attribution (countries only, raw)
r22 = R.raw_hs6(2022); r23 = R.raw_hs6(2023)
rep22 = r22.drop(columns=[c for c in r22.columns if c in eci.M49_AGGREGATES]).sum()
rep23 = r23.drop(columns=[c for c in r23.columns if c in eci.M49_AGGREGATES]).sum()
dd = pd.concat([rep22.rename('2022'), rep23.rename('2023')], axis=1).fillna(0)
dd['change'] = dd['2023'] - dd['2022']
dd['iso3'] = [eci.m49_to_iso3(c) for c in dd.index]
# compare each reporter with Atlas totals
a22 = atl[atl.year == 2022].set_index('iso3').export_value; a23 = atl[atl.year == 2023].set_index('iso3').export_value
dd['atlas_2023'] = dd.iso3.map(a23); dd['ratio_raw_to_atlas_2023'] = dd['2023'] / dd['atlas_2023']
dd['ratio_raw_to_atlas_2022'] = dd['2022'] / dd.iso3.map(a22)
top_rep = dd.sort_values('change', ascending=False).head(12)
top_rep.to_csv(HERE / 'figures' / 'top_reporter_increases_2022_2023.csv')
ch22 = r22.drop(columns=[c for c in r22.columns if c in eci.M49_AGGREGATES]).groupby(r22.index.str[:2]).sum().sum(axis=1)
ch23 = r23.drop(columns=[c for c in r23.columns if c in eci.M49_AGGREGATES]).groupby(r23.index.str[:2]).sum().sum(axis=1)
chd = pd.concat([ch22.rename('2022'), ch23.rename('2023')], axis=1).fillna(0); chd['change'] = chd['2023'] - chd['2022']
top_ch = chd.sort_values('change', ascending=False).head(10)
top_ch.to_csv(HERE / 'figures' / 'top_chapter_increases_2022_2023.csv')
# share of reporters whose raw total is within 10% of Atlas, by year
within = {}
for y in YEARS:
    r = R.raw_hs6(y); rr = r.drop(columns=[c for c in r.columns if c in eci.M49_AGGREGATES]).sum()
    iso = pd.Series([eci.m49_to_iso3(c) for c in rr.index], index=rr.index)
    at = atl[atl.year == y].set_index('iso3').export_value
    ratio = (rr / iso.map(at)).dropna()
    ratio = ratio[np.isfinite(ratio)]
    within[y] = {'n': int(len(ratio)), 'median_ratio_raw_to_atlas': float(ratio.median()),
                 'share_within_10pct': float(((ratio > .9) & (ratio < 1.1)).mean()),
                 'n_ratio_gt_1_5': int((ratio > 1.5).sum()),
                 'n_ratio_1_8_to_2_2': int(((ratio >= 1.8) & (ratio <= 2.2)).sum()), 'n_ratio_gt_2_2': int((ratio > 2.2).sum())}
# duplicated HS6 codes inside a year's file (possible double pull)
dups = {y: int(R.raw_hs6(y).index.duplicated().sum()) for y in YEARS}
res = {'totals_trillions': tot.reset_index().to_dict('records'), 'raw_vs_atlas_by_reporter': within,
       'duplicated_hs6_codes': dups,
       'top_reporter_increases': [{'m49': int(i), 'iso3': r.iso3, 'change_bn': r.change / 1e9, 'raw2023_bn': r['2023'] / 1e9,
                                   'ratio_raw_to_atlas_2023': r.ratio_raw_to_atlas_2023, 'ratio_raw_to_atlas_2022': r.ratio_raw_to_atlas_2022}
                                  for i, r in top_rep.iterrows()],
       'top_chapter_increases': [{'chapter': i, 'change_bn': r.change / 1e9, 'v2022_bn': r['2022'] / 1e9, 'v2023_bn': r['2023'] / 1e9} for i, r in top_ch.iterrows()],
       'runtime_s': time.time() - t0}
R.save_json(res, HERE / 'results.json')
pd.set_option('display.width', 250)
print(tot.round(2).T.to_string()); print(within); print(dups)
print(top_rep[['iso3', '2022', '2023', 'change', 'ratio_raw_to_atlas_2022', 'ratio_raw_to_atlas_2023']].assign(**{c: lambda d, c=c: d[c] / 1e9 for c in ['2022', '2023', 'change']}).round(2).to_string())
print((top_ch / 1e9).round(1).to_string())
