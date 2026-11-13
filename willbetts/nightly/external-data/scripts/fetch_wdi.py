"""Fetch WDI + WGI indicators (1995-2024) from the World Bank API into raw/wdi_panel.csv."""
import json, sys, time, urllib.request
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / 'raw' / 'wdi_panel.csv'
WDI = {
    'NY.GDP.PCAP.KD': 'gdppc_const2015usd',
    'NY.GDP.PCAP.PP.KD': 'gdppc_ppp_const',
    'NY.GDP.PCAP.CD': 'gdppc_current_usd',
    'NY.GDP.TOTL.RT.ZS': 'resource_rents_pct_gdp',
    'SP.POP.TOTL': 'population',
    'SE.TER.ENRR': 'tertiary_enrollment',
    'SE.SEC.ENRR': 'secondary_enrollment',
    'GB.XPD.RSDV.GD.ZS': 'rnd_pct_gdp',
    'NE.TRD.GNFS.ZS': 'trade_pct_gdp',
    'IT.NET.USER.ZS': 'internet_users_pct',
    'EG.ELC.ACCS.ZS': 'electricity_access_pct',
    'FS.AST.PRVT.GD.ZS': 'private_credit_pct_gdp',
}
WGI = {'GOV_WGI_GE.EST': 'wgi_gov_effectiveness', 'GOV_WGI_RL.EST': 'wgi_rule_of_law',
       'GOV_WGI_RQ.EST': 'wgi_regulatory_quality', 'GOV_WGI_CC.EST': 'wgi_control_corruption'}

def fetch(code, source=None):
    url = (f'https://api.worldbank.org/v2/country/all/indicator/{code}'
           f'?date=1995:2024&format=json&per_page=20000' + (f'&source={source}' if source else ''))
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=120) as r:
                j = json.load(r)
            rows = j[1] or []
            return pd.DataFrame({'iso3': [x['countryiso3code'] for x in rows],
                                 'year': [int(x['date']) for x in rows],
                                 'value': [x['value'] for x in rows]})
        except Exception as e:
            print('retry', code, e, file=sys.stderr); time.sleep(3)
    raise RuntimeError(code)

frames = []
for code, name in WDI.items():
    d = fetch(code); d['var'] = name; frames.append(d); print(code, len(d))
for code, name in WGI.items():
    d = fetch(code, source=3); d['var'] = name; frames.append(d); print(code, len(d))
df = pd.concat(frames)
df = df[df.iso3.str.len() == 3]
wide = df.pivot_table(index=['iso3', 'year'], columns='var', values='value').reset_index()
wide.to_csv(OUT, index=False)
print('wrote', OUT, wide.shape)
