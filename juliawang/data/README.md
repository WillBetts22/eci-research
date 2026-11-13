# Project 3 data readiness

Data prepared November 13, 2026. This page documents the input-readiness stage. The notebook now also contains calculated export measures, ECI validation and initial growth regressions; results are saved under `juliawang/outputs/project3/`.

## Inputs

- Historical trade: Harvard Growth Lab, *International Trade Data (HS92)*, DOI `10.7910/DVN/T4CHWJ`, version 18.0 (April 22, 2026), file ID 13685110. Export values are current USD; product codes use HS 1992. Downloaded November 13, 2026. The original file is 451,749,132 bytes; its MD5 matches Harvard's metadata.
- Country panel: `maitreemody/eci_growth/data/derived/country_year.csv`; source documentation in that project's README. Uses real PPP GDP per capita for this project's outcome, starting population and resource rents, and published HS ECI/diversity.
- `raw/atlas_dataset_metadata.json` records the retrieved Harvard release and checksum.

## Reproduce

From the repository root, using the local `.venv` Python environment:

```sh
mkdir -p juliawang/data/raw
curl --fail --location --output juliawang/data/raw/atlas_dataset_metadata.json 'https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/T4CHWJ'
curl --fail --location --output juliawang/data/raw/atlas_hs92_country_product_year_4.csv 'https://dataverse.harvard.edu/api/access/datafile/13685110?format=original'
.venv/bin/python juliawang/prepare_growth_data.py
```

Preparation requires pandas and NumPy. Notebook execution also requires IPython, nbformat, nbclient and ipykernel. The large original and compressed trade extract are locally available but excluded from git. Future downloads can change: verify the saved manifest's release and checksum, not merely the URL.

## Outputs and findings

- `derived/hs92_hs4_selected_years.csv.gz`: 1997–1999 and 2007–2009 goods records, retaining leading zeros. All six years have 1,242 unique four-digit product codes. Non-four-digit `XXXX` records are excluded; no interpretation as services is assumed.
- `derived/trade_coverage.csv`: row/country/product counts and export sums by year.
- `derived/country_window_audit.csv`: all starting countries, endpoint availability, controls and eligibility flags.
- `derived/growth_windows_preliminary.csv`: 95 eligible observations for 1998–2008 and 129 for 2008–2018. Population is at least 1 million; start-year goods exports are at least $1 billion. Growth is annualized log change in real PPP GDP per person. All preliminary eligible observations have published HS ECI and diversity.
- `derived/sample_flow.csv`: sequential exclusions. Goods-only and published-export thresholds select the same preliminary samples, although export totals differ.
- `derived/network_countries.csv`: 210 countries with positive goods exports in all selected years, a candidate fixed network, not a final decision. Botswana, Namibia and Serbia qualify for the later growth sample but are absent from this network. Do not silently drop them.
- `derived/data_manifest.json`: provenance, checksum, source coverage, excluded product codes, unmatched trade-country identifiers, and audit status.

## Analysis status

Diversity, entropy, HHI and standard ECI have been calculated and compared in the notebook. Initial growth models train on 1998–2008 and test on 2008–2018. The primary network uses each year’s population/export thresholds; a broader positive-export network is included as a sensitivity check. Document zero-filling of missing records and the trade-network universe. A fixed six-year universe uses future trade coverage relative to 1998; year-specific networks are needed as a sensitivity check. GDP outcomes must not select the network used to construct RCA.

Goods-only reconstructions of the lab groups cannot reproduce services. The source includes chapter 99 but not 98; chapter 77 is absent. Inspect empty groups and omitted goods chapters before comparing aggregation levels. No original mappings have been changed.
