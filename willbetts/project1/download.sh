#!/usr/bin/env bash
# Growth Lab SITC rev.2 country x 2-digit product exports (doi:10.7910/DVN/H8SFD2).
set -euo pipefail
cd "$(dirname "$0")"; mkdir -p data/raw
DV=https://dataverse.harvard.edu/api/access/datafile
curl -sSL -o data/raw/sitc_country_product_year_2.csv "$DV/13685146?format=original"
curl -sSL -o data/raw/sitc_product_year_2.csv "$DV/13685145?format=original"
curl -sSL -o data/raw/sitc_data_dictionary.csv "$DV/13685147?format=original"
