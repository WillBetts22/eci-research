"""Extract selected WDI indicators (1995-2024) from the bulk WDI_CSV.zip into raw/wdi_panel.csv."""
import zipfile, io
from pathlib import Path
import pandas as pd
B = Path(__file__).resolve().parents[1]
IND = {
    'NY.GDP.PCAP.KD': 'gdppc_const2015usd', 'NY.GDP.PCAP.PP.KD': 'gdppc_ppp_const',
    'NY.GDP.PCAP.CD': 'gdppc_current_usd', 'NY.GDP.TOTL.RT.ZS': 'resource_rents_pct_gdp',
    'SP.POP.TOTL': 'population', 'SE.TER.ENRR': 'tertiary_enrollment', 'SE.SEC.ENRR': 'secondary_enrollment',
    'GB.XPD.RSDV.GD.ZS': 'rnd_pct_gdp', 'NE.TRD.GNFS.ZS': 'trade_pct_gdp', 'IT.NET.USER.ZS': 'internet_users_pct',
    'EG.ELC.ACCS.ZS': 'electricity_access_pct', 'FS.AST.PRVT.GD.ZS': 'private_credit_pct_gdp',
    'TX.VAL.MRCH.CD.WT': 'merch_exports_usd',
}
z = zipfile.ZipFile(B / 'wdi_bulk' / 'WDI_CSV.zip')
name = [n for n in z.namelist() if n.lower().endswith('wdicsv.csv')][0]
df = pd.read_csv(z.open(name))
df = df[df['Indicator Code'].isin(IND)]
years = [str(y) for y in range(1995, 2025) if str(y) in df.columns]
long = df.melt(id_vars=['Country Code', 'Indicator Code'], value_vars=years, var_name='year', value_name='v')
long['year'] = long.year.astype(int)
wide = long.pivot_table(index=['Country Code', 'year'], columns='Indicator Code', values='v').rename(columns=IND).reset_index()
wide = wide.rename(columns={'Country Code': 'iso3'})
wide.to_csv(B / 'raw' / 'wdi_panel.csv', index=False)
print(wide.shape, wide.columns.tolist())
