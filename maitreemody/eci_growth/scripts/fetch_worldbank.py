"""Download World Bank WDI indicators (1960-2024) and country metadata via the WB API.

Writes data/raw/wdi_panel.csv (iso3, year, one column per indicator) and
data/raw/wb_countries.csv (iso3, name, region, income group; aggregates removed).
"""
import json
import sys
import time
import urllib.request
from pathlib import Path

import pandas as pd

RAW = Path(__file__).resolve().parents[1] / 'data' / 'raw'
API = 'https://api.worldbank.org/v2'
INDICATORS = {
    'NY.GDP.PCAP.KD': 'gdppc_const_usd',      # constant 2015 US$
    'NY.GDP.PCAP.PP.KD': 'gdppc_ppp_const',   # PPP, constant 2021 intl $
    'NY.GDP.TOTL.RT.ZS': 'resource_rents_pct_gdp',
    'SP.POP.TOTL': 'population',
}


def get(url):
    for attempt in range(5):
        try:
            with urllib.request.urlopen(url, timeout=90) as r:
                return json.load(r)
        except Exception as e:  # API is flaky; retry
            print('retry', attempt, e, file=sys.stderr)
            time.sleep(3 * (attempt + 1))
    raise RuntimeError(url)


def main():
    frames = []
    for code, name in INDICATORS.items():
        j = get(f'{API}/country/all/indicator/{code}?date=1960:2024&format=json&per_page=20000')
        rows = j[1] or []
        d = pd.DataFrame({'iso3': [x['countryiso3code'] for x in rows],
                          'year': [int(x['date']) for x in rows],
                          'value': [x['value'] for x in rows]})
        d['var'] = name
        frames.append(d)
        print(code, len(rows), 'pages', j[0]['pages'])
    df = pd.concat(frames)
    df = df[df.iso3.str.len() == 3]
    wide = df.pivot_table(index=['iso3', 'year'], columns='var', values='value').reset_index()
    wide.to_csv(RAW / 'wdi_panel.csv', index=False)
    print('wdi_panel', wide.shape)

    j = get(f'{API}/country?format=json&per_page=400')
    meta = pd.DataFrame([{'iso3': c['id'], 'name': c['name'], 'region': c['region']['value'],
                          'income_group': c['incomeLevel']['value']} for c in j[1]])
    meta = meta[meta.region != 'Aggregates']
    meta.to_csv(RAW / 'wb_countries.csv', index=False)
    print('wb_countries', meta.shape)


if __name__ == '__main__':
    main()
