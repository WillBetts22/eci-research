#!/usr/bin/env bash
# Download the external data used by Q06, Q12-Q16 into external-data/raw (about 800 MB before compaction).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p raw wdi_bulk
DV=https://dataverse.harvard.edu/api/access/datafile
curl -sSL -o raw/atlas_hs92_country_year.csv         "$DV/13685109?format=original"
curl -sSL -o raw/atlas_hs92_data_dictionary.csv      "$DV/13685113?format=original"
curl -sSL -o raw/atlas_hs92_product_year_4.csv       "$DV/13685116?format=original"
curl -sSL -o raw/atlas_hs92_country_product_year_4.csv "$DV/13685110?format=original"
curl -sSL -o raw/pwt1001.dta https://dataverse.nl/api/access/datafile/354098
curl -sSL -o raw/wgidataset.xlsx https://www.worldbank.org/content/dam/sites/govindicators/doc/wgidataset.xlsx
curl -sSL -o wdi_bulk/WDI_CSV.zip https://databankfiles.worldbank.org/public/ddpext_download/WDI_CSV.zip
python3 scripts/compact_atlas.py
python3 scripts/extract_wdi.py
python3 scripts/extract_wgi.py
