#!/usr/bin/env bash
# Download Harvard Growth Lab + Penn World Table files into data/raw.
# Then run: python3 scripts/fetch_worldbank.py
set -euo pipefail
cd "$(dirname "$0")/../data/raw"
DV=https://dataverse.harvard.edu/api/access/datafile

# Atlas International Trade Data (HS92), doi:10.7910/DVN/T4CHWJ: country-year ECI, COI, diversity, growth_proj, 1995-2024
curl -sSL -o atlas_hs92_country_year.csv     "$DV/13685109?format=original"
curl -sSL -o atlas_hs92_data_dictionary.csv  "$DV/13685113?format=original"
# Atlas International Trade Data (SITC Rev. 2), doi:10.7910/DVN/H8SFD2: country-year ECI 1962-2024
curl -sSL -o atlas_sitc_country_year.csv     "$DV/13685143?format=original"
curl -sSL -o atlas_sitc_data_dictionary.csv  "$DV/13685147?format=original"
# Penn World Table 10.01 (ends 2019)
curl -sSL -o pwt1001.dta https://dataverse.nl/api/access/datafile/354098

# Growth Projections and Complexity Rankings, doi:10.7910/DVN/XTAQMC: every published version (vintage), 2019-2026
mkdir -p growth_proj_vintages
curl -sS "https://dataverse.harvard.edu/api/datasets/:persistentId/versions?persistentId=doi:10.7910/DVN/XTAQMC" \
  > growth_proj_vintages/versions.json
python3 - <<'EOF'
import json, subprocess
for v in json.load(open('growth_proj_vintages/versions.json'))['data']:
    tag = f"v{v['versionNumber']}.{v.get('versionMinorNumber', 0)}_{v['releaseTime'][:10]}"
    for f in v['files']:
        d = f['dataFile']
        name = d.get('originalFileName', d['filename'])
        subprocess.run(['curl', '-sSL', '-o', f'growth_proj_vintages/{tag}__{name}',
                        f"https://dataverse.harvard.edu/api/access/datafile/{d['id']}?format=original"], check=True)
EOF
