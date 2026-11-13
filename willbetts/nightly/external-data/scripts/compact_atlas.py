"""Compact the Atlas HS92 HS4 panel to raw/atlas_hs4_exports.pkl (iso3, hs4, year, export_value)."""
from pathlib import Path
import pandas as pd
R = Path(__file__).resolve().parents[1] / 'raw'
df = pd.read_csv(R / 'atlas_hs92_country_product_year_4.csv',
                 usecols=['country_iso3_code', 'product_hs92_code', 'year', 'export_value'],
                 dtype={'country_iso3_code': 'category', 'product_hs92_code': str, 'year': 'int16', 'export_value': 'float64'})
df = df[df.export_value > 0]
df.columns = ['iso3', 'hs4', 'year', 'export_value']
df['hs4'] = df.hs4.astype('category')
df.to_pickle(R / 'atlas_hs4_exports.pkl')
print(df.shape, df.year.min(), df.year.max(), df.iso3.nunique(), df.hs4.nunique())
