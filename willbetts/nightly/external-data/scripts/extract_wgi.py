"""Extract WGI point estimates (1996-2022) from raw/wgidataset.xlsx into raw/wgi_panel.csv."""
from pathlib import Path
import pandas as pd
R = Path(__file__).resolve().parents[1] / 'raw'
SHEETS = {'GovernmentEffectiveness': 'wgi_gov_effectiveness', 'RegulatoryQuality': 'wgi_regulatory_quality',
          'RuleofLaw': 'wgi_rule_of_law', 'ControlofCorruption': 'wgi_control_corruption'}
FIX = {'ADO': 'AND', 'ROM': 'ROU', 'ZAR': 'COD', 'TMP': 'TLS', 'WBG': 'PSE', 'KSV': 'XKX'}
out = []
for sh, name in SHEETS.items():
    raw = pd.read_excel(R / 'wgidataset.xlsx', sheet_name=sh, header=None)
    years, kinds = raw.iloc[13], raw.iloc[14]
    body = raw.iloc[15:]
    for j in range(2, raw.shape[1]):
        if kinds[j] == 'Estimate':
            d = pd.DataFrame({'iso3': body[1].replace(FIX).values, 'year': int(years[j]),
                              'var': name, 'v': pd.to_numeric(body[j], errors='coerce').values})
            out.append(d)
df = pd.concat(out).pivot_table(index=['iso3', 'year'], columns='var', values='v').reset_index()
df.to_csv(R / 'wgi_panel.csv', index=False)
print(df.shape, df.year.min(), df.year.max())
