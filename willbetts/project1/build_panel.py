"""Project 1 panel: Maitree's country-year panel + nominal GDP + natural-resource exports.

Adds what the Atlas growth regression needs and Maitree's panel lacks:
  - nominal GDP (current US$, WDI NY.GDP.MKTP.CD) and the US GDP deflator (NY.GDP.DEFL.ZS, USA),
  - natural-resource exports by country-year from the Growth Lab SITC rev.2 2-digit file.

Natural resources follow Leamer's (1984) "petroleum" + "raw materials" clusters at the 2-digit level:
  27 crude fertilizers and minerals, 28 metal ores and scrap, 32 coal, 33 petroleum, 34 gas,
  35 electric current, 68 non-ferrous metals. Variant 'nr_gold' adds 97 (non-monetary gold);
  variant 'nr_broad' adds all primary agriculture (sections 0, 1, 2 and 4).

Inputs:  maitreemody/eci_growth/data/derived/country_year.csv (built by her scripts/panel.py)
         willbetts/nightly/external-data/wdi_bulk/WDI_CSV.zip (bulk WDI; see nightly download.sh)
         data/raw/sitc_country_product_year_2.csv (Dataverse doi:10.7910/DVN/H8SFD2, file 13685146)
Output:  data/derived/country_year_p1.csv
"""
import zipfile
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
RAW, DER = HERE / 'data' / 'raw', HERE / 'data' / 'derived'

NR_CORE = ['27', '28', '32', '33', '34', '35', '68']
NR_GOLD = NR_CORE + ['97']
NR_BROAD = sorted(set(NR_GOLD) | {f'{i:02d}' for i in range(0, 30)} | {'41', '42', '43'})


def wdi_extra():
    z = zipfile.ZipFile(REPO / 'willbetts/nightly/external-data/wdi_bulk/WDI_CSV.zip')
    name = [n for n in z.namelist() if n.lower().endswith('wdicsv.csv')][0]
    df = pd.read_csv(z.open(name))
    df = df[df['Indicator Code'].isin(['NY.GDP.MKTP.CD', 'NY.GDP.DEFL.ZS'])]
    years = [c for c in df.columns if c.isdigit()]
    long = df.melt(id_vars=['Country Code', 'Indicator Code'], value_vars=years, var_name='year', value_name='v')
    long['year'] = long.year.astype(int)
    gdp = long[long['Indicator Code'] == 'NY.GDP.MKTP.CD'].rename(columns={'Country Code': 'iso3', 'v': 'gdp_current_usd'})
    defl = long[(long['Indicator Code'] == 'NY.GDP.DEFL.ZS') & (long['Country Code'] == 'USA')]
    defl = defl[['year', 'v']].rename(columns={'v': 'us_deflator'})
    return gdp[['iso3', 'year', 'gdp_current_usd']], defl


def nr_exports():
    s = pd.read_csv(RAW / 'sitc_country_product_year_2.csv', dtype={'product_sitc_code': str},
                    usecols=['country_iso3_code', 'product_sitc_code', 'year', 'export_value'])
    s = s.rename(columns={'country_iso3_code': 'iso3', 'product_sitc_code': 'code'})
    out = s.groupby(['iso3', 'year']).export_value.sum().rename('exports_sitc2_total').to_frame()
    for name, codes in [('nr_core', NR_CORE), ('nr_gold', NR_GOLD), ('nr_broad', NR_BROAD)]:
        out[name] = s[s.code.isin(codes)].groupby(['iso3', 'year']).export_value.sum()
    return out.fillna({'nr_core': 0, 'nr_gold': 0, 'nr_broad': 0}).reset_index()


if __name__ == '__main__':
    DER.mkdir(parents=True, exist_ok=True)
    cy = pd.read_csv(REPO / 'maitreemody/eci_growth/data/derived/country_year.csv')
    gdp, defl = wdi_extra()
    cy = cy.merge(gdp, on=['iso3', 'year'], how='left').merge(defl, on='year', how='left')
    cy = cy.merge(nr_exports(), on=['iso3', 'year'], how='left')
    cy.to_csv(DER / 'country_year_p1.csv', index=False)
    chk = cy.dropna(subset=['exports_sitc', 'exports_sitc2_total'])
    ratio = (chk.exports_sitc2_total / chk.exports_sitc)
    print(cy.shape, 'SITC2 total / country-year exports: median', round(ratio.median(), 4),
          'p1-p99', round(ratio.quantile(.01), 3), round(ratio.quantile(.99), 3))
    print('NR core share of exports, 2008 median:', round((cy[cy.year == 2008].nr_core / cy[cy.year == 2008].exports_sitc2_total).median(), 3))
